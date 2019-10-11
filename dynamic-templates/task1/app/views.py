import csv

from django.shortcuts import render

from app.settings import INFLATION_CSV


def inflation_view(request):
    template_name = 'app/inflation.html'

    # чтение csv-файла и заполнение контекста
    with open(INFLATION_CSV, encoding='utf_8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        inflation = []
        for line in reader:
            inflation_year_dict = {
                'Год': line['Год'],
                'Январь': line['Янв'],
                'Февраль': line['Фев'],
                'Март': line['Мар'],
                'Апрель': line['Апр'],
                'Май': line['Май'],
                'Июнь': line['Июн'],
                'Июль': line['Июл'],
                'Август': line['Авг'],
                'Сентябрь': line['Сен'],
                'Октябрь': line['Окт'],
                'Ноябрь': line['Ноя'],
                'Декабрь': line['Дек'],
                'Всего': line['Суммарная'],
            }
            inflation.append(inflation_year_dict)
        for inflation_year_dict in inflation:
            inflation_year_dict.update((k, '-') for k, v in inflation_year_dict.items() if v == '')

    context = {'inflation': inflation}

    return render(request, template_name, context)
