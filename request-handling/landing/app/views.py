from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по
    # GET параметру from-landing
    landing_arg = request.GET.get('from-landing')
    if landing_arg == 'test':
        counter_click['page_landing_alternate'] += 1
    else:
        counter_click['page_landing_original'] += 1
    print(counter_click['page_landing_original'])
    print(counter_click['page_landing_alternate'])
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    page_arg = request.GET.get('ab-test-arg')
    if page_arg == 'test':
        page = render_to_response('landing_alternate.html')
        counter_show['page_ab_alternate'] += 1
    else:
        page = render_to_response('landing.html')
        counter_show['page_ab_original'] += 1
    print(counter_show['page_ab_original'])
    print(counter_show['page_ab_alternate'])
    return page


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов
    # к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать
    # значения test и original
    # Для вывода результат передайте в следующем формате:
    try:
        original_conversion = counter_click['page_landing_original'] / counter_show['page_ab_original']
    except ZeroDivisionError:
        original_conversion = 0.0
    try:
        test_conversion = counter_click['page_landing_alternate'] / counter_show['page_ab_alternate']
    except ZeroDivisionError:
        test_conversion = 0.0
    return render_to_response('stats.html', context={
        'original_conversion': round(original_conversion, 2),
        'test_conversion': round(test_conversion, 2),
    })
