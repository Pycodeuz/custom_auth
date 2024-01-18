from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from core.drf_yasg import urlpatterns

urlpatterns = [
                  path('user/', include('users.urls')),
                  path('blog/', include('blog.urls')),
                  path('token/create/', TokenObtainPairView.as_view(), name='token_create'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
              ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
