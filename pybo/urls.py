# path 좀 쓸게..^^!
from django.urls import path
# 현재 폴더에 있는 views 함수들좀 가져다 씀
from . import views


app_name = 'pybo'


urlpatterns = [
    path('', views.index),
    # int: = question_id에 숫자가 매핑됨을 이야기함
    # URL 매핑에 detail이라는 이름 붙여주자^^!
    path('<int:question_id>/',views.detail, name = 'detail'),
    # answer_create라는 별명을 가진 answer/create/question_id 매핑을 answer_create 뷰 함수에 보냄
    path('answer/create/<int:question_id>/', views.answer_create, name = 'answer_create'),
]