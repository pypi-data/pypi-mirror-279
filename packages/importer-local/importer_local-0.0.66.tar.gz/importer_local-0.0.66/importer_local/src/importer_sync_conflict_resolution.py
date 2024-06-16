from enum import Enum
from datetime import datetime
from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger


IMPORTER_LOCAL_PYTHON_COMPONENT_ID = 114
IMPORTER_LOCAL_PYTHON_COMPONENT_NAME = 'importer-local-python-package'

logger_code_init = {
    'component_id': IMPORTER_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': IMPORTER_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'tal.g@circlez.ai'
}
logger = Logger.create_logger(object=logger_code_init)


class UpdateStatus(Enum):
    UPDATE_DATA_SOURCE = -1
    DONT_UPDATE = 0
    UPDATE_CIRCLEZ = 1


class ImporterSyncConflictResolution(GenericCRUD):
    def __init__(self):
        GenericCRUD.__init__(self, default_schema_name="importer", default_table_name="importer_table",
                             default_view_table_name="importer_view",
                             default_column_name="importer_id")

    # last_modified_timestamp is the last time the entity was modified in the data source
    def get_update_status(self, last_modified_timestamp: str, data_source_instance_id: int,
                          entity_type_id: int,
                          entity_id: int) -> UpdateStatus:
        updated_timestamp = self.select_one_value_by_where(
            select_clause_value="updated_timestamp",
            where="data_source_instance_id = %s AND entity_type_id = %s AND entity_id = %s",
            params=(data_source_instance_id, entity_type_id, entity_id)
        )
        # Convert the timestamps to datetime objects
        last_modified_timestamp: datetime = datetime.strptime(last_modified_timestamp, '%Y-%m-%d %H:%M:%S')
        if updated_timestamp is None or last_modified_timestamp > updated_timestamp:
            return UpdateStatus.UPDATE_CIRCLEZ
        elif last_modified_timestamp < updated_timestamp:
            return UpdateStatus.UPDATE_DATA_SOURCE
        else:
            return UpdateStatus.DONT_UPDATE
