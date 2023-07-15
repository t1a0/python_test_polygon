from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpRequest

from send_and_get_card.models import BankCard


def main_page_view(request):
    return render(request, 'main_page.html', {'title': 'Home'})

def validate_number(number) -> bool:
    number = number.replace("-", "")
    if len(number) == 16 and number.isdigit():
        return False
    else:
        return True



def create_card_view(request):
    if request.POST:
        try:
            data = request.POST
            number = data['number'].replace("-","")
            exp_date = data['exp_date']

            if validate_number(number):
                error_message = "Неправильний формат номеру картки."
                return render(request, 'create.html', {'title': 'Create card', 'error': error_message})
            card = BankCard(number=int(number), exp_date=data['exp_date'], cvv=data['cvv'])
            card.save()
            success_message = "Картка додана."
            return render(request, 'create.html', {'title': 'Створення картки', 'success': success_message})
        except Exception as e:
            error_message = "Помилка додавання картки: " + str(e)
            return render(request, 'create.html', {'title': 'Створення картки', 'error': error_message})
    else:
        check = False

    return render(request, 'create.html', {'title': 'Створення картки', 'check': check})


def show_card_view(request):
    if request.GET:
        card_number = request.GET.get('number').replace("-","")
        if validate_number(card_number):
            error_message = "Неправильний формат номеру картки."
            return render(request, 'show.html', {'title': 'Пошук картки', 'error': error_message})
        else:
            card = BankCard.objects.filter(number=int(card_number)).first()
    else:
        card = False

    return render(request, 'show.html', {'title': 'Пошук картки', 'card': card})

