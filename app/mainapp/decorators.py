from django.shortcuts import render, redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            elif group is None:
                return render(request, 'pricing.html')
            else:
                return render(request, 'pricing.html')

        return wrapper_func
    return decorator
