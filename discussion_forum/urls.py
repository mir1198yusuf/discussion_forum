"""discussion_forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf import settings 
from django.conf.urls.static import static
from django.views.static import serve

import boards.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', boards.views.Home_View.as_view(), name='home_url'),
    path('board/', include('boards.urls')),     #urls of boards app
    path('user/', include('user_account.urls')),    #urls of user_account app  


    #mdeditor
    path('mdeditor/', include('mdeditor.urls'))
    
] 


#serving media files for development only
if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, view=serve, document_root=settings.MEDIA_ROOT)
    #https://docs.djangoproject.com/en/3.0/ref/views/#django.views.static.serve
    #https://docs.djangoproject.com/en/3.0/ref/urls/#django.conf.urls.static.static