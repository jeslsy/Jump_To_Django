from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm


def signup(request):
    """
    계정 생성
    """
    #request가 POST방식이면
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # 유효하면 전송받아온 값 저장
            form.save()
            username = form.cleaned_data.get('username')
            # 입력값 얻어옴
            raw_password = form.cleaned_data.get('password1')
            
            # 완료후 자동으로 로그인되도록 authenticate와 login함수를 이용!
            user = authenticate(username=username, password = raw_password)
            login(request, user)
            return redirect('index')
        
    # request가 GET방식이면
    else:
        # 입력창 보여주기
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})