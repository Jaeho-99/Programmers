# 특정 질문에 대한 수정 권한을 관리하기 위한 파일.

from rest_framework import permissions

# owner이거나 owner가 아니라면 읽기용으로만 접근 가능.
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user