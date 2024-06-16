from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger
from user_context_remote.user_context import UserContext
from location_local.locations_local_crud import LocationsLocal

IMPORTER_LOCAL_PYTHON_COMPONENT_ID = 114
IMPORTER_LOCAL_PYTHON_COMPONENT_NAME = 'importer-local-python-package'

logger_code_init = {
    'component_id': IMPORTER_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': IMPORTER_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'idan.a@circlez.ai'
}


class ImportersLocal(GenericCRUD, metaclass=MetaLogger, object=logger_code_init):
    def __init__(self):
        super().__init__(default_schema_name="importer", default_table_name="importer_table",
                         default_view_table_name="importer_view", default_column_name="importer_id")
        self.user_context = UserContext()
        self.locations_local = LocationsLocal()

    def insert(self, *,  # noqa
               data_source_instance_id: int, data_source_type_id: int, location_id: int,
               entity_type_id: int, entity_id: int, url: str,
               user_external_id: int, google_people_api_resource_name: str = None) -> int:
        # TODO Can we have data type for url which is not str?
        country_id = self.locations_local.read(location_id=location_id).get('country_id')
        # TODO importer_dict
        data_dict = {
            'data_source_instance_id': data_source_instance_id,
            'data_source_type_id_old': data_source_type_id,
            "user_external_country_id_old": country_id,
            "entity_type_id": entity_type_id,
            "entity_id": entity_id,
            "url": url,
            "created_user_id": self.user_context.get_effective_user_id(),
            "user_external_id": user_external_id,
            "google_people_api_resource_name": google_people_api_resource_name
        }
        importer_id = super().insert(data_dict=data_dict)
        return importer_id

