from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class IPCheckMiddleware(MiddlewareMixin):
    allowed_ips = settings.ALLOWED_IPS

    def process_request(self, request):
        if request.META['REMOTE_ADDR'] not in self.allowed_ips and hasattr(
                request.user, 'employee'):
            print("IPCheckMiddleware: IP address not allowed" +
                  request.META['REMOTE_ADDR'])
            print("IPCheckMiddleware: Allowed IPs are: " +
                  str(self.allowed_ips))
            print(request.META.get('HTTP_X_FORWARDED_FOR'))
            raise PermissionDenied
