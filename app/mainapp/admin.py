# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

# Get the custom user model (or default User model)
User = get_user_model()

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'date_joined', 
        'time_remaining',  # Add the new field for remaining time
        'is_staff'
    )
    
    actions = [
        'reset_expiration_time_by_29_days',
        'reset_expiration_time_by_23_hours',
        'reset_expiration_time_by_60_minutes',
        'reset_expiration_time_by_45_minutes',
        'reset_expiration_time_by_30_minutes',
        'reset_expiration_time_by_15_minutes',
        'reset_expiration_time_by_5_minutes',
    ]  # Add the custom actions to the admin

    # Method to calculate the remaining time
    def time_remaining(self, obj):
        remaining_time = timedelta(days=30) - (timezone.now() - obj.date_joined)
        if remaining_time.total_seconds() > 0:
            return str(remaining_time).split('.')[0]  # Format as "HH:MM:SS"
        return "Expired"  # Or you can return any other message indicating expiration

    time_remaining.short_description = 'Time Remaining'  # Column header in admin

    # Reset expiration time by 29 days
    def reset_expiration_time_by_29_days(self, request, queryset):
        for user in queryset:
            user.date_joined = timezone.now() - timedelta(days=29)
            user.save()
            messages.success(request, f'Expiration time reset for {user.username} by 29 days.')

    reset_expiration_time_by_29_days.short_description = "Reset Expiration Time to 24 Hours"

    # Reset expiration time by 60 minutes
    def reset_expiration_time_by_60_minutes(self, request, queryset):
        for user in queryset:
            user.date_joined = timezone.now() - timedelta(days=29, hours=23)
            user.save()
            messages.success(request, f'Expiration time reset for {user.username} by 60 minutes.')

    reset_expiration_time_by_60_minutes.short_description = "Reset Expiration Time to 1 Hour"
    
    # Reset expiration time by 45 minutes
    def reset_expiration_time_by_45_minutes(self, request, queryset):
        for user in queryset:
            user.date_joined = timezone.now() - timedelta(days=29, hours=23, minutes=15)
            user.save()
            messages.success(request, f'Expiration time reset for {user.username} to 45 minutes.')

    reset_expiration_time_by_45_minutes.short_description = "Reset Expiration Time to 45 Minutes"

    # Reset expiration time to 30 minutes
    def reset_expiration_time_by_30_minutes(self, request, queryset):
        for user in queryset:
            user.date_joined = timezone.now() - timedelta(days=29, hours=23, minutes=30)
            user.save()
            messages.success(request, f'Expiration time reset for {user.username} to 30 minutes.')

    reset_expiration_time_by_30_minutes.short_description = "Reset Expiration Time to 30 Minutes"

    # Reset expiration time to 15 minutes
    def reset_expiration_time_by_15_minutes(self, request, queryset):
        for user in queryset:
            user.date_joined = timezone.now() - timedelta(days=29, hours=23, minutes=45)
            user.save()
            messages.success(request, f'Expiration time reset for {user.username} to 15 minutes.')

    reset_expiration_time_by_15_minutes.short_description = "Reset Expiration Time to 15 Minutes"

    # Reset expiration time to 5 minutes
    def reset_expiration_time_by_5_minutes(self, request, queryset):
        for user in queryset:
            user.date_joined = timezone.now() - timedelta(days=29, hours=23, minutes=55)
            user.save()
            messages.success(request, f'Expiration time reset for {user.username} to 5 minutes.')

    reset_expiration_time_by_5_minutes.short_description = "Reset Expiration Time to 5 Minutes"

# Unregister the default UserAdmin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
