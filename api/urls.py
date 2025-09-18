from django.urls import path
from django.http import JsonResponse
from .views import create_offer, export_results_csv, upload_leads, score_leads, results

def home(request):
    return JsonResponse({
        "message": "Lead Scoring Backend is running 🚀",
        "endpoints": {
            "Create Offer": "/offer/ (POST)",
            "Upload Leads": "/leads/upload/ (POST)",
            "Score Leads": "/score/ (POST)",
            "Get Results": "/results/ (GET)",
            "Export Results": "/results/export/ (GET)"
        }
    })

urlpatterns = [
    path('', home),   
    path('offer/', create_offer),
    path('leads/upload/', upload_leads),
    path('score/', score_leads),
    path('results/', results),
    path('results/export/', export_results_csv, name='export_results_csv'),
]
