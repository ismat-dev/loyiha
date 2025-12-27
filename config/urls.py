from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('mcq/', include('apps.MCQ.urls')),
    path('submission/', include('apps.submission.urls')),

]
