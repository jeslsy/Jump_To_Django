from django.shortcuts import redirect, render, get_object_or_404
# HttpResponse클래스 = 페이지 요청에 대한 응답에 사용
#from django.http import HttpResponse
# Question 모델 가져와 쓸것.
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
# 페이징 기능 
from django.core.paginator import Paginator



# request = 자동으로 전달되는 HTTP 요청 객체
def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    # 여기서 1은 /pybo/같이 page 파라미터 없는 것을 위한 디폴트 값
    page = request.GET.get('page','1') # 페이지
    # 조회
    question_list =Question.objects.order_by('-create_date')
    
    # 페이징 처리
    # 페이징 구현에 사용한 클래스 = Panginator = question_list를 페이징 객체 paginator로 변환
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    # question_list를 템플릿에 전달
    context = {'question_list': page_obj}
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

def question_create(request):
    """
    pybo 질문 등록 & 저장
    """
    # URL = pybo/question/create
    # 동일한 URL 요청을 POST, GET 따라 다르게 처리
    # POST 방식일때 (저장하기 버튼) = 저장해줌
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # 임시저장하고 (아직 submit, content만 있기 때문)
            question = form.save(commit=False)
            # 작성 시간 필드 채워주고
            question.create_date = timezone.now()
            # 진짜 저장
            question.save()
            # pybo/index (= 목록 보여주는 페이지)로 redirect
            return redirect('pybo:index')
    
    # 따로 method없으면 GET 방식일때 = 입력창 보여줌.
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
    
    

def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    # pk기본키로 모델 객체 1개 출력 -> 없으면 404 페이지 반환
    question = get_object_or_404(Question, pk=question_id)
    # POST방식일 때 입력값넣은 객체 저장
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id = question.id)
        
    # GET방식이면 입력창 반환
    else:
        form = AnswerForm()
    context = {'question': question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)    
