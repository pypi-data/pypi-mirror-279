from typing import List

from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger

from .constants_profile_reaction import (
    OBJECT_TO_INSERT_CODE, PROFILE_REACTION_DATABASE_NAME, PROFILE_REACTION_TABLE_NAME, PROFILE_REACTION_VIEW_NAME,
    PROFILE_REACTION_ID_COLUMN_NAME)
from .profile_reaction_dto import ProfileReactionDto

ERROR_MESSAGE_FAILED_INSERT = 'error: Failed to insert profile_reaction'
ERROR_MESSAGE_FAILED_READ = 'error: Failed to read profile_reaction'
ERROR_MESSAGE_FAILED_UPDATE = 'error: Failed to update profile_reaction'
ERROR_MESSAGE_FAILED_DELETE = 'error: Failed to delete profile_reaction'


# TODO: create assert functions
# TODO: add tests
class ProfileReactions(GenericCRUD, metaclass=MetaLogger, object=OBJECT_TO_INSERT_CODE):
    """ProfileReaction class provides methods for all the CRUD operations to the profile_reaction db"""

    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name=PROFILE_REACTION_DATABASE_NAME,
                         default_table_name=PROFILE_REACTION_TABLE_NAME,
                         default_view_table_name=PROFILE_REACTION_VIEW_NAME,
                         default_column_name=PROFILE_REACTION_ID_COLUMN_NAME,
                         is_test_data=is_test_data)

    def insert(self, reaction_id: int, profile_id: int) -> int:
        data_dict = {'reaction_id': reaction_id, 'profile_id': profile_id}
        assert not (reaction_id is None or profile_id is None or reaction_id <= 0 or profile_id <= 0)
        profile_reaction_id = super().insert(data_dict=data_dict)
        return profile_reaction_id

    def insert_with_dto(self, profile_reaction_dto: ProfileReactionDto) -> int:
        data_dict = profile_reaction_dto.get_arguments()
        assert not (profile_reaction_dto.get('reaction_id') is None or profile_reaction_dto.get('profile_id') is None or
                    profile_reaction_dto.get('reaction_id') <= 0 or profile_reaction_dto.get('profile_id') <= 0)
        profile_reaction_id = super().insert(data_dict=data_dict)
        return profile_reaction_id

    def select_reaction_id_profile_id_by_profile_reaction_id(self, profile_reaction_id: int) -> dict:
        assert profile_reaction_id is not None and profile_reaction_id > 0
        result = self.select_one_dict_by_column_and_value(column_value=profile_reaction_id,
                                            select_clause_value="reaction_id, profile_id")
        return result

    def select_dtos_by_profile_reaction_id(self, profile_reaction_id: int) -> List[ProfileReactionDto]:
        assert profile_reaction_id is not None and profile_reaction_id > 0
        results = self.select_multi_dict_by_column_and_value(column_value=profile_reaction_id,
                                               select_clause_value="profile_id, reaction_id")

        list_profile_reaction_dto = []
        for result in results:
            profile_reaction_dto = ProfileReactionDto(profile_id=result["profile_id"],
                                                      reaction_id=result["reaction_id"])
            list_profile_reaction_dto.append(profile_reaction_dto)
        return list_profile_reaction_dto

    def select_all_by_profile_id(self, profile_id: int) -> list[dict]:
        assert profile_id is not None and profile_id > 0
        result = self.select_multi_dict_by_column_and_value(column_value=profile_id,
                                              column_name="profile_id",
                                              select_clause_value="profile_reaction_id, reaction_id")
        return result

    def select_all_profile_reaction_id_profile_id_by_reaction_id(self, reaction_id: int) -> list[dict]:
        assert reaction_id is not None and reaction_id > 0
        result = self.select_multi_dict_by_column_and_value(column_value=reaction_id,
                                              column_name="reaction_id",
                                              select_clause_value="profile_reaction_id, profile_id")
        return result

    def update(self, profile_reaction_id: int, reaction_id: int, profile_id: int) -> None:
        assert profile_reaction_id is not None and profile_reaction_id > 0
        assert reaction_id is not None and reaction_id > 0
        assert profile_id is not None and profile_id > 0
        super().update_by_column_and_value(data_dict={'profile_id': profile_id, 'reaction_id': reaction_id},
                             column_value=profile_reaction_id)

    def delete_by_profile_reaction_id(self, profile_reaction_id: int) -> None:
        assert profile_reaction_id is not None and profile_reaction_id > 0
        super().delete_by_column_and_value(column_value=profile_reaction_id)
