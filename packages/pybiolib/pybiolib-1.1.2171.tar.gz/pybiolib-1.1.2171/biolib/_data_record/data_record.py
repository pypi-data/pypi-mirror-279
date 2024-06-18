import os
from collections import namedtuple
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path
from struct import Struct
from typing import Callable, Dict, List, Union, cast

from biolib import api, utils
from biolib._internal import types
from biolib._internal.data_record import get_data_record_state_from_uri
from biolib._internal.data_record.data_record import validate_sqlite_v1
from biolib._internal.data_record.remote_storage_endpoint import DataRecordRemoteStorageEndpoint
from biolib._internal.file_utils import get_files_and_size_of_directory, get_iterable_zip_stream
from biolib._internal.http_client import HttpClient
from biolib.api import client as api_client
from biolib.biolib_api_client import BiolibApiClient
from biolib.biolib_api_client.lfs_types import DataRecordInfo, DataRecordVersion, DataRecordVersionInfo
from biolib.biolib_binary_format import LazyLoadedFile
from biolib.biolib_binary_format.utils import RemoteIndexableBuffer
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger
from biolib.typing_utils import Optional as _Optional
from biolib.utils.app_uri import parse_app_uri
from biolib.utils.zip.remote_zip import RemoteZip


PathFilter = Union[str, Callable[[str], bool]]


class DataRecord:
    def __init__(self, _internal_state: DataRecordVersionInfo):
        self._state = _internal_state

    def __repr__(self):
        return f'DataRecord: {self._state["resource_uri"]}'

    @property
    def uri(self) -> str:
        return self._state['resource_uri']

    @property
    def uuid(self) -> str:
        return self._state['resource_uuid']

    @property
    def name(self) -> str:
        uri_parsed = parse_app_uri(self._state['resource_uri'], use_account_as_name_default=False)
        if not uri_parsed['app_name']:
            raise ValueError('Expected parameter "resource_uri" to contain resource name')

        return uri_parsed['app_name']

    def list_files(self, path_filter: _Optional[PathFilter] = None) -> List[LazyLoadedFile]:
        remote_storage_endpoint = DataRecordRemoteStorageEndpoint(
            resource_version_uuid=self._state['resource_version_uuid'],
        )
        files: List[LazyLoadedFile] = []
        with RemoteZip(url=remote_storage_endpoint.get_remote_url()) as remote_zip:
            central_directory = remote_zip.get_central_directory()
            for file_info in central_directory.values():
                files.append(self._get_file(remote_storage_endpoint, file_info))

        return self._get_filtered_files(files=files, path_filter=path_filter) if path_filter else files

    def download_zip(self, output_path: str):
        remote_storage_endpoint = DataRecordRemoteStorageEndpoint(
            resource_version_uuid=self._state['resource_version_uuid'],
        )
        HttpClient.request(url=remote_storage_endpoint.get_remote_url(), response_path=output_path)

    def download_files(self, output_dir: str, path_filter: _Optional[PathFilter] = None) -> None:
        filtered_files = self.list_files(path_filter=path_filter)

        if len(filtered_files) == 0:
            logger.debug('No files to save')
            return

        for file in filtered_files:
            file_path = os.path.join(output_dir, file.path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, mode='wb') as file_handle:
                for chunk in file.get_data_iterator():
                    file_handle.write(chunk)

    def save_files(self, output_dir: str, path_filter: _Optional[PathFilter] = None) -> None:
        self.download_files(output_dir=output_dir, path_filter=path_filter)

    def update(self, data_path: str, chunk_size_in_mb: _Optional[int] = None) -> None:
        assert os.path.isdir(data_path), f'The path "{data_path}" is not a directory.'
        BiolibApiClient.assert_is_signed_in(authenticated_action_description='push data to a Data Record')

        if os.path.realpath(data_path) == '/':
            raise BioLibError('Pushing your root directory is not possible')

        original_working_dir = os.getcwd()
        os.chdir(data_path)
        files_to_zip, data_size_in_bytes = get_files_and_size_of_directory(directory=os.getcwd())

        if data_size_in_bytes > 4_500_000_000_000:
            raise BioLibError('Attempted to push directory with a size larger than the limit of 4.5 TB')

        # validate data record
        detailed_dict: types.DataRecordDetailedDict = self._get_detailed_dict()
        if detailed_dict['type']:
            # only validate if data record has a type
            data_record_type: types.DataRecordTypeDict = detailed_dict['type']
            logger.info(f"Validating data record of type {data_record_type['name']}")
            for rule in data_record_type['validation_rules']:
                logger.info(f"Validating rule {rule['type']} for {rule['path']}...")
                if rule['type'] == "sqlite-v1":
                    try:
                        validate_sqlite_v1(schema=rule['rule'], sqlite_file=Path(rule['path']))
                    except Exception as error:
                        raise Exception("Data Record Validation failed") from error
                else:
                    raise Exception(f"Error processing data record validation: unknown rule type {rule['type']}")

        min_chunk_size_bytes = 10_000_000
        chunk_size_in_bytes: int
        if chunk_size_in_mb:
            chunk_size_in_bytes = chunk_size_in_mb * 1_000_000  # Convert megabytes to bytes
            if chunk_size_in_bytes < min_chunk_size_bytes:
                logger.warning('Specified chunk size is too small, using minimum of 10 MB instead.')
                chunk_size_in_bytes = min_chunk_size_bytes
        else:
            # Calculate chunk size based on max chunk count of 10_000, using 9_000 to be on the safe side
            chunk_size_in_bytes = max(min_chunk_size_bytes, int(data_size_in_bytes / 9_000))

        data_size_in_mb = round(data_size_in_bytes / 10**6)
        logger.info(f'Zipping {len(files_to_zip)} files, in total ~{data_size_in_mb}mb of data')

        response = api.client.post(path='/lfs/versions/', data={'resource_uuid': self._state['resource_uuid']})
        data_record_version: DataRecordVersion = response.json()
        iterable_zip_stream = get_iterable_zip_stream(files=files_to_zip, chunk_size=chunk_size_in_bytes)

        multipart_uploader = utils.MultiPartUploader(
            use_process_pool=True,
            get_presigned_upload_url_request=dict(
                headers=None,
                requires_biolib_auth=True,
                path=f"/lfs/versions/{data_record_version['uuid']}/presigned_upload_url/",
            ),
            complete_upload_request=dict(
                headers=None,
                requires_biolib_auth=True,
                path=f"/lfs/versions/{data_record_version['uuid']}/complete_upload/",
            ),
        )

        multipart_uploader.upload(payload_iterator=iterable_zip_stream, payload_size_in_bytes=data_size_in_bytes)
        os.chdir(original_working_dir)
        logger.info(f"Successfully pushed a new Data Record version '{data_record_version['uri']}'")
        self._state = get_data_record_state_from_uri(data_record_version['uri'])

    @staticmethod
    def get_by_uri(uri: str) -> 'DataRecord':
        return DataRecord(_internal_state=get_data_record_state_from_uri(uri))

    @staticmethod
    def create(destination: str, data_path: _Optional[str] = None) -> 'DataRecord':
        BiolibApiClient.assert_is_signed_in(authenticated_action_description='create a Data Record')
        if data_path is not None:
            assert os.path.isdir(data_path), f'The path "{data_path}" is not a directory.'
        uri_parsed = parse_app_uri(destination, use_account_as_name_default=False)
        if uri_parsed['app_name_normalized']:
            data_record_uri = destination
        else:
            record_name = 'data-record-' + datetime.now().isoformat().split('.')[0].replace(':', '-')
            data_record_uri = f'{destination}/{record_name}'

        uri_parsed = parse_app_uri(data_record_uri)
        response = api.client.post(
            path='/lfs/',
            data={
                'account_handle': uri_parsed['account_handle_normalized'],
                'name': uri_parsed['app_name'],
            },
        )
        data_record_info: DataRecordInfo = response.json()
        logger.info(f"Successfully created new Data Record '{data_record_info['uri']}'")

        if data_path is not None:
            data_record = DataRecord.get_by_uri(uri=data_record_info['uri'])
            data_record.update(data_path=data_path)
            return data_record
        else:
            return DataRecord.get_by_uri(uri=data_record_info['uri'])

    @staticmethod
    def fetch(uri: _Optional[str] = None, count: _Optional[int] = None) -> List['DataRecord']:
        max_page_size = 1_000
        params: Dict[str, Union[str, int]] = {
            'page_size': str(count or max_page_size),
            'resource_type': 'data-record',
        }
        if uri:
            uri_parsed = parse_app_uri(uri, use_account_as_name_default=False)
            params['account_handle'] = uri_parsed['account_handle_normalized']
            if uri_parsed['app_name_normalized']:
                params['app_name'] = uri_parsed['app_name_normalized']

        results = api_client.get(path='/apps/', params=params).json()['results']
        if count is None and len(results) == max_page_size:
            logger.warning(
                f'Fetch results exceeded maximum count of {max_page_size}. Some data records might not be fetched.'
            )

        return [
            DataRecord(
                _internal_state={
                    'resource_uri': result['resource_uri'],
                    'resource_uuid': result['public_id'],
                    'resource_version_uuid': result['active_version'],
                }
            )
            for result in results
        ]

    @staticmethod
    def _get_file(remote_storage_endpoint: DataRecordRemoteStorageEndpoint, file_info: Dict) -> LazyLoadedFile:
        local_file_header_signature_bytes = b'\x50\x4b\x03\x04'
        local_file_header_struct = Struct('<H2sHHHIIIHH')
        LocalFileHeader = namedtuple(
            'LocalFileHeader',
            (
                'version',
                'flags',
                'compression_raw',
                'mod_time',
                'mod_date',
                'crc_32_expected',
                'compressed_size_raw',
                'uncompressed_size_raw',
                'file_name_len',
                'extra_field_len',
            ),
        )

        local_file_header_start = file_info['header_offset'] + len(local_file_header_signature_bytes)
        local_file_header_end = local_file_header_start + local_file_header_struct.size

        def file_start_func() -> int:
            local_file_header_response = HttpClient.request(
                url=remote_storage_endpoint.get_remote_url(),
                headers={'range': f'bytes={local_file_header_start}-{local_file_header_end - 1}'},
                timeout_in_seconds=300,
            )
            local_file_header = LocalFileHeader._make(
                local_file_header_struct.unpack(local_file_header_response.content)
            )
            file_start: int = (
                local_file_header_end + local_file_header.file_name_len + local_file_header.extra_field_len
            )
            return file_start

        return LazyLoadedFile(
            buffer=RemoteIndexableBuffer(endpoint=remote_storage_endpoint),
            length=file_info['file_size'],
            path=file_info['filename'],
            start=None,
            start_func=file_start_func,
        )

    @staticmethod
    def _get_filtered_files(files: List[LazyLoadedFile], path_filter: PathFilter) -> List[LazyLoadedFile]:
        if not (isinstance(path_filter, str) or callable(path_filter)):
            raise Exception('Expected path_filter to be a string or a function')

        if callable(path_filter):
            return list(filter(lambda x: path_filter(x.path), files))  # type: ignore

        glob_filter = cast(str, path_filter)

        def _filter_function(file: LazyLoadedFile) -> bool:
            return fnmatch(file.path, glob_filter)

        return list(filter(_filter_function, files))

    def _get_detailed_dict(self) -> types.DataRecordDetailedDict:
        return cast(types.DataRecordDetailedDict, api_client.get(f'/resources/data-records/{self.uuid}/').json())
