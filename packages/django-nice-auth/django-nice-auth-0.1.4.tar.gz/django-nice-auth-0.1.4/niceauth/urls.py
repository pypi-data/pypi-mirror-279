from django.urls import path
from .views import GetNiceAuthDataView, GetNiceAuthUrlView, VerifyNiceAuthView, NiceAuthRequestRetrieveView, NiceAuthResultRetrieveView

urlpatterns = [
    path('data/', GetNiceAuthDataView.as_view(), name='get_nice_auth_data'),
    path('url/', GetNiceAuthUrlView.as_view(), name='get_nice_auth_url'),
    path('verify/', VerifyNiceAuthView.as_view(), name='verify_nice_auth'),
    path('request/<uuid:request_no>/', NiceAuthRequestRetrieveView.as_view(), name='retrieve_nice_auth_request'),
    path('result/<uuid:request_no>/', NiceAuthResultRetrieveView.as_view(), name='retrieve_nice_auth_result'),
]
