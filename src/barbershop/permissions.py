from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)  # Preserva o nome e docstring da função original
    def _wrapped_view(request, *args, **kwargs):
        print(request.user.user_type)
        if request.user.is_authenticated and request.user.user_type == 'ADMIN':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return _wrapped_view
