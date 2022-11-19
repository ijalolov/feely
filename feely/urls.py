from django.conf import settings
from django.contrib import admin


from django.conf.urls.static import static
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from drf_yasg.generators import OpenAPISchemaGenerator


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["https"]
        return schema


schema_view = get_schema_view(
   openapi.Info(
      title="Feely API",
      default_version='v1',
      description="Feely backend",
   ),
   public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
   permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/doctor/', include('doctor.urls')),
    path('api/article/', include('article.urls')),
    path('api/psy_test/', include('psy_test.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/chat-app/', include('chat_app.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
