from django.urls import path

from send_and_get_card.views import BankCardView


urlpatterns = [
	path('card/', BankCardView.as_view(http_method_names=['get', 'post']) , name='bank_card')
]