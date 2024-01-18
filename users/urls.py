from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, VerifyForLoginApi, EditCurrrentUserData, \
    VerifyForActivateApi, GenerateNewPassword

urlpatterns = [
    path('register', RegisterView.as_view(), name='create-user'),
    path('login', LoginView.as_view(), name='login-user'),
    path('logout', LogoutView.as_view(), name='logout-user'),
    path('me/', UserView.as_view(), name='get-current-user'),

    path('verify-for-login/<int:code>/', VerifyForLoginApi.as_view(), name='verify-for-login'),
    path('verify-for-activate/<int:code>/', VerifyForActivateApi.as_view(), name='verify-for-activate'),
    path('CurrentUserEdit', EditCurrrentUserData.as_view(), name='edit-current-user-edi'),
    path('generate/password', GenerateNewPassword.as_view(), name='generate-password'),
]
