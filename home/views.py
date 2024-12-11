from django.shortcuts import render, HttpResponse
import os
from dotenv import load_dotenv
from django.http import JsonResponse, FileResponse
from .models import Query, BNS, IPC, CrPC, MVA, CPC, IEA, Document, Case
from home.webscrap import WebScrapping
import json
import re
import csv
from django.views.decorators.csrf import csrf_exempt
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from nltk.stem import PorterStemmer

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

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('punkt_tab')


@csrf_exempt
def encode(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query = data["query"]

            # Tokenize and preprocess the text
            crime_code_dic = {
                "murder": 0,
                "culpable homicide": 1,
                "decoity": 2,
                "kidnapping": 3,
                "robbery": 4,
                "bribery": 5,
                "theft": 6,
                "alcohol": 7,
                "criminal intimidation": 8
            }
            tokens = word_tokenize(query)
            stop_words = set(stopwords.words('english'))
            filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words]
            refined_tokens = [token for token in filtered_tokens if token not in string.punctuation]
            final_tokens = [token for token in refined_tokens if token.isalnum()]

            stemmer = PorterStemmer()
            stemmed_tokens = [stemmer.stem(token) for token in final_tokens]
            print("Stemmed Tokens:", stemmed_tokens)
            # Lemmatize tokens
            lemmatizer = WordNetLemmatizer()
            lemmatized_tokens = [lemmatizer.lemmatize(token) for token in stemmed_tokens]

            # Generate crime code
            crime_code = ""
            for token in lemmatized_tokens:
                if token in crime_code_dic:
                    crime_code += str(crime_code_dic[token])

            return JsonResponse({"crime_code": crime_code}, safe=False)


        except Exception as e:
            return JsonResponse({"error": str(e)})

    else:
        return JsonResponse("test", safe=False)


@csrf_exempt
def decode(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            crime_code = data["crime_code"]
            # Decode crime code to acts
            crime_code_dic = {
                "murder": 0,
                "culpable homicide": 1,
                "decoity": 2,
                "kidnapping": 3,
                "robbery": 4,
                "bribery": 5,
                "theft": 6,
                "alcohol": 7,
                "criminal intimidation": 8
            }
            acts = {
                "murder": ["100", "103"],
                "culpable homicide": ["299", "304"],
                "decoity": ["391", "395"],
                "kidnapping": ["359", "363"],
                "robbery": ["390", "392"],
                "bribery": ["171B", "171E"],
                "theft": ["378", "379"],
                "alcohol": ["510", ""],
                "criminal intimidation": ["503", "506"],
            }
            act = []
            for code in crime_code:
                index = int(code)
                crime = list(crime_code_dic.keys())[index]
                description, punishment = acts[crime]
                if description:
                    act.append(description)
                if punishment:
                    act.append(punishment)
            return JsonResponse({"acts": act}, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Method not allowed"})


#  AI
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

            return JsonResponse({"response": response.text})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Invalid Request Method"})

@csrf_exempt
def save_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data['query']
            response = data['response']

            # Save the query and response to the database
            Query.objects.create(query=query, response=response)

            return JsonResponse({"message": "Response saved successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": "Invalid Request Method"})


# Bare Acts
@csrf_exempt  # Remove this for production, use proper CSRF handling
def search_database(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            act = data.get("act")
            query = data.get("query")

            # Validate inputs
            if not act:
                return JsonResponse({"error": "Please provide an act"}, status=400)

            # Get the model for the selected act
            model = ACT_MODELS.get(act)
            if not model:
                return JsonResponse({"error": "Invalid 'act' provided."}, status=400)

            # only act
            if query == "":
                data = model.objects.values()
                data_list = list(data)
                return JsonResponse({"response": data_list})


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
    data_list = {}

    bns = BNS.objects.values()
    data_list['bns'] = list(bns)
    ipc = IPC.objects.values()
    data_list['ipc'] = list(ipc)
    crpc = CrPC.objects.values()
    data_list['crpc'] = list(crpc)
    cpc = CPC.objects.values()
    data_list['cpc'] = list(cpc)
    mva = MVA.objects.values()
    data_list['mva'] = list(mva)
    iea = IEA.objects.values()
    data_list['iea'] = list(iea)

    return JsonResponse({"data": data_list})


# PDFs
def save_pdf(request):
    """
    with open("", "rb") as pdf_file:
        binary_data = pdf_file.read()

    document = Document(act_name="",
                        description="",
                        pdf=binary_data)
    document.save()
    """
    return JsonResponse("saved", safe=False)


def pdf_list(request):
    # Fetch all PDFs with name and description
    documents = Document.objects.values('id', 'act_name', 'description').order_by('id')
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


# Cases
@csrf_exempt
def case_save(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            case = Case.objects.create(
                caseHeading=data.get('caseHeading'),
                applicableArticle=data.get('applicableArticle'),  # Convert list to JSON
                tags=data.get('tags'),  # Convert list to JSON
                query=data.get('query'),
                status=data.get('status'),
                description=data.get('description')
            )
            return JsonResponse({"message": "Case saved successfully!", "case": {
                "id": case.id,
                "caseHeading": case.caseHeading,
                "applicableArticle": case.applicableArticle,
                "tags": case.tags,
                "query": case.query,
                "status": case.status,
                "description": case.description,
            }}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def case_list(request):
    try:
        cases = Case.objects.all()
        cases_list = [
            {
                "id": case.id,
                "caseHeading": case.caseHeading,
                "applicableArticle": case.applicableArticle,
                "tags": case.tags,
                "query": case.query,
                "status": case.status,
                "description": case.description,
            }
            for case in cases
        ]
        return JsonResponse({"cases": cases_list}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def case_update(request, case_id):
    try:
        case = Case.objects.get(id=case_id)
        data = json.loads(request.body)

        case.caseHeading = data.get('caseHeading')
        case.applicableArticle = data.get('applicableArticle')
        case.tags = data.get('tags')
        case.query = data.get('query')
        case.status = data.get('status')
        case.description = data.get('description')
        case.save()

        return JsonResponse({"message": "Case saved successfully!", "case": {
            "id": case.id,
            "caseHeading": case.caseHeading,
            "applicableArticle": case.applicableArticle,
            "tags": case.tags,
            "query": case.query,
            "status": case.status,
            "description": case.description,
        }}, status=201)

    except Case.DoesNotExist:
        return JsonResponse({"error": "Case not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


