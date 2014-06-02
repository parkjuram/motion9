from django.shortcuts import render

# Create your views here.
def registration_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')

    if password is not password_confirm:
