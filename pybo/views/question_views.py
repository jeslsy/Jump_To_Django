from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from pybo.forms import QuestionForm
from django.contrib.auth.decorators import login_required
from pybo.models import Question
from django.contrib import messages


# Answer 모델로 데이터 저장 이렇게 가능!
# question = get_object_or_404(Question, pk=question_id)
# answer = Answer(question=question, content=request.POST.get('content'), create_
# date=timezone.now())
# answer.save()
@login_required(login_url='common:login')
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
            # author(글쓴이) = user()
            question.author = request.user
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
    
    
    
    
    
    # 질문 수정 함수.
@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    # 사용자 == 글쓴이 ??
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    # 입력 form 요소 내용 POST 전송시 객체에 저장.
    if request.method == "POST":
        # 기본 값을 기반으로 전달받은 입력값들 덮어써서 QuestionForm 생성하라는 의미.
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시 현재 시간으로 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
        
    # GET 전송시 기존 제목, 내용 그대로.
    else:
        # 기존 제목, 내용 그대로
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


# 질문 삭제 함수.
@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')