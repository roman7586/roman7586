from django import template


register = template.Library()


# CURRENCIES_SYMBOLS = {
#    'редиска': 'р******',
# }

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   # """
   # value: значение, к которому нужно применить фильтр
   # code: код замены
   # """
   # postfix = CURRENCIES_SYMBOLS[code]
   # # Возвращаемое функцией значение подставится в шаблон.
   # return f' {value} {postfix}'
      return value.replace("редиска", "р******")