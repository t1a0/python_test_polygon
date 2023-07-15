from django.urls import path

from send_and_get_card.views import create_card_view, main_page_view, show_card_view


urlpatterns = [
	path('', main_page_view, name='home_card'),
	path('create/',  create_card_view, name='create_card'),
	path('show/', show_card_view, name='show_card'),

]