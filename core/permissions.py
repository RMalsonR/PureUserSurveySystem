from rest_framework.permissions import BasePermission

from core.roles import Role


def create_user_permission_class(roles):
    """
    Factory method creates Permission classes
    by user role
    :param roles: list of allowed roles
    :return: permission class
    """
    class _PermissionClass(BasePermission):
        def has_permission(self, request, view):
            return request.user.is_authenticated and request.user.role in roles
    return _PermissionClass


IsAdmin = create_user_permission_class([Role.ADMIN_ROLE.value])
IsSurveyParticipant = create_user_permission_class([Role.SURVEY_PARTICIPANT.value])

