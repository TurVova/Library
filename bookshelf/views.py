from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from bookshelf.models import Book, User
from bookshelf.serializers import BookSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer