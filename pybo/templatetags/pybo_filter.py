from django import template

register = template.Library()


# sub함수에 @애너테이션 적용 = 해당함수를 필터로 사용 가능
@register.filter
# value = 기존값, arg = 입력 받은 값.
def sub(value, arg):
    return value - arg