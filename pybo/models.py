from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    # 질문의 제목
    # 글자 수 제한하고 싶을 때 CharField 사용 
    subject = models.CharField(max_length=200)
    # 질문의 내용
    # 제한 없는 데이터 = TextField 사용
    content = models.TextField()
    # 질문을 작성한 일시
    # 날짜, 시간 관련 = DataTimeField 사용
    create_date = models.DateTimeField()

    # 계정 삭제되면 계정과 연결된 Question 모델 데이터를 모두 삭제!
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 수정일시.
    # null = True : null 허용, blanck=True : form.is_valid()를 통한 입력 폼 데이터 검사 시 없어도 됨.
    modify_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.subject



class Answer(models.Model):
    # 질문
    # ForeingKey = Question모델의 질문 필요
    # CASCADE = 질문 삭제시 연결된 답변도 삭제  
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    # 답변의 내용
    content = models.TextField()
    # 답변 작성 일시
    create_date = models.DateTimeField()
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    

    
class Comment(models.Model):
    # 글쓴이
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    # 댓글 내용
    content= models.TextField()
    # 댓글 작성일시
    create_date = models.DateTimeField()
    # 댓글 수정일시
    # blank=True = 필드 안채워 져도 is_valid() 괜츈
    modify_date = models.DateTimeField(null=True, blank=True)
    # 이 댓글이 달린 질문
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    # 이 댓글이 달린 답변
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)