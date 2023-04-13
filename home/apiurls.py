from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_view
from . import api

urlpatterns = [
    # Auth APIs
    path('signup_api/', api.SignupApiView.as_view(), name='signup-api'),
    path('login_api/', api.LoginApiView.as_view(), name='login-api'),
    path('reset-password/', api.ResetPasswordApiView.as_view(), name='reset-password-api'),
    # path('user-forgot-password/', api.ForgotPasswordApiView.as_view(), name='forgot-password-api'),
    path('addclient_api/', api.AddClientApiView.as_view(), name='addclient-api'),
    path('clientdetail-api/', api.GetClientAPiView.as_view(),name='get-client-api'),
    path('clientdocument-api/', api.ClientDocumentApiView.as_view(),name='client-document-api'),
    path('document-client-api/', api.GetDocumentAPiView.as_view(),name='get-client-document-api'),
    path('user-forgot-password/', api.ForgotPasswordApiView.as_view(),name='forgot-password-api'),
    path('user-verify-email/', api.VerifyEmailApiView.as_view(), name='verify-email'),
    path('user-reset-password/', api.ForgotResetPasswordApiView.as_view(),name='forgot-reset-password-api'),
    path('edit_profile_api/<int:id>/', api.EditClientApiView.as_view(), name='edit-profile-api'),
]


