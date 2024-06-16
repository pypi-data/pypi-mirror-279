from datetime import date

from database_mysql_local.generic_crud import GenericCRUD
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger
from python_sdk_remote.utilities import is_valid_date_range

from .constants_location_profile import LocationProfileLocalConstants


class LocationProfile:
    def __init__(self, location_id, profile_id):
        self.profile_id = profile_id
        self.location_id = location_id

    def __dict__(self):
        return {
            'profile_id': self.profile_id,
            'location_id': self.location_id
        }


class LocationProfilesLocal(GenericCRUD, metaclass=MetaLogger,
                            object=LocationProfileLocalConstants.OBJECT_FOR_LOGGER_CODE):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name="location_profile", is_test_data=is_test_data)

    def get_last_location_id_by_profile_id(self, profile_id: int) -> int:
        location_id = self.select_one_value_by_column_and_value(
            view_table_name="location_profile_view", select_clause_value="location_id",
            column_name="profile_id", column_value=profile_id,
            order_by="start_timestamp desc")
        if location_id is not None:
            return location_id
        else:
            self.logger.warning("No location_id found for profile_id = " + str(profile_id))

    def get_location_ids_by_profile_id(self, profile_id: int, limit: int = 1,
                                       datetime_range: (date, date) = None) -> list[LocationProfile]:
        if datetime_range is None:
            where_clause = f"profile_id = {profile_id}"
        else:
            if is_valid_date_range(datetime_range):
                if datetime_range[0] > datetime_range[1]:
                    datetime_range = (datetime_range[1], datetime_range[0])
                date1: date = datetime_range[0].strftime('%Y-%m-%d')
                date2: date = datetime_range[1].strftime('%Y-%m-%d')
                where_clause = f"profile_id = {profile_id} AND updated_timestamp BETWEEN " \
                               f"'{date1} 00:00:00' AND '{date2} 23:59:59'"
            else:
                raise ValueError(
                    "Invalid time_range format. It should be 'YYYY-MM-DD'.")

        location_ids = self.select_multi_tuple_by_where(
            view_table_name="location_profile_view",
            select_clause_value="location_id", where=where_clause,
            limit=limit, order_by="updated_timestamp DESC")

        location_ids = [LocationProfile(
            location_id=location_id, profile_id=profile_id) for location_id in location_ids]
        return location_ids

    # TODO: use crud ml?
    def insert_location_profile(self, *, profile_id: int, location_id: int,
                                title: str, lang_code: LangCode = LangCode.ENGLISH) -> tuple:
        data_dict = {
            "profile_id": profile_id,
            "location_id": location_id
        }
        location_profile_id = self.insert(
            table_name="location_profile_table", data_dict=data_dict)
        data_dict = {
            "location_profile_id": location_profile_id,
            "lang_code": lang_code.value,
            "title": title,
            "title_approved": False
        }
        location_profile_ml_id = self.insert(
            table_name="location_profile_ml_table", data_dict=data_dict)
        return location_profile_id, location_profile_ml_id
