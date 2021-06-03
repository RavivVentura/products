from django.shortcuts import render
from django.http import HttpResponse
from blogs_service.main import main
# Create your views here.
def get_blogs(request):
    main()
    return render(request, 'blogs_service/homepage.html')
    #return HttpResponse("success")
