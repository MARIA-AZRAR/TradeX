from rest_framework import permissions

class isOwnerPermission(permissions.BasePermission):
    """ Return the permission so that only owner can access the watchlist """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user