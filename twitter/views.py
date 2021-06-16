from django.http import HttpResponse, Http404
from django.template import loader
from twitter.models import TwitterHandle
from django.shortcuts import render, get_object_or_404
from twitter.manage_webinars import load_company_tweets_into_csv_file , load_company_tweets_into_csv_file_from_csv_file_refresh
import requests
from common.google_drive.read_data_from_spreadsheet import get_all_twitter_handles_from_spredsheet

def index(request):
    latest_twitter_handle_list = TwitterHandle.objects.order_by('-id')
    context = {
        'latest_twitter_handle_list': latest_twitter_handle_list,
    }
    if request.method == "POST":
        print("post")
        twitter_handle = request.POST.get('twitter_handle')
        folder_id = request.POST.get('folder_id')
        load_company_tweets_into_csv_file(twitter_handle, folder_id)
        return render(request, 'twitter/detail.html', {'handle': twitter_handle})
    return render(request, 'twitter/index.html', context)

def get_twitter_handle(request, twitter_handle , folder_id):
    # handle = get_object_or_404(TwitterHandle, twitter_handle=twitter_handle)
    load_company_tweets_into_csv_file(twitter_handle,folder_id)
    return render(request, 'twitter/detail.html', {'handle':twitter_handle})

def getwebinars(request):
    twitter_handle = request.GET.get('twitter_handle', '')
    folder_id = request.GET.get('folder_id', '')
    print("hrhjerekl")
    load_company_tweets_into_csv_file(twitter_handle, folder_id)
    return render(request, 'twitter/detail.html', {'handle':twitter_handle})

def get_webinars_to_refresh(request,file_name, date , sheet_num):
    print("filename{},date{}".format(file_name,date))
    twitter_handle_list = get_all_twitter_handles_from_spredsheet(file_name, sheet_num)
    load_company_tweets_into_csv_file_from_csv_file_refresh(twitter_handle_list, date)
    return HttpResponse("done")


