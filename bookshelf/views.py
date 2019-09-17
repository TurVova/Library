from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from bookshelf.models import Book
from bookshelf.serializers import BookSerializer, UserSerializer

User = get_user_model()

class UserCreateAPIView(views.APIView):
    """Create user"""

    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        try:
            user = User.objects._create_user(**data)
            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            response = {
                "error": f"User with email {data['email']} already exists"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserBooksAPIView(views.APIView):
    """List of user books"""

    authentication_classes = [JWTAuthentication]

    def get(self, request):
        books = Book.objects.filter(user=request.user)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TakeBookAPIView(views.APIView):
    """Getting books for use"""

    authentication_classes = [JWTAuthentication]

    def put(self, request, book_id):
        user = request.user
        response = {}

        try:
            book = Book.objects.get(id=book_id)

            if book.status:
                book.user = user
                book.status = False
                book.save()
                response = BookSerializer(book).data

            elif book.user == user:
                response['error'] = 'This book is in your use'

            elif not book.status:
                response['error'] = 'This book is not available'

            return Response(response, status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            response['error'] = f'Book with id {book_id} does not exist'

            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ReturnBookAPIView(views.APIView):
    """Return the book to the library."""

    authentication_classes = [JWTAuthentication]

    def put(self, request, book_id):
        user = request.user
        response = {}

        try:
            book = Book.objects.get(id=book_id)

            if book.user == user:
                book.user = None
                book.status = True
                book.save()
                response = BookSerializer(book).data

            elif book.user != user:
                response['error'] = "This book isn't in your use"

            return Response(response, status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            response['error'] = f'Book with id {book_id} does not exist'

            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ReturnAllBooksAPIView(views.APIView):
    """Return all books to the library"""

    authentication_classes = [JWTAuthentication]

    def put(self, request):
        user = request.user
        books = Book.objects.filter(user=user)
        for book in books:
            book.user = None
            book.status = True
        Book.objects.bulk_update(books, ['user', 'status'])

        return Response(f"{books.count()} books were returned.", status=status.HTTP_200_OK)


class DetailBookAPIView(views.APIView):
    """Obtaining detailed information"""

    authentication_classes = [JWTAuthentication]

    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookSerializer(book)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            response = {
                'error': f'Book with id {book_id} does not exist'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class BooksListAPIView(views.APIView):
    """List of books"""

    authentication_classes = [JWTAuthentication]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
