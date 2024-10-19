from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

def allowed_users(allowed_roles=[], redirect_url='pricing'):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(reverse(redirect_url))  # Use reverse for URL resolution

        return wrapper_func
    return decorator

def check_expiration(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        signup_date = user.date_joined
        countdown_end = signup_date + timezone.timedelta(days=30)  # Change this as needed
        remaining_time = countdown_end - timezone.now()

        # Check if the countdown has expired
        countdown_expired = remaining_time.total_seconds() <= 0

        if countdown_expired:
            # Redirect to an 'account_expired' page if the account is expired
            return redirect('account_expired')
        
        # Proceed with the view if the account is still active
        return view_func(request, *args, **kwargs)

    return wrapper_func
