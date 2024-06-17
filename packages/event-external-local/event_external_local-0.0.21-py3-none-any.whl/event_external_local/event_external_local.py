from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger
from python_sdk_remote.utilities import validate_url

from .event_external_constants import EventExternalLocalConstants


class EventExternalsLocal(GenericCRUD, metaclass=MetaLogger,
                          object=EventExternalLocalConstants.EXTERNAL_EVENT_LOCAL_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name=EventExternalLocalConstants.EXTERNAL_EVENT_SCHEMA_NAME,
                         default_table_name=EventExternalLocalConstants.EXTERNAL_EVENT_TABLE_NAME,
                         default_column_name=EventExternalLocalConstants.EXTERNAL_EVENT_ID_COLUMN_NAME,
                         default_view_table_name=EventExternalLocalConstants.EXTERNAL_EVENT_VIEW_NAME,
                         is_test_data=is_test_data)

    def insert(self, event_external_dict: dict = None) -> int:
        # adding variables validation might be good
        event_external_dict = event_external_dict or {}
        url = event_external_dict.get("url")
        if url and not validate_url(url):
            raise ValueError("url is not valid")
        event_external_id = super().insert(data_dict=event_external_dict)
        return event_external_id

    def delete_by_event_external_id(self, event_external_id: int) -> None:
        super().delete_by_column_and_value(column_value=event_external_id)

    def update_by_event_external_id(self, event_external_id: int, event_external_dict: dict) -> None:
        url = event_external_dict.get("url")
        if url and not validate_url(url):
            raise ValueError("url is not valid")

        super().update_by_column_and_value(column_value=event_external_id, data_dict=event_external_dict)

    def select_by_event_external_id(self, event_external_id: int) -> dict:
        event_external = super().select_one_dict_by_column_and_value(column_value=event_external_id)
        return event_external

    def get_event_external_test_id(self) -> int:
        return super().get_test_entity_id(entity_name="event_external",
                                          insert_function=self.insert,
                                          view_name="event_external_view")
