from django.urls import path
from .views import GetNiceAuthView, GetNiceAuthUrlView, VerifyNiceAuthView, CallNiceAuthView

urlpatterns = [
    path('', GetNiceAuthView.as_view(), name='get_nice_auth_data'),
    path('url/', GetNiceAuthUrlView.as_view(), name='get_nice_auth_url'),
    path('verify/', VerifyNiceAuthView.as_view(), name='verify_nice_auth'),
    path('call/', CallNiceAuthView.as_view(), name='call_nice_service'),
]
