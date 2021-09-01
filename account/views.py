from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from account import serializers
from account.forms import SignUpForm


@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class GetUserInfo(APIView):
    serializer_class = serializers.RestSerializer

    def get(self, request, format=None):
        an_apiview = ["hello", "there"]
        return Response({'mensaje': 'hello there', 'an_apiview': an_apiview})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            user = User.objects.get(username=name)
            token = Token.objects.get_or_create(user=user)
            email = user.email
            active = user.is_active
            staff = user.is_staff
            is_superuser = user.is_superuser

            print(token)

            users = get_user_model()
            all_users = users.objects.all()

            print(all_users[0])

            if is_superuser:
                return Response({'mensaje': message,
                                 'token': token[0].key,
                                 'email': email,
                                 'active': active,
                                 'staff': staff,
                                 'is_superuser': is_superuser,
                                 "Users": all_users.values('username',
                                                           'first_name',
                                                           'last_name',
                                                           'email',
                                                           'is_superuser',
                                                           'is_staff',
                                                           'is_active')})
            return Response({'mensaje': message,
                             'token': token[0].key,
                             'email': email,
                             'active': active,
                             'staff': staff,
                             'is_superuser': is_superuser})
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, pk=None):
        return Response({'método': 'PUT'})

    def patch(self, request, pk=None):
        return Response({'método': 'PATCH'})

    def delete(self, request, pk=None):
        return Response({'método': 'DELETE'})
