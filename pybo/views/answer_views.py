# question_id = URL 매핑 정보값 //2
# request = textarea에 작성한 form 데이터
from django.utils import timezone
from pybo.forms import AnswerForm
from django.contrib.auth.decorators import login_required
from pybo.models import Answer, Question
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.contrib import messages


@login_required(login_url='common:login')
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
            answer.author = request.user # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # 앵커 없을 때 (스크롤 관리 위함)
            #return redirect('pybo:detail', question_id = question.id)
            # 앵커로 redirect 구성할때 
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))
        
    # GET방식이면 입력창 반환
    else:
        form = AnswerForm()
    context = {'question': question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)    





# 답변 수정 함수 
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            #return redirect('pybo:detail', question_id=answer.question.id)
            # 앵커로 redirect 구성할때 
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)




# 답변 삭제 함수 추가하기.
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)