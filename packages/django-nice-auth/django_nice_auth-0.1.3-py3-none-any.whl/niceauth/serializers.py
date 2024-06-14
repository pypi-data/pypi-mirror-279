from rest_framework import serializers
from .models import NiceAuthRequest, NiceAuthResult


class NiceAuthRequestReturnUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = NiceAuthRequest
        fields = ['return_url']


class NiceAuthRequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NiceAuthRequest
        fields = ['request_no', 'enc_data', 'integrity_value', 'token_version_id']


class NiceAuthResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = NiceAuthResult
        fields = ['request', 'result']


class NiceAuthServiceRequestSerializer(serializers.Serializer):
    token_version_id = serializers.CharField(max_length=100)
    enc_data = serializers.CharField()
    integrity_value = serializers.CharField()


class NiceAuthServiceResponseSerializer(serializers.Serializer):
    token_version_id = serializers.CharField(max_length=100)
    enc_data = serializers.CharField()
    integrity_value = serializers.CharField()
