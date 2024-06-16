import datetime
from typing import List, Dict, Tuple

from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger

# TODO: move to constants
OPERATIONAL_HOURS_LOCAL_COMPONENT_ID = 158
OPERATIONAL_HOURS_LOCAL_COMPONENT_NAME = 'operational_hours_local/src/operational_hours.py'

logger_code_object = {
    'component_id': OPERATIONAL_HOURS_LOCAL_COMPONENT_ID,
    'component_name': OPERATIONAL_HOURS_LOCAL_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'tal.g@circ.zone'
}


# OperationalHours class provides methods for all the CRUD operations to the operational_hours db


class OperationalHours(GenericCRUD, metaclass=MetaLogger, object=logger_code_object):
    def __init__(self):
        super().__init__(default_schema_name="operational_hours",
                         default_column_name="operational_hours_id",
                         default_table_name="operational_hours_table",
                         default_view_table_name="operational_hours_view")

    # location_id is optional
    def insert(self, profile_id: int, location_id: int, hours: List[Dict[str, int]]):  # noqa
        for day_of_week, day in enumerate(hours):
            super().insert(data_dict={"profile_id": profile_id, "location_id": location_id, "day_of_week": day_of_week,
                                      "from_time": day["from_time"], "until_time": day["until_time"]})
            self.logger.info("executed query insert")

        operational_hours_ids = self.get_operational_hours_ids_list_by_profile_id_location_id(
            profile_id, location_id)

        return operational_hours_ids

    # location_id is optional
    def update(self, profile_id: int, location_id: int or None, hours: List[Dict[str, int]]):

        operational_hours_ids = self.get_operational_hours_ids_list_by_profile_id_location_id(
            profile_id)

        for day_of_week, day in enumerate(hours):
            operational_hours_id = operational_hours_ids[day_of_week]
            data_dict = {"day_of_week": day_of_week, "from_time": day["from_time"],
                         "until_time": day["until_time"]}
            if location_id is not None:
                data_dict["location_id"] = location_id
            super().update_by_column_and_value(data_dict=data_dict, column_value=operational_hours_id)

    def get_operational_hours_list_by_profile_id_location_id(self, profile_id: int, location_id: int = None) -> List[
        Tuple[int, int, datetime.timedelta, datetime.timedelta]]:
        where = "profile_id = %s"
        params = (profile_id,)
        if location_id is not None:
            where += " AND location_id = %s"
            params += (location_id,)
        select_clause_value = "operational_hours_id, day_of_week, from_time, until_time"
        operational_hours_list = super().select_multi_tuple_by_where(select_clause_value=select_clause_value,
                                                                     where=where, params=params)

        # operational_hours_json = self._operational_hours_to_json(operational_hours_list)

        return operational_hours_list

    # One profile can have different operational_hours in different locations
    def delete_all_operational_hours_by_profile_id_location_id(self, profile_id: int, location_id: int = None) -> None:
        where = "profile_id = %s"
        params = (profile_id,)
        if location_id is not None:
            where += " AND location_id = %s"
            params += (location_id,)

        super().delete_by_where(where=where, params=params)

    def get_operational_hours_id_by_profile_id_location_id(self, profile_id: int, location_id: int = None) -> int:
        where = "profile_id = %s"
        params = (profile_id,)
        if location_id is not None:
            where += " AND location_id = %s"
            params += (location_id,)
        operational_hours_id = self.select_one_value_by_where(select_clause_value="operational_hours_id",
                                                              where=where, params=params)

        return operational_hours_id

    def get_operational_hours_ids_list_by_profile_id_location_id(
            self, profile_id: int, location_id: int = None) -> List[int]:
        where = "profile_id = %s"
        params = (profile_id,)
        if location_id is not None:
            where += " AND location_id = %s"
            params += (location_id,)
        rows = self.select_multi_tuple_by_where(
            select_clause_value="operational_hours_id", where=where, params=params)

        operational_hours_ids = [row[0] for row in rows]

        return operational_hours_ids

    '''
  There may be a problem, if for example there's hour1 = {"day_of_week" : 2, "from": 8:00, "until": 12:00} and hour2 = {"day_of_week": 2, "from": 15:00, "until": 20:00}
  (A business closed between 12:00 and 15:00) then hour2 will override hour1 in operational_hours = {}.
  '''

    @staticmethod
    def generate_hours_list(days_collection: List[Dict[str, int]]) -> List[Dict[str, int]]:
        operational_hours = []
        for day in days_collection:
            day_of_week = day.get("day_of_week")
            element_to_insert = {
                "from_time": day.get("from_time"),
                "until_time": day.get("until_time")
            }
            operational_hours.insert(int(day_of_week), element_to_insert)

        return operational_hours
