from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger

CONTACT_LOCAL_PYTHON_COMPONENT_ID = 123
CONTACT_LOCAL_PYTHON_COMPONENT_NAME = 'contact-local-python'
SCHEMA_NAME = 'contact'
TABLE_NAME = 'contact_table'
VIEW_TABLE_NAME = 'contact_view'
ID_COLUMN_NAME = 'contact_id'
GOOGLE_CONTACT_PEOPLE_API_DATA_SOURCE_TYPE_ID = 10

obj = {
    'component_id': CONTACT_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': CONTACT_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'sahar.g@circ.zone'
}
logger = Logger.create_logger(object=obj)
