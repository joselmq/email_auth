from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from account.forms import SignUpForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


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


# class SignupPageView(TemplateView):
#     template_name = "signup.html"


class RestAPIView(APIView):
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
                                 "Users": all_users.values('first_name',
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
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data,
    #                                        context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response({
    #         'token': token.key,
    #         'user': user.pk,
    #         'email': user.email
    #     })

    def put(self, request, pk=None):
        return Response({'método': 'PUT'})

    def patch(self, request, pk=None):
        return Response({'método': 'PATCH'})

    def delete(self, request, pk=None):
        return Response({'método': 'DELETE'})
