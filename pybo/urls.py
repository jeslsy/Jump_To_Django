# path 좀 쓸게..^^!
from django.urls import path
# 현재 폴더에 있는 views 함수들좀 가져다 씀
from . import views


app_name = 'pybo'


urlpatterns = [
    path('', views.index, name = 'index'),
    # int: = question_id에 숫자가 매핑됨을 이야기함
    # URL 매핑에 detail이라는 이름 붙여주자^^!
    path('<int:question_id>/',views.detail, name = 'detail'),
    # answer_create라는 별명을 가진 answer/create/question_id 매핑을 answer_create 뷰 함수에 보냄
    path('answer/create/<int:question_id>/', views.answer_create, name = 'answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    
    
    path('comment/create/question/<int:question_id>/', views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', views.comment_delete_question, name='comment_delete_question'),
    
    
    path('comment/create/answer/<int:answer_id>/', views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', views.comment_delete_answer, name='comment_delete_answer'),
    
]