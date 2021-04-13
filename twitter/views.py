from django.http import HttpResponse, Http404
from django.template import loader
from twitter.models import TwitterHandle
from django.shortcuts import render, get_object_or_404
from manage_webinars import load_company_tweets_into_csv_file
import requests

def index(request):
    latest_twitter_handle_list = TwitterHandle.objects.order_by('-id')
    context = {
        'latest_twitter_handle_list': latest_twitter_handle_list,
    }
    # if request.method == "POST":
    #     handle = request.POST.get('twitter_handle')
    #     return render(request, 'twitter/detail.html', {'handle': handle})
    return render(request, 'twitter/index.html', context)

def get_twitter_handle(request, twitter_handle , folder_id):
    # handle = get_object_or_404(TwitterHandle, twitter_handle=twitter_handle)
    load_company_tweets_into_csv_file(twitter_handle,folder_id)
    return render(request, 'twitter/detail.html', {'handle':twitter_handle})

# def results(request, twitter_handle):
#     response = "You're looking at the results of twitter_handle %s."
#     return HttpResponse(response % twitter_handle)
#
# def get_webinars(request ,twitter_handle):
#     response = "You're looking at the get_webinars of twitter_handle %s."
#     return HttpResponse(response % twitter_handle)



