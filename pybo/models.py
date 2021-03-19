from django.db import models


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

    