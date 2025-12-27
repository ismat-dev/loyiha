from rest_framework.permissions import BasePermission

class IsTeacher(BasePermission):
    """
    Teacher can create test
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "teacher":
            return True
        return False

class IsStudent(BasePermission):
    """
    Docstring for IsStudent
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "student":
            return True
        return False
    