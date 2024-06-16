from django.conf import settings
from drf_yasg import openapi
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import NiceAuthRequest, NiceAuthResult
from .serializers import (
    NiceAuthRequestReturnUrlSerializer,
    NiceAuthRequestDetailSerializer,
    NiceAuthResultSerializer, VerifyNiceAuthSerializer,
)
from nice_auth.services import NiceAuthService
from nice_auth.exceptions import NiceAuthException
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponseRedirect
import uuid

def create_nice_auth_request(data):
    return NiceAuthRequest.objects.create(
        enc_data=data["enc_data"],
        integrity_value=data["integrity_value"],
        token_version_id=data["token_version_id"],
        key=data["key"],
        iv=data["iv"],
        return_url=data.get('return_url'),
        redirect_url=data.get('redirect_url'),
        authtype=data.get('authtype'),
        popupyn=data.get('popupyn')
    )

def handle_get_or_post_request(request):
    return {
        'return_url': request.GET.get('return_url') if request.method == 'GET' else request.data.get('return_url'),
        'redirect_url': request.GET.get('redirect_url') if request.method == 'GET' else request.data.get('redirect_url'),
        'authtype': request.GET.get('authtype') if request.method == 'GET' else request.data.get('authtype'),
        'popupyn': request.GET.get('popupyn') if request.method == 'GET' else request.data.get('popupyn')
    }

class NiceAuthBaseView(APIView):
    """
    Base view for NICE authentication, handles common functionality.
    """
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
            openapi.Parameter('redirect_url', openapi.IN_QUERY, description="Redirect URL", type=openapi.TYPE_STRING),
            openapi.Parameter('authtype', openapi.IN_QUERY, description="Authentication Type", type=openapi.TYPE_STRING),
            openapi.Parameter('popupyn', openapi.IN_QUERY, description="Popup Flag", type=openapi.TYPE_STRING),
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

class GetNiceAuthDataView(NiceAuthBaseView):
    """
    View to handle the retrieval of NICE authentication data.
    """
    def handle_request(self, request):
        try:
            params = handle_get_or_post_request(request)
            service = NiceAuthService(
                base_url=settings.NICE_AUTH_BASE_URL,
                client_id=settings.NICE_CLIENT_ID,
                client_secret=settings.NICE_CLIENT_SECRET,
                product_id=settings.NICE_PRODUCT_ID,
                return_url=params['return_url'] or settings.NICE_RETURN_URL,
                authtype=params['authtype'] or settings.NICE_AUTHTYPE,
                popupyn=params['popupyn'] or settings.NICE_POPUPYN
            )
            auth_data = service.get_nice_auth()
            auth_request = create_nice_auth_request({**auth_data, **params})
            serializer = NiceAuthRequestDetailSerializer(auth_request)
            return Response(serializer.data)
        except NiceAuthException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetNiceAuthUrlView(NiceAuthBaseView):
    """
    View to handle the retrieval of NICE authentication URL.
    """
    def handle_request(self, request):
        try:
            params = handle_get_or_post_request(request)
            service = NiceAuthService(
                base_url=settings.NICE_AUTH_BASE_URL,
                client_id=settings.NICE_CLIENT_ID,
                client_secret=settings.NICE_CLIENT_SECRET,
                product_id=settings.NICE_PRODUCT_ID,
                return_url=params['return_url'] or settings.NICE_RETURN_URL,
                authtype=params['authtype'] or settings.NICE_AUTHTYPE,
                popupyn=params['popupyn'] or settings.NICE_POPUPYN
            )
            auth_data = service.get_nice_auth()
            auth_request = create_nice_auth_request({**auth_data, **params})
            nice_url = f"https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb?m=service&token_version_id={auth_data['token_version_id']}&enc_data={auth_data['enc_data']}&integrity_value={auth_data['integrity_value']}"
            return Response({'url': nice_url})
        except NiceAuthException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyNiceAuthView(APIView):
    """
    View to verify the result of NICE authentication.
    """
    @swagger_auto_schema(
        tags=['NICE Authentication'],
        operation_description="Verify NICE authentication result",
        request_body=VerifyNiceAuthSerializer,
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
            serializer = VerifyNiceAuthSerializer(data=request.data if request.method == 'POST' else request.GET)
            serializer.is_valid(raise_exception=True)
            enc_data = serializer.validated_data['enc_data']
            token_version_id = serializer.validated_data['token_version_id']
            integrity_value = serializer.validated_data['integrity_value']

            auth_request = NiceAuthRequest.objects.filter(token_version_id=token_version_id, integrity_value=integrity_value).first()
            if not auth_request:
                raise NotFound(detail="NiceAuthRequest with the specified token_version_id and integrity_value does not exist.")

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
            auth_result, created = NiceAuthResult.objects.get_or_create(
                request=auth_request,
                defaults={'result': result_data, 'request_no': auth_request.request_no, 'enc_data': enc_data, 'is_verified': True}
            )
            serializer = NiceAuthResultSerializer(auth_result)

            # Update the is_verified field of NiceAuthRequest
            auth_request.is_verified = True
            auth_request.save()

            # Check if redirect_url is present
            if auth_request.redirect_url:
                return HttpResponseRedirect(auth_request.redirect_url)

            return Response(serializer.data)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)
        except NiceAuthException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NiceAuthRequestRetrieveView(APIView):
    """
    View to retrieve the NiceAuthRequest by request_no.
    """
    @swagger_auto_schema(
        tags=['NICE Authentication'],
        operation_description="Retrieve NICE authentication request by request_no",
        responses={
            200: NiceAuthRequestDetailSerializer(many=False),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        }
    )
    def get(self, request, request_no):
        try:
            auth_request = NiceAuthRequest.objects.get(request_no=request_no)
            serializer = NiceAuthRequestDetailSerializer(auth_request)
            return Response(serializer.data)
        except NiceAuthRequest.DoesNotExist:
            return Response({'error': 'NiceAuthRequest with the specified request_no does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NiceAuthResultRetrieveView(APIView):
    """
    View to retrieve the NiceAuthResult by request_no.
    """
    @swagger_auto_schema(
        tags=['NICE Authentication'],
        operation_description="Retrieve NICE authentication result by request_no",
        responses={
            200: NiceAuthResultSerializer(many=False),
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        }
    )
    def get(self, request, request_no):
        try:
            auth_result = NiceAuthResult.objects.get(request_no=request_no)
            serializer = NiceAuthResultSerializer(auth_result)
            return Response(serializer.data)
        except NiceAuthResult.DoesNotExist:
            return Response({'error': 'NiceAuthResult with the specified request_no does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
