from django.shortcuts import render, HttpResponse
import os
from dotenv import load_dotenv
import google.generativeai as genai
from django.http import JsonResponse
from .models import Query, BNS, IPC, CrPC, MVA, CPC, IEA
from home.webscrap import WebScrapping
import json
import re
import csv


load_dotenv()

# Create your views here.
def home(request):
    return HttpResponse("Hello Developer...")

def ai(request):
    if request.method == 'POST':
        try:
            # Get the query from the request
            data = json.loads(request.body)
            query = data['query']

            # Generate response using the query
            API_KEY = os.getenv("API_KEY")
            if not API_KEY:
                raise ValueError("API_KEY is not set. Please set it in your .env file.")
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(query)

            # Add query and response to database
            Query.objects.create(query=query, response=response.text)
            return JsonResponse({"response": response.text})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:  
        return JsonResponse({"error": "Invalid Request Method"})

def search_database(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        act = data.get("act")
        if not act:
            return JsonResponse({"error": "Act is not selected"})
        query = data.get("query")
        if not query:
            return JsonResponse({"error": "None"})

        response = {"section": "",
                    "title": "",
                    "description": ""}
        if act == 'bns':
            if BNS.objects.filter(section_id=query).exists():
                record = BNS.objects.get(section_id=query)
                response["section"] = query
                response["title"] = record.section_title
                response["description"] = record.description

            elif BNS.objects.filter(section_title=query).exists():
                record = BNS.objects.get(section_title=query)
                response["title"] = query
                response["section"] = record.section_id
                response["description"] = record.description
            else:
                return JsonResponse({"error": "Enter valid query"})

        elif act == 'ipc':
            if IPC.objects.filter(section_id=query).exists():
                record = IPC.objects.get(section_id=query)
                response["section"] = query
                response["title"] = record.section_title
                response["description"] = record.description

            elif IPC.objects.filter(section_title=query).exists():
                record = IPC.objects.get(section_title=query)
                response["title"] = query
                response["section"] = record.section_id
                response["description"] = record.description
            else:
                return JsonResponse({"error": "Enter valid query"})

        elif act == 'crpc':
            if CrPC.objects.filter(section_id=query).exists():
                record = CrPC.objects.get(section_id=query)
                response["section"] = query
                response["title"] = record.section_title
                response["description"] = record.description

            elif CrPC.objects.filter(section_title=query).exists():
                record = CrPC.objects.get(section_title=query)
                response["title"] = query
                response["section"] = record.section_id
                response["description"] = record.description
            else:
                return JsonResponse({"error": "Enter valid query"})

        elif act == 'iea':
            if IEA.objects.filter(section_id=query).exists():
                record = IEA.objects.get(section_id=query)
                response["section"] = query
                response["title"] = record.section_title
                response["description"] = record.description

            elif IEA.objects.filter(section_title=query).exists():
                record = IEA.objects.get(section_title=query)
                response["title"] = query
                response["section"] = record.section_id
                response["description"] = record.description
            else:
                return JsonResponse({"error": "Enter valid query"})

        elif act == 'cpc':
            if CPC.objects.filter(section_id=query).exists():
                record = CPC.objects.get(section_id=query)
                response["section"] = query
                response["title"] = record.section_title
                response["description"] = record.description

            elif CPC.objects.filter(section_title=query).exists():
                record = CPC.objects.get(section_title=query)
                response["title"] = query
                response["section"] = record.section_id
                response["description"] = record.description
            else:
                return JsonResponse({"error": "Enter valid query"})

        elif act == 'mva':
            if MVA.objects.filter(section_id=query).exists():
                record = MVA.objects.get(section_id=query)
                response["section"] = query
                response["title"] = record.section_title
                response["description"] = record.description

            elif MVA.objects.filter(section_title=query).exists():
                record = MVA.objects.get(section_title=query)
                response["title"] = query
                response["section"] = record.section_id
                response["description"] = record.description
            else:
                return JsonResponse({"error": "Enter valid query"})
        return JsonResponse(response, status=200)
    return JsonResponse({"error": "Invalid Request Method"})

def data(request):
    '''url = os.getenv("link")
    scrapping = WebScrapping(url)
    section_detail = scrapping.scrap()
    for section in section_detail:
        #print(section)
        description = section_detail[section]
        match = re.match(r"Section (\d+[A-Za-z]*)\s*[\u2013\u2014-]\s*(.+)", section)
        #print(match)
        section_no = match.group(1)
        section_title = match.group(2).strip()
        print(section_no, section_title)
        if not IEA.objects.filter(section_id=section_no).exists():
            IEA(section_id=section_no, section_title=section_title, description=description).save()

    #print(section_detail)

    return HttpResponse(f"i am a chill guy!\n\t Added -> {section_no} - {section_title}")'''
    data = BNS.objects.values()
    data_list = list(data)
    return JsonResponse({"response": "i am a chill guy!", "data": data_list})

