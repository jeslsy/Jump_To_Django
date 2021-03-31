# request = 자동으로 전달되는 HTTP 요청 객체
from django.shortcuts import get_object_or_404, render
from pybo.models import Question
from django.core.paginator import Paginator
# 검색기능에 사용함.
from django.db.models import Q

def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    # 여기서 1은 /pybo/같이 page 파라미터 없는 것을 위한 디폴트 값
    page = request.GET.get('page','1') # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    
    # 조회
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            # kw 문자 포함되었는지 확인.
            # contains 말고 icontains 쓰면 대소문자 가리지 않고 찾아줌! 개꿀!
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()
    
    

    
    
    # 페이징 처리
    # 페이징 구현에 사용한 클래스 = Panginator = question_list를 페이징 객체 paginator로 변환
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    # question_list를 템플릿에 전달
    # 입력 받은 page와 kw값을 템플릿 searchForm에 전달 위해 context안에 page와 kw로 넣어줌.
    context = {'question_list': page_obj, 'page': page, 'kw': kw}  # page와 kw가 추가되었다.
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    # 넘어온 id에 해당하는 질문 데이터 베이스 question에 저장
    question = get_object_or_404(Question, pk = question_id)
    # question을 templates에 넘겨주기 위해 context에 저장
    context = {'question': question}
    # 요청과 context를 question_detail.html에 전송
    return render(request, 'pybo/question_detail.html', context)

