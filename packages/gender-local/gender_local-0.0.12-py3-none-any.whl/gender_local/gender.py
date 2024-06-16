from database_mysql_local.generic_crud import GenericCRUD
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger

from .constants_gender_local import ConstantsGenderLocal


class Gender(GenericCRUD, metaclass=MetaLogger, object=ConstantsGenderLocal.OBJECT_FOR_LOGGER_CODE):
    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name="gender",
                         default_table_name="gender_table",
                         default_view_table_name="gender_view",
                         default_column_name="gender_id",
                         is_test_data=is_test_data)

    def get_gender_id_by_title(self, title: str) -> int or None:
        return self.select_one_dict_by_column_and_value(select_clause_value="gender_id",
                                                        view_table_name="gender_ml_view",
                                                        column_name="title",
                                                        column_value=title).get("gender_id")

    def insert_gender(self, name: str, title: str, lang_code: LangCode, is_test_data: bool = False) -> int:
        # TODO Use GenericCrudMl
        gender_id = super().insert(data_dict={"name": name, "is_test_data": is_test_data})
        super().insert(table_name="gender_ml_table", data_dict={
            "gender_id": gender_id, "lang_code": lang_code.value, "title": title})
        return gender_id

    def get_test_gender_id(self):
        return 1  # TODO: implement
