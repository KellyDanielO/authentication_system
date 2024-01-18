from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login

from .custom_functions import is_valid_email, check_email_exists
from .models import User
from .serializers import UserSerializer


# Let's create a base view
class BaseView(APIView):

    def get(self, request):
        return Response({'response': "OK"}, status=status.HTTP_200_OK)


# let's create our register view
class RegisterView(APIView):
    # let's create a post request
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')

        # let's check for errors
        if email is None or email == '' or password is None or password == '' or name is None or name == '':
            return Response({'response': 'empty fields'}, status=status.HTTP_400_BAD_REQUEST)

        # check if is valid email
        if not is_valid_email(email):
            return Response({'response': 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        if check_email_exists(email):
            return Response({'response': 'email exists'}, status=status.HTTP_409_CONFLICT)

        # validating password
        try:
            validate_password(password, User)
        except ValidationError as e:
            print(e)
            return Response({'error': 'invalid password', 'type': e}, status=status.HTTP_400_BAD_REQUEST)

        # creating new user
        user = User(email=email, name=name)
        user.set_password(password)
        user.save()

        serializer = UserSerializer(user)

        return Response({"response": 'user created', 'user': serializer.data}, status=status.HTTP_201_CREATED)


# Let's create the login view
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # let's check for errors
        if email is None or email == '' or password is None or password == '':
            return Response({'response': 'empty fields'}, status=status.HTTP_400_BAD_REQUEST)

        # check if is valid email
        if not is_valid_email(email):
            return Response({'response': 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        if not check_email_exists(email):
            return Response({'response': 'email does not exist'}, status=status.HTTP_409_CONFLICT)

        user = User.objects.get(email=email)
        if not user.check_password(password):
            return Response({'response': 'invalid password'}, status=status.HTTP_409_CONFLICT)

        else:
            try:
                login(request, user)
                serializer = UserSerializer(user)
                return Response({'response': 'login successful', 'user': serializer.data}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'response': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Thanks for watching, Please like and subscribe for more
# Link to source code is in the description
