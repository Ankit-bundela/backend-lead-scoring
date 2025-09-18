from django.urls import path
from .views import create_offer, export_results_csv, upload_leads, score_leads, results

urlpatterns = [
    path('offer/', create_offer),            # trailing slash
    path('leads/upload/', upload_leads),    # trailing slash
    path('score/', score_leads),
    path('results/', results),
    path('results/export/', export_results_csv, name='export_results_csv'),
]
