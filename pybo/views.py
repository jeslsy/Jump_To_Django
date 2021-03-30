from django.shortcuts import redirect, render, get_object_or_404
# HttpResponse클래스 = 페이지 요청에 대한 응답에 사용
#from django.http import HttpResponse
# Question 모델 가져와 쓸것.
from .models import Answer, Question, Comment
from django.utils import timezone
from .forms import QuestionForm, AnswerForm, CommentForm
# 페이징 기능 
from django.core.paginator import Paginator
# 로그인 정보가 필요한 함수를 위한것.
from django.contrib.auth.decorators import login_required
#
from django.contrib import messages


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
@login_required(login_url='common:login')
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
            return redirect('pybo:detail', question_id = question.id)
        
    # GET방식이면 입력창 반환
    else:
        form = AnswerForm()
    context = {'question': question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)    


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
            return redirect('pybo:detail', question_id=answer.question.id)
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



@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """
    pybo 질문댓글등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)




@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    pybo 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    pybo 질문댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)








@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    pybo 답글댓글등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """
    pybo 답글댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    pybo 답글댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)

