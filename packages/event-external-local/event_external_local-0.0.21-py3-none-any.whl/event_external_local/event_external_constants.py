from logger_local.LoggerComponentEnum import LoggerComponentEnum


class EventExternalLocalConstants:
    DEVELOPER_EMAIL = 'gil.a@circ.zone'
    EXTERNAL_EVENT_LOCAL_COMPONENT_ID = 251
    EVENT_EXTERNAL_LOCAL_PYHTON_COMPONENT_NAME = 'event-external-local-python-package'
    EXTERNAL_EVENT_LOCAL_CODE_LOGGER_OBJECT = {
        'component_id': EXTERNAL_EVENT_LOCAL_COMPONENT_ID,
        'component_name': EVENT_EXTERNAL_LOCAL_PYHTON_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }

    EXTERNAL_EVENT_TABLE_NAME = 'event_external_table'

    EXTERNAL_EVENT_SCHEMA_NAME = 'event_external'

    EXTERNAL_EVENT_ID_COLUMN_NAME = 'event_external_id'

    EXTERNAL_EVENT_VIEW_NAME = 'event_external_view'
