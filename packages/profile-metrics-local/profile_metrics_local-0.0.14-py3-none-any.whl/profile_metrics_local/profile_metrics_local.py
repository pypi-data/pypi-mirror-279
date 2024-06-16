from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger

# TODO: move to constants
PROFILE_METRICS_LOCAL_COMPONENT_ID = 233
PROFILE_METRICS_LOCAL_COMPONENT_NAME = "profile metrics local"
DEVELOPER_EMAIL = "tal.g@circ.zone"
object_for_logger_code = {
    'component_id': PROFILE_METRICS_LOCAL_COMPONENT_ID,
    'component_name': PROFILE_METRICS_LOCAL_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}


class ProfileMetricsLocal(GenericCRUD, metaclass=MetaLogger, object=object_for_logger_code):

    def __init__(self):
        super().__init__(default_schema_name="profile_metrics",
                         default_table_name="profile_metrics_table",
                         default_view_table_name="profile_metrics_view",
                         default_column_name="profile_metrics_id")

    def insert_by_ids(self, *, profile_id: int, profile_metrics_type: int, value: int) -> int:
        profile_metrics_id = self.insert(
            data_dict={'profile_id': profile_id, 'profile_metrics_type': profile_metrics_type, 'value': value})
        return profile_metrics_id

    def insert(self, data_dict: dict[str, int]) -> int:
        profile_metrics_id = super().insert(data_dict=data_dict)
        return profile_metrics_id

    def update(self, profile_metrics_id: int, profile_id: int, profile_metrics_type: int, value: int) -> int:
        data_dict = {'profile_id': profile_id, 'profile_metrics_type': profile_metrics_type, 'value': value}
        profile_metrics_id = self.update_by_column_and_value(column_value=profile_metrics_id, data_dict=data_dict)
        return profile_metrics_id

    def delete_by_id(self, profile_metrics_id: int) -> int:
        deleted_rows = super().delete_by_column_and_value(column_value=profile_metrics_id)
        return deleted_rows

    def select_one_dict_by_id(self, profile_metrics_id: int) -> dict[str, int]:
        select_clause_value = 'profile_id, profile_metrics_type, value'
        profile_metrics_dict = super().select_one_dict_by_column_and_value(
            select_clause_value=select_clause_value,
            column_value=profile_metrics_id)
        return profile_metrics_dict
