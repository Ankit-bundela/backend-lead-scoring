from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Offer, Lead, LeadScore
from .serializers import OfferSerializer, LeadSerializer, LeadScoreSerializer
import pandas as pd
import csv
from django.http import HttpResponse

# -------------------------
# Offer APIs
# -------------------------
@api_view(['POST'])
def create_offer(request):
    serializer = OfferSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':200, 'offer': serializer.data})
    return Response({'status':400, 'errors': serializer.errors})

@api_view(['POST'])
def upload_leads(request):
    file = request.FILES.get('file')
    if not file:
        return Response({'status':400, 'error':'CSV file required'})
    
    df = pd.read_csv(file)
    leads = []
    for _, row in df.iterrows():
        lead = Lead.objects.create(
            name=row['name'],
            role=row['role'],
            company=row['company'],
            industry=row['industry'],
            location=row['location'],
            linkedin_bio=row['linkedin_bio']
        )
        leads.append(lead)
    serializer = LeadSerializer(leads, many=True)
    return Response({'status':200, 'leads': serializer.data})

# -------------------------
# Scoring Logic
# -------------------------
def rule_based_score(lead, offer):
    score = 0
    reasoning = []

    decision_maker_roles = ['Head', 'Manager', 'Director', 'VP', 'Chief', 'CEO', 'CFO', 'CTO', 'COO']
    influencer_roles = ['Lead', 'Senior', 'Team']

    # Role relevance
    if any(r in lead.role for r in decision_maker_roles):
        score += 20
        reasoning.append('Role is decision maker (+20)')
    elif any(r in lead.role for r in influencer_roles):
        score += 10
        reasoning.append('Role is influencer (+10)')
    
    # Industry match
    if lead.industry in offer.ideal_use_cases:
        score += 20
        reasoning.append('Industry matches ICP (+20)')
    else:
        score += 10
        reasoning.append('Industry partially matches (+10)')

    # Data completeness
    if all([lead.name, lead.role, lead.company, lead.industry, lead.location, lead.linkedin_bio]):
        score += 10
        reasoning.append('All fields present (+10)')

    return score, '; '.join(reasoning)

def ai_score(lead, offer):
    """
    Dummy AI scoring without OpenAI. 
    Assign High/Medium/Low intent and points based on lead role and offer.
    """
    role = lead.role.lower()
    if any(r.lower() in role for r in ['ceo', 'head', 'director', 'vp', 'chief']):
        return 50, 'High', 'AI reasoning: senior role strongly aligns with offer'
    elif any(r.lower() in role for r in ['manager', 'engineer', 'lead']):
        return 30, 'Medium', 'AI reasoning: relevant role may influence decision'
    else:
        return 10, 'Low', 'AI reasoning: role less relevant for offer'

# -------------------------
# Scoring API
# -------------------------
@api_view(['POST'])
def score_leads(request):
    offer_id = request.data.get('offer_id')
    if not offer_id:
        return Response({'status':400, 'error':'offer_id required'})
    
    try:
        offer = Offer.objects.get(id=offer_id)
    except Offer.DoesNotExist:
        return Response({'status':404, 'error':'Offer not found'})

    scores = []
    leads = Lead.objects.all()
    for lead in leads:
        # Rule layer
        rule_points, rule_reasoning = rule_based_score(lead, offer)

        # AI layer
        ai_points, ai_intent, ai_reasoning = ai_score(lead, offer)

        # Final score
        final_score = rule_points + ai_points

        # Create LeadScore object
        ls = LeadScore.objects.create(
            lead=lead,
            offer=offer,
            score=final_score,
            intent=ai_intent,
            reasoning=rule_reasoning + '; ' + ai_reasoning
        )
        scores.append(ls)
    
    serializer = LeadScoreSerializer(scores, many=True)
    return Response({'status':200, 'results': serializer.data})

# -------------------------
# Results APIs
# -------------------------
@api_view(['GET'])
def results(request):
    scores = LeadScore.objects.all()
    serializer = LeadScoreSerializer(scores, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def export_results_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="results.csv"'

    writer = csv.writer(response)
    writer.writerow(["name", "role", "company", "intent", "score", "reasoning"])

    scores = LeadScore.objects.select_related("lead", "offer").all()
    for s in scores:
        writer.writerow([
            s.lead.name,
            s.lead.role,
            s.lead.company,
            s.intent,
            s.score,
            s.reasoning
        ])
    return response
