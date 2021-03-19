from django.shortcuts import redirect, render, get_object_or_404
# HttpResponse클래스 = 페이지 요청에 대한 응답에 사용
#from django.http import HttpResponse
# Question 모델 가져와 쓸것.
from .models import Question
from django.utils import timezone

# request = 자동으로 전달되는 HTTP 요청 객체
def index(request):
    # pybo 목록 출력
    question_list =Question.objects.order_by('-create_date')
    # question_list를 템플릿에 전달
    context = {'question_list':question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    # 넘어온 id에 해당하는 질문 데이터 베이스 question에 저장
    question = get_object_or_404(Question, pk = question_id)
    # question을 templates에 넘겨주기 위해 context에 저장
    context = {'question': question}
    # 요청과 context를 question_detail.html에 전송
    return render(request, 'pybo/question_detail.html', context)


# question_id = URL 매핑 정보값 //2
# request = textarea에 작성한 form 데이터
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    # 넘어온 id를 질문 데이터베이스 question에 저장, 없으면 404
    question = get_object_or_404(Question, pk = question_id)
    # request.POST.get('content') 
    # = textarea에 작성한 데이터 추출 
    # = POST 형식으로 전송된 form 데이터 항목중//name,id,rows// name이 content인거를 추출
    # question.answer_set.create 
    # = Question 모델로 Answer모델 데이터 생성 // 외래키 있응께
    # = Answer모델로 데이터 저장 가능 저기 위처럼
    question.answer_set.create(content = request.POST.get('content'), create_date = timezone.now())
    return redirect('pybo:detail', question_id = question.id)



# Answer 모델로 데이터 저장 이렇게 가능!
# question = get_object_or_404(Question, pk=question_id)
# answer = Answer(question=question, content=request.POST.get('content'), create_
# date=timezone.now())
# answer.save()