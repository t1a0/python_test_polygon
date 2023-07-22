from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import BankCard, Status
from .permissions import IsOwner
from .serializer import CardSerializer, CardSerializerUpdate

class CardsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner, IsAuthenticated]
    queryset = BankCard.objects.all()
    serializer_class = CardSerializer

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return CardSerializerUpdate
        return CardSerializer

    def list(self, request):
        # Retrieve cards belonging to the authenticated user
        cards = BankCard.objects.filter(owner=request.user)

        if cards.exists():
            # Serialize the cards and return the data
            data = [CardSerializer(card).data for card in cards]
            return Response(data)

        return Response({"error": "You don`t have any cards"})

    @action(methods=['get'], detail=True, permission_classes=[IsOwner, IsAuthenticated])
    def freeze(self, request, pk=None):
        if not pk:
            return Response({'error': 'You need to enter a primary key'})

        try:
            card = BankCard.objects.get(pk=pk)
        except BankCard.DoesNotExist:
            return Response({'error': 'This card doesn`t exist'})

        if not (request.user.is_authenticated and request.user == card.owner):
            return Response({'error': 'It`s not your card'})

        # Set the card status to 'Frozen' (Status ID 3)
        card.status = Status.objects.get(pk=3)
        card.save()

        return Response(CardSerializer(card).data)

    @action(methods=['get'], detail=True, permission_classes=[IsOwner, IsAuthenticated])
    def reactivate(self, request, pk=None):
        if not pk:
            return Response({'error': 'You need to enter a pk'})

        try:
            card = BankCard.objects.get(pk=pk)
        except BankCard.DoesNotExist:
            return Response({'error': 'This card doesn`t exist'})

        if not (request.user.is_authenticated and request.user == card.owner):
            return Response({'error': 'It`s not your card'})

        # Set the card status to 'Active' (Status ID 2)
        card.status = Status.objects.get(pk=2)
        card.save()

        return Response(CardSerializer(card).data)
