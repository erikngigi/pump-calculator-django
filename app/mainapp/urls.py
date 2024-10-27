from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("pricing/", views.pricing, name="pricing"),
    
    # user authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("profile/", views.profile_view, name="profile"),
    path("accountexpired/", views.account_expired, name="account_expired"),
    path('select-package/', views.select_package, name='select_package'),
    path('contact/', views.contact_view, name='contact'),
    # password reset stuff
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="reset/password_reset.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="reset/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
    template_name='reset/password_reset_complete.html'), name='password_reset_complete'),
    path("calculator/", views.trade_calculations_view, name="calculator"),
    path("calculator/", views.home_view, name="calculator"),
    path( "tables/", views.trade_calculations_view, name="tables"),
]
