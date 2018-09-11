from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from scheduler import settings

from scheduler.api.views import TasksViewset, ResultsViewset

router = DefaultRouter()

router.register(r'tasks', TasksViewset, base_name='tasks')
router.register(r'results', ResultsViewset, base_name='results')

urlpatterns = [
    url(r'^api/v1.0/', include(router.urls, namespace='api')),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
