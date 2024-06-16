from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger

# TODO: move to constants
PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 190
PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = "profile_profile_local"
DEVELOPER_EMAIL = "idan.a@circ.zone"
SCHEMA_NAME = "profile_profile"
PROFILE_PROFILE_TABLE_NAME = "profile_profile_table"
PROFILE_PROFILE_VIEW_TABLE_NAME = "profile_profile_view"
PROFILE_PROFILE_ID_COLUMN_NAME = "profile_profile_id"
LOGGER_CODE_OBJECT = {
    'component_id': PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': PROFILE_PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}


class ProfileProfile(GenericCRUD, metaclass=MetaLogger, object=LOGGER_CODE_OBJECT):
    def __init__(self) -> None:
        super().__init__(default_schema_name=SCHEMA_NAME, default_table_name=PROFILE_PROFILE_TABLE_NAME,
                         default_view_table_name=PROFILE_PROFILE_VIEW_TABLE_NAME,
                         default_column_name=PROFILE_PROFILE_ID_COLUMN_NAME)

    def insert_profile_profile(self, profile_id1: int, profile_id2: int, relationship_type_id: int,
                               job_title: str = None, is_test_data: bool = False) -> int:
        data_dict = {
            'profile_id1': profile_id1,
            'profile_id2': profile_id2,
            'relationship_type_id': relationship_type_id,
            'job_title': f"'{job_title}'",
            'is_test_data': is_test_data
        }
        profile_profile_id = self.insert(data_dict=data_dict)
        return profile_profile_id

    def update_profile_profile_by_profile_profile_id(self, profile_profile_id: int, profile_profile_dict: dict) -> int:
        affected_rows = self.update_by_column_and_value(data_dict=profile_profile_dict, column_value=profile_profile_id)
        return affected_rows

    def delete_by_profile_profile_id(self, profile_profile_id: int) -> int:
        affected_rows = self.delete_by_column_and_value(column_value=profile_profile_id)
        return affected_rows

    def get_dicts_by_profile_profile_id(self, profile_profile_id: int) -> list[dict]:
        profile_profile_record = self.select_multi_dict_by_column_and_value(
            column_value=profile_profile_id)
        return profile_profile_record
