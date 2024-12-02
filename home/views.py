from django.shortcuts import render, HttpResponse
import os
from dotenv import load_dotenv
import google.generativeai as genai
from django.http import JsonResponse, FileResponse
from .models import Query, BNS, IPC, CrPC, MVA, CPC, IEA, Document
from home.webscrap import WebScrapping
import json
import re
import csv
from django.views.decorators.csrf import csrf_exempt


load_dotenv()

# Create your views here.
def home(request):
    return HttpResponse("Hello Developer...")

ACT_MODELS = {
    "bns": BNS,
    "ipc": IPC,
    "crpc": CrPC,
    "iea": IEA,
    "cpc": CPC,
    "mva": MVA,
}
@csrf_exempt
def ai(request):
    if request.method == 'POST':
        try:
            # Get the query from the request
            data = json.loads(request.body)
            query = data['query']
            prompt = os.getenv('prompt')
            text = f"{query}. {prompt}"
            # Generate response using the query
            API_KEY = os.getenv("API_KEY")
            if not API_KEY:
                raise ValueError("API_KEY is not set. Please set it in your .env file.")
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(text)

            # Add query and response to database (Optional, based on your model)
            # Query.objects.create(query=query, response=response_text)

            return JsonResponse({"response": response.text})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Invalid Request Method"})


@csrf_exempt  # Remove this for production, use proper CSRF handling
def search_database(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            act = data.get("act")
            query = data.get("query")

            # Validate inputs
            if not act or not query:
                return JsonResponse({"error": "Both 'act' and 'query' are required."}, status=400)

            # Get the model for the selected act
            model = ACT_MODELS.get(act)
            if not model:
                return JsonResponse({"error": "Invalid 'act' provided."}, status=400)

            # Search for the record
            record = model.objects.filter(section_id=query).first() or \
                     model.objects.filter(section_title=query).first()

            if not record:
                return JsonResponse({"error": "No matching record found."}, status=404)

            # Build the response
            response = {
                "section": getattr(record, "section_id", ""),
                "title": getattr(record, "section_title", ""),
                "description": getattr(record, "description", ""),
            }
            return JsonResponse({"data": response}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid Request Method"}, status=405)


def database(request):

    #websrcap
    """
    url = os.getenv("link")
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

    return HttpResponse(f"i am a chill guy!\n\t Added -> {section_no} - {section_title}")
    """
    data = BNS.objects.values()
    data_list = list(data)
    return JsonResponse({"data": data_list})

def save_pdf(request):
    '''with open("C:\Django projects\Space\Project_Backend\Criminal Laws/BNS.pdf", "rb") as pdf_file:
        binary_data = pdf_file.read()

    document = Document(act_name="",
                        description="",
                        pdf=binary_data)
    document.save()'''

    return JsonResponse("saved", safe=False)


def pdf_list(request):
    # Fetch all PDFs with name and description
    documents = Document.objects.all().values('id', 'act_name', 'description')
    return JsonResponse(list(documents), safe=False)

def download_pdf(request, pdf_id):
    try:
        # Fetch the PDF document by ID
        document = Document.objects.get(id=pdf_id)

        response = HttpResponse(document.pdf, content_type='application/pdf')

        # Add content-disposition header to indicate it's a file
        response['Content-Disposition'] = f'attachment; filename="{document.act_name}.pdf"'
        return response
    except Document.DoesNotExist:
        return JsonResponse({"error": "Document not found"}, status=404)


