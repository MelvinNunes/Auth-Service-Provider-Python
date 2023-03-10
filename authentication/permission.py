from django.contrib.auth.models import Group
from rest_framework import permissions


def _is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        g = Group.objects.get(name=group_name)
        for user in user.groups.all():
            if user == g:
                return True
    except Group.DoesNotExist:
        return None


def _has_group_permission(user, required_groups):
    return any([_is_in_group(user, group_name) for group_name in required_groups])


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['admin']

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(
            request.user, self.required_groups)
        if self.required_groups is None:
            return False
        return obj == request.user or has_group_permission


class IsAdminUser(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['admin']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(
            request.user, self.required_groups)
        return request.user and has_group_permission

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(
            request.user, self.required_groups)
        return request.user and has_group_permission


class IsAdminOrClientUser(permissions.BasePermission):
    required_groups = ['admin', 'client']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(
            request.user, self.required_groups)
        return request.user and has_group_permission


class IsAdminOrSeguradoraUser(permissions.BasePermission):
    required_groups = ['admin', 'seguradora_admin']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(
            request.user, self.required_groups)
        return request.user and has_group_permission


class IsAdminOrSeguradoraOrDelegacaoUser(permissions.BasePermission):
    required_groups = ['admin', 'delegacao_admin', 'seguradora_admin']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(
            request.user, self.required_groups)
        return request.user and has_group_permission


class IsEmployee(permissions.BasePermission):
    required_groups = ['admin', 'delegacao_admin',
                       'seguradora_admin', 'delegacao_employee']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(
            request.user, self.required_groups)
        return request.user and has_group_permission


class IsAllEssentials(permissions.BasePermission):
    required_groups = ['admin', 'delegacao_admin',
                       'seguradora_admin', 'client', 'delegacao_employee']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(
            request.user, self.required_groups)
        return request.user and has_group_permission
