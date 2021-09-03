from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsSuperuser
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import UserSerializer
from account.forms import SignUpForm
from .serializers import ListUserSerializer, UpdateUserSerializer


class ListUsersView(ListAPIView):
    permission_classes = [IsAdminUser, IsSuperuser]
    queryset = User.objects.all()
    serializer_class = ListUserSerializer


class UpdateUserView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer


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


class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
