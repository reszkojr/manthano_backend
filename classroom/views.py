from django.shortcuts import render


def classroom_home(request, classroom_code):
    print(f'Hello world, {request.user}!')
