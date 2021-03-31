import markdown
from django.utils.safestring import mark_safe
"""
위 두개로 문자열을 HTML코드로 변환
"""
from django import template


register = template.Library()


# sub함수에 @애너테이션 적용 = 해당함수를 필터로 사용 가능
@register.filter
# value = 기존값, arg = 입력 받은 값.
def sub(value, arg):
    return value - arg


@register.filter()
def mark(value):
    # 확장 도구
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))