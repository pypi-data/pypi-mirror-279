from rest_framework import serializers
from .models import NiceAuthRequest, NiceAuthResult

# Serializer for NiceAuthRequest including return_url, redirect_url, authtype, and popupyn
class NiceAuthRequestReturnUrlSerializer(serializers.ModelSerializer):
    """
    Serializer for handling NiceAuthRequest return URL, redirect URL, authtype, and popupyn.
    """
    class Meta:
        model = NiceAuthRequest
        fields = ['return_url', 'redirect_url', 'authtype', 'popupyn']  # Added authtype and popupyn fields


class NiceAuthRequestDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed NiceAuthRequest information.
    """
    class Meta:
        model = NiceAuthRequest
        fields = [
            'request_no',
            'enc_data',
            'integrity_value',
            'token_version_id',
            'return_url',
            'redirect_url',
            'authtype',
            'popupyn'
        ]


class NiceAuthResultSerializer(serializers.ModelSerializer):
    """
    Serializer for handling NiceAuthResult data.
    """
    class Meta:
        model = NiceAuthResult
        fields = ['request', 'result', 'request_no', 'enc_data', 'is_verified']


class VerifyNiceAuthSerializer(serializers.ModelSerializer):
    """
    Serializer for verifying NICE authentication result.
    """
    class Meta:
        model = NiceAuthRequest
        fields = ['enc_data', 'token_version_id', 'integrity_value']
