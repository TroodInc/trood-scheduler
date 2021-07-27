from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter


from scheduler.api.views import TasksViewset, ResultsViewset

router = DefaultRouter()

router.register(r'tasks', TasksViewset, base_name='tasks')
router.register(r'results', ResultsViewset, base_name='results')

urlpatterns = [
    url(r'^api/v1.0/', include(router.urls, namespace='api')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        url('swagger/', TemplateView.as_view(template_name='swagger_ui.html'), name='swagger-ui'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
