import logging
import requests
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from drf_spectacular.extensions import OpenApiAuthenticationExtension

User = get_user_model()
logger = logging.getLogger(__name__)

class JWTAuthBackend(JWTAuthentication):
    def authenticate(self, request):
        try:
            header = self.get_header(request)
            if header is None:
                return None

            raw_token = self.get_raw_token(header)
            if raw_token is None:
                logger.debug("No token found in Authorization header")
                return None

            logger.debug(f"Raw token: {raw_token}")

            # 验证Token
            validated_token = self.get_validated_token(raw_token)
            logger.debug(f"Validated token: {validated_token}")

            # 从Token中获取用户信息
            user = self.get_user(validated_token)
            return (user, validated_token)
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise AuthenticationFailed(str(e))

    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            
            url = f"{settings.USER_SERVICE_URL}/api/customUser/me/"
            logger.debug(f"Requesting user info from: {url}")
            
            response = requests.get(
                url,
                headers={'Authorization': f"Bearer {validated_token}"}
            )
            # logger.debug(f"Response status: {response.status_code}")
            # logger.debug(f"Response content: {response.text}")
            
            if response.status_code == 200:
                user_data = response.json()['data']
                user, created = User.objects.update_or_create(
                    id=user_data['id'],
                    defaults={
                        'email': user_data['email'],
                        'username': user_data['name'],
                        'is_staff': user_data['is_staff'],
                        'is_active': user_data['is_active'],
                    }
                )
                logger.debug(f"User {'created' if created else 'updated'}: {user}")
                return user
            else:
                raise AuthenticationFailed(f'无法验证用户: {response.status_code} - {response.text}')
        except Exception as e:
            logger.error(f'获取用户信息时出错: {str(e)}')
            raise AuthenticationFailed(f'获取用户信息时出错: {str(e)}')

class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'accommodation.auth_backend.JWTAuthBackend'
    name = 'JWTAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
