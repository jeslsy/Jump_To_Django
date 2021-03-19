from django.contrib import admin
# pybo/models.py의 Question 객체를 가져와 쓸것임.
from .models import Question


# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


# Question 모델을 admin에 등록하겠솨와요 ^ㅡ^~
admin.site.register(Question, QuestionAdmin)
