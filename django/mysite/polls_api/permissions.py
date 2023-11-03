from rest_framework import permissions

# owner이거나 owner가 아니라면 읽기용으로만 접근 가능.
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user
    
class IsVoter(permissions.BasePermission):
    # 오직 해당 유저가 voter인 경우에만 가능하도록 권한 부여
    def has_object_permission(self, request, view, obj):
        return obj.voter == request.user