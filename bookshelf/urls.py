from django.urls import path

from bookshelf.views import (
    BooksListAPIView,
    UserBooksAPIView,
    TakeBookAPIView,
    DetailBookAPIView,
    ReturnBookAPIView,
    ReturnAllBooksAPIView,
    UserCreateAPIView
)

urlpatterns = [
    path('book/get-all/', BooksListAPIView.as_view()),
    path('user/create/', UserCreateAPIView.as_view()),
    path('user/get-all-books/', UserBooksAPIView.as_view()),
    path('book/<int:book_id>/take/', TakeBookAPIView.as_view()),
    path('book/<int:book_id>/detail/', DetailBookAPIView.as_view()),
    path('book/<int:book_id>/return/', ReturnBookAPIView.as_view()),
    path('book/return-all/', ReturnAllBooksAPIView.as_view()),
]
