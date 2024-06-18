from biolib.api import client as api_client
from biolib.biolib_api_client import AppGetResponse
from biolib.biolib_api_client.lfs_types import DataRecordVersionInfo


def get_data_record_state_from_uri(uri) -> 'DataRecordVersionInfo':
    app_response: AppGetResponse = api_client.get(path='/app/', params={'uri': uri}).json()
    return DataRecordVersionInfo(
        resource_uri=app_response['app_version']['app_uri'],
        resource_uuid=app_response['app']['public_id'],
        resource_version_uuid=app_response['app_version']['public_id'],
    )
