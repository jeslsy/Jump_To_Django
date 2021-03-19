"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
# include = pybo.urls사용할 수 있게 해줌.
from django.urls import path, include
## pybo 앱의 views 폴더 기능들 가져와 씀.
#from pybo import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # 이제부터 pybo/로 시작하는 페이지 요청은 모두 pybo/urls.py에서 관리
    path('pybo/', include('pybo.urls')),
]
