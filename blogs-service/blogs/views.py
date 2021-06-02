from django.shortcuts import render
from django.http import HttpResponse
from main import main
# Create your views here.
def get_blogs(request):
    main()
    return render(request, 'blogs/homepage.html')
