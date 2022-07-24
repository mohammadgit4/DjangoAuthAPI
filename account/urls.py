from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, SendEmailResetPasswordView, ResetPasswordView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='URV'),
    path('login/', UserLoginView.as_view(), name='ULV'),
    path('profile/', UserProfileView.as_view(), name='UPV'),
    path('ucpv/', UserChangePasswordView.as_view(), name='UCPV'),
    path('serpv/', SendEmailResetPasswordView.as_view(), name='SERPV'),
    path('rpv/<uid>/<token>/', ResetPasswordView.as_view(), name='RPV')
]