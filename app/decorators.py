from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

#   Generic permission check. This decorator will work with all permissions to check if user
#   has valid rank
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

#   Expressed by @admin_required decorator in views.py
def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

#   Expressed by @instructor_required
def instructor_required(f):
    return permission_required(Permission.MANAGE_CLASSES)(f)
