from rest_framework import serializers
from .models import BankCard


class CardSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BankCard
        fields = ('__all__')
        read_only_fields = ['date_of_issue', 'owner', 'status']


class CardSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = BankCard
        fields = ('name', 'cvv')
        read_only_fields = ['date_of_issue', 'owner', 'number']
