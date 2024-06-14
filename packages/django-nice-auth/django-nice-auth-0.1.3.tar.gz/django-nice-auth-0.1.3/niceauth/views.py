from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import NiceAuthRequest, NiceAuthResult
from .serializers import (
    NiceAuthRequestReturnUrlSerializer,
    NiceAuthRequestDetailSerializer,
    NiceAuthResultSerializer,
    NiceAuthServiceRequestSerializer,
    NiceAuthServiceResponseSerializer,
)
from nice_auth.services import NiceAuthService
from nice_auth.exceptions import NiceAuthException
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests

class NiceAuthBaseView(APIView):
    @swagger_auto_schema(
        tags=['NICE Authentication'],
        operation_description="Handle NICE authentication data",
        request_body=NiceAuthRequestReturnUrlSerializer,
        responses={
            200: NiceAuthRequestDetailSerializer(many=False),
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def post(self, request):
        return self.handle_request(request)

    @swagger_auto_schema(
        tags=['NICE Authentication'],
        operation_description="Handle NICE authentication data",
        manual_parameters=[
            openapi.Parameter('return_url', openapi.IN_QUERY, description="Return URL", type=openapi.TYPE_STRING),
        ],
        responses={
            200: NiceAuthRequestDetailSerializer(many=False),
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def get(self, request):
        return self.handle_request(request)

    def handle_request(self, request):
        raise NotImplementedError("Subclasses should implement this method")


class GetNiceAuthView(NiceAuthBaseView):
    def handle_request(self, request):
        try:
            return_url = request.GET.get('return_url') if request.method == 'GET' else request.data.get('return_url')
            service = NiceAuthService(
                base_url=settings.NICE_AUTH_BASE_URL,
                client_id=settings.NICE_CLIENT_ID,
                client_secret=settings.NICE_CLIENT_SECRET,
                product_id=settings.NICE_PRODUCT_ID,
                return_url=return_url or settings.NICE_RETURN_URL,
                authtype=settings.NICE_AUTHTYPE,
                popupyn=settings.NICE_POPUPYN
            )
            auth_data = service.get_nice_auth()
            auth_request = NiceAuthRequest.objects.create(
                request_no=auth_data["requestno"],
                enc_data=auth_data["enc_data"],
                integrity_value=auth_data["integrity_value"],
                token_version_id=auth_data["token_version_id"],
                key=auth_data["key"],
                iv=auth_data["iv"],
                return_url=return_url
            )
            serializer = NiceAuthRequestDetailSerializer(auth_request)
            return Response(serializer.data)
        except NiceAuthException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetNiceAuthUrlView(NiceAuthBaseView):
    def handle_request(self, request):
        try:
            return_url = request.GET.get('return_url') if request.method == 'GET' else request.data.get('return_url')
            service = NiceAuthService(
                base_url=settings.NICE_AUTH_BASE_URL,
                client_id=settings.NICE_CLIENT_ID,
                client_secret=settings.NICE_CLIENT_SECRET,
                product_id=settings.NICE_PRODUCT_ID,
                return_url=return_url or settings.NICE_RETURN_URL,
                authtype=settings.NICE_AUTHTYPE,
                popupyn=settings.NICE_POPUPYN
            )
            auth_data = service.get_nice_auth()
            auth_request = NiceAuthRequest.objects.create(
                request_no=auth_data["requestno"],
                enc_data=auth_data["enc_data"],
                integrity_value=auth_data["integrity_value"],
                token_version_id=auth_data["token_version_id"],
                key=auth_data["key"],
                iv=auth_data["iv"],
                return_url=return_url
            )
            nice_url = f"https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb?m=service&token_version_id={auth_data['token_version_id']}&enc_data={auth_data['enc_data']}&integrity_value={auth_data['integrity_value']}"
            return Response({'nice_auth_url': nice_url})
        except NiceAuthException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyNiceAuthView(APIView):
    @swagger_auto_schema(
        tags=['NICE Authentication'],
        operation_description="Verify NICE authentication result",
        request_body=NiceAuthRequestDetailSerializer,
        responses={
            200: NiceAuthResultSerializer(many=False),
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def post(self, request):
        return self.handle_request(request)

    @swagger_auto_schema(
        tags=['NICE Authentication'],
        operation_description="Verify NICE authentication result",
        manual_parameters=[
            openapi.Parameter('enc_data', openapi.IN_QUERY, description="Encrypted Data", type=openapi.TYPE_STRING),
            openapi.Parameter('token_version_id', openapi.IN_QUERY, description="Token Version ID", type=openapi.TYPE_STRING),
            openapi.Parameter('integrity_value', openapi.IN_QUERY, description="Integrity Value", type=openapi.TYPE_STRING),
        ],
        responses={
            200: NiceAuthResultSerializer(many=False),
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def get(self, request):
        return self.handle_request(request)

    def handle_request(self, request):
        try:
            data = request.GET if request.method == 'GET' else request.data
            enc_data = data.get('enc_data')
            token_version_id = data.get('token_version_id')
            integrity_value = data.get('integrity_value')

            auth_request = get_object_or_404(NiceAuthRequest, token_version_id=token_version_id, integrity_value=integrity_value)
            key = auth_request.key
            iv = auth_request.iv

            service = NiceAuthService(
                base_url=settings.NICE_AUTH_BASE_URL,
                client_id=settings.NICE_CLIENT_ID,
                client_secret=settings.NICE_CLIENT_SECRET,
                product_id=settings.NICE_PRODUCT_ID,
                return_url=auth_request.return_url,
                authtype=settings.NICE_AUTHTYPE,
                popupyn=settings.NICE_POPUPYN
            )

            result_data = service.verify_auth_result(enc_data, key, iv)
            auth_result = NiceAuthResult.objects.create(
                request=auth_request,
                result=result_data
            )
            serializer = NiceAuthResultSerializer(auth_result)
            return Response(serializer.data)
        except NiceAuthException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CallNiceAuthView(APIView):
    @swagger_auto_schema(
        tags=['NICE Authentication'],
        operation_description="Call NICE authentication service",
        request_body=NiceAuthServiceRequestSerializer,
        responses={
            200: NiceAuthServiceResponseSerializer,
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def post(self, request):
        serializer = NiceAuthServiceRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response = requests.post(
                "https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb",
                data={
                    "m": "service",
                    "token_version_id": data["token_version_id"],
                    "enc_data": data["enc_data"],
                    "integrity_value": data["integrity_value"]
                }
            )
            if response.status_code == 200:
                # HTML 응답을 텍스트로 처리
                response_data = response.text
                return Response({'html_content': response_data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to call NICE service'}, status=response.status_code)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
