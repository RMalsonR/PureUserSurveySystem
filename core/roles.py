from enum import Enum


class Role(Enum):
    ADMIN_ROLE = 'ADMIN_ROLE'
    SURVEY_PARTICIPANT = 'SURVEY_PARTICIPANT'

    @classmethod
    def as_choices(cls):
        return (
            (cls.ADMIN_ROLE.value, 'Администратор'),
            (cls.SURVEY_PARTICIPANT.value, 'Участник опроса'),
        )
