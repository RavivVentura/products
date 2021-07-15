from django.http import HttpResponse, Http404
from django.template import loader
from twitter.models import TwitterHandle
from django.shortcuts import render, get_object_or_404
from twitter.manage_webinars import load_company_tweets_into_csv_file , load_company_tweets_into_csv_file_from_csv_file_refresh
import requests
from common.google_drive.read_data_from_spreadsheet import get_all_twitter_handles_and_folder_id_from_spredsheet , get_companies_twitter_handle_from_db

def index(request):
    latest_twitter_handle_list = TwitterHandle.objects.order_by('-id')
    context = {
        'latest_twitter_handle_list': latest_twitter_handle_list,
    }
    if request.method == "POST" and 'run_script' in request.POST:
        print("post")
        twitter_handle = request.POST.get('twitter_handle')
        folder_id = request.POST.get('folder_id')
        load_company_tweets_into_csv_file(twitter_handle, folder_id)
        return render(request, 'twitter/detail.html', {'handle': twitter_handle})
    if request.method == "POST" and 'all_companies' in request.POST:
        #get_companies_twitter_handle_from_db("https://www.reblaze.com")
        records = get_companies_twitter_handle_from_db()
        twitter_handles, companies_without_twitter_handle = get_all_twitter_handles_and_folder_id_from_spredsheet('Webinars_to_refresh',2,records)
        for twitter_handel, folder_id in twitter_handles.items():
            print("working on company:{}".format(twitter_handel))
            load_company_tweets_into_csv_file(twitter_handel, folder_id)
        for company in companies_without_twitter_handle:
            print("can't find twitter handle for this company:{} please search manually".format(company))
    return render(request, 'twitter/index.html', context)

# def all_companies_script(request):
#     if request.method == "POST" and 'all_companies' in request.POST:
#         load_company_tweets_into_csv_file('AccureBattery', '124L86R1gDZFMGxs_cRSZfjdGQBPYubZo')


def get_twitter_handle(request, twitter_handle , folder_id):
    # handle = get_object_or_404(TwitterHandle, twitter_handle=twitter_handle)
    load_company_tweets_into_csv_file(twitter_handle,folder_id)
    return render(request, 'twitter/detail.html', {'handle':twitter_handle})

def getwebinars(request):
    twitter_handle = request.GET.get('twitter_handle', '')
    folder_id = request.GET.get('folder_id', '')
    load_company_tweets_into_csv_file(twitter_handle, folder_id)
    return render(request, 'twitter/detail.html', {'handle':twitter_handle})

def get_webinars_to_refresh(request,file_name, date, sheet_num):
    print("val", file_name, date, sheet_num)
    twitter_handle_list = get_all_twitter_handles_and_folder_id_from_spredsheet(file_name, sheet_num)
    load_company_tweets_into_csv_file_from_csv_file_refresh(twitter_handle_list, date)
    return HttpResponse("done")


