import logging
import requests
from django.utils import timezone
from django.conf import settings
from rest_framework import viewsets
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from .auth_backend import JWTAuthBackend  # 导入 JWTAuthBackend

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthBackend()  # 创建 JWTAuthBackend 实例

    def __call__(self, request):
        response = self.get_response(request)
        response = self.process_response(request, response)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            # 获取视图类和动作名称
            view_class, action_name = self.get_view_class_and_action(request)

            # 检查视图类是否为 ModelViewSet 的子类并且定义了 activity_name
            if view_class and issubclass(view_class, viewsets.ModelViewSet) and hasattr(view_class, 'activity_name'):
                # 获取用户信息（可以是已认证用户或匿名用户）
                user = self.get_user_from_token(request)
                case_id = self.get_or_create_case_id(request, user)
                request.session['case_id'] = case_id

                request.start_time = timezone.now()
                user_name = getattr(user, 'email', 'Anonymous') if user else 'Anonymous'
                user_id = user.id if user else None

                # 获取 activity_name
                activity_name = view_class.activity_name  # 使用视图中的 activity_name
                logger.debug(f"Detected activity_name: {activity_name}")

                # 附加请求操作的后缀（如 List, Retrieve, Create）
                activity = f"{activity_name} {action_name.capitalize()}" if action_name else activity_name

                # 构建事件日志数据
                request.event_log = {
                    "case_id": case_id,
                    "activity": activity,
                    "start_time": str(request.start_time),
                    "user_id": user_id,
                    "user_name": user_name
                }

                # 打印日志数据以供调试
                logger.debug(f"Event Log: {request.event_log}")

                # 发送日志到日志 API 并保存返回的 ID
                log_id = self.log_event_to_api(request.event_log)
                if log_id:
                    request.event_log['id'] = log_id  # 保存日志ID，后续更新用
            else:
                # 不满足条件，不记录日志
                logger.debug("View is not a ModelViewSet with activity_name. Skipping logging.")

        except Exception as e:
            logger.error(f"Error in process_view: {str(e)}")

    def process_response(self, request, response):
        try:
            if hasattr(request, 'event_log') and 'id' in request.event_log:
                end_time = timezone.now()
                request.event_log['end_time'] = str(end_time)
                request.event_log['status_code'] = response.status_code

                # 更新日志并发送到日志 API
                self.update_log_event_to_api(request.event_log)
                logger.debug(f"Updated Event Log: {request.event_log}")
            else:
                logger.debug("No event_log or log ID found in request. Skipping process_response logging.")
        except Exception as e:
            logger.error(f"Error in process_response: {str(e)}")
        finally:
            return response

    def get_user_from_token(self, request):
        """
        使用 JWTAuthBackend 从请求中的 JWT Token 获取用户。
        如果没有 Token 或认证失败，返回 None（表示匿名用户）。
        """
        try:
            auth_result = self.jwt_auth.authenticate(request)
            if auth_result is not None:
                user, validated_token = auth_result
                return user
            else:
                logger.debug("No valid token found or user not authenticated, treating as anonymous")
                return None
        except (InvalidToken, AuthenticationFailed) as e:
            logger.error(f"Failed to authenticate user, treating as anonymous: {str(e)}")
            return None

    def get_view_class_and_action(self, request):
        """
        获取请求中的视图类和动作名称。
        """
        try:
            resolver_match = request.resolver_match
            view_class = getattr(resolver_match, 'cls', None)

            if view_class is None:
                # 尝试从 view_func 获取
                if hasattr(resolver_match.func, 'cls'):
                    view_class = resolver_match.func.cls
                elif hasattr(resolver_match.func, '__self__'):
                    view_class = resolver_match.func.__self__.__class__

            if view_class is None and hasattr(resolver_match.func, 'view_class'):
                view_class = resolver_match.func.view_class

            action_name = getattr(resolver_match, 'action', None)

            # 如果 action_name 仍然为 None，尝试推断
            if not action_name and view_class and issubclass(view_class, viewsets.ModelViewSet):
                if request.method.lower() == 'get' and 'pk' in resolver_match.kwargs:
                    action_name = 'retrieve'
                elif request.method.lower() == 'get':
                    action_name = 'list'
                elif request.method.lower() == 'post':
                    action_name = 'create'
                elif request.method.lower() == 'put':
                    action_name = 'update'
                elif request.method.lower() == 'patch':
                    action_name = 'partial_update'
                elif request.method.lower() == 'delete':
                    action_name = 'destroy'

            logger.debug(f"Resolved view_class: {view_class}")
            logger.debug(f"Determined action_name: {action_name}")

            return view_class, action_name
        except Exception as e:
            logger.error(f"Error resolving view class and action: {str(e)}")
            return None, None

    def get_or_create_case_id(self, request, user):
        """
        生成或获取用于日志记录的 case ID
        """
        if user:
            return f"user_{user.id}"
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            return f"session_{session_key}"

    def log_event_to_api(self, event_data):
        """
        发送日志到日志 API，并返回日志的 ID
        """
        try:
            response = requests.post(f"{settings.LOGS_API_URL}/api/customUser/event-logs/", json=event_data)
            if response.status_code == 201:
                response_data = response.json()
                log_id = response_data.get('data', {}).get('id')  # 获取日志ID
                if log_id:
                    logger.info(f"Log successfully recorded to API with ID: {log_id}")
                return log_id
            else:
                logger.error(f"Failed to record log to API: {response.status_code} {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error sending log to API: {str(e)}")
            return None

    def update_log_event_to_api(self, event_data):
        """
        更新日志到日志 API
        """
        try:
            log_id = event_data.get('id')
            if log_id:
                response = requests.patch(f"{settings.LOGS_API_URL}/api/customUser/event-logs/{log_id}/", json=event_data)
                if response.status_code == 200:
                    logger.info(f"Log successfully updated to API with ID: {log_id}")
                else:
                    logger.error(f"Failed to update log to API: {response.status_code} {response.text}")
            else:
                logger.error("No log ID found in event data. Cannot update log.")
        except Exception as e:
            logger.error(f"Error updating log to API: {str(e)}")
