
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Offer, Lead, LeadScore
from .views import rule_based_score

class RuleBasedScoreUnitTests(TestCase):
    def test_decision_maker_role_gets_20_points(self):
        # Create simple lead-like object using a lightweight mock (use model or simple object)
        class L: pass
        class O: pass
        lead = L()
        lead.role = "CEO"
        lead.industry = "B2B SaaS mid-market"
        lead.name = "A"
        lead.company = "C"
        lead.location = "L"
        lead.linkedin_bio = "bio"

        offer = O()
        offer.ideal_use_cases = ["B2B SaaS mid-market"]

        score, reasoning = rule_based_score(lead, offer)
        self.assertIn("Role is decision maker", reasoning)
        self.assertGreaterEqual(score, 20)

    def test_influencer_role_gets_10_points(self):
        class L: pass
        class O: pass
        lead = L()
        lead.role = "Lead Engineer"
        lead.industry = "B2B SaaS mid-market"
        lead.name = "A"
        lead.company = "C"
        lead.location = "L"
        lead.linkedin_bio = "bio"

        offer = O()
        offer.ideal_use_cases = ["B2B SaaS mid-market"]

        score, reasoning = rule_based_score(lead, offer)
        self.assertIn("Role is influencer", reasoning)
        self.assertGreaterEqual(score, 10)

    def test_industry_match_awards_20_points(self):
        class L: pass
        class O: pass
        lead = L()
        lead.role = "Manager"
        lead.industry = "B2B SaaS mid-market"
        lead.name = "A"
        lead.company = "C"
        lead.location = "L"
        lead.linkedin_bio = "bio"

        offer = O()
        offer.ideal_use_cases = ["B2B SaaS mid-market"]

        score, reasoning = rule_based_score(lead, offer)
        self.assertIn("Industry matches ICP", reasoning)
        self.assertGreaterEqual(score, 20)

    def test_data_completeness_awards_10_points(self):
        class L: pass
        class O: pass
        lead = L()
        lead.role = "Manager"
        lead.industry = "B2B SaaS mid-market"
        lead.name = "A"
        lead.company = "C"
        lead.location = "L"
        lead.linkedin_bio = "bio"

        offer = O()
        offer.ideal_use_cases = ["B2B SaaS mid-market"]

        score, reasoning = rule_based_score(lead, offer)
        self.assertIn("All fields present", reasoning)
        self.assertGreaterEqual(score, 10)


class IntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_full_flow_upload_score_and_results_and_csv(self):
        # 1) Create Offer
        offer_payload = {
            "name": "AI Outreach Automation",
            "value_props": ["24/7 outreach", "6x more meetings"],
            "ideal_use_cases": ["B2B SaaS mid-market"]
        }
        r = self.client.post("/offer/", offer_payload, format="json")
        self.assertEqual(r.status_code, 200)
        offer_id = r.data["offer"]["id"]

        # 2) Upload leads CSV
        csv_content = (
            "name,role,company,industry,location,linkedin_bio\n"
            "Ava Patel,Head of Growth,FlowMetrics,B2B SaaS mid-market,San Francisco,Experienced in SaaS growth\n"
            "John Doe,Manager,TechCorp,B2B SaaS mid-market,New York,SaaS marketing lead\n"
        ).encode("utf-8")
        uploaded = SimpleUploadedFile("leads.csv", csv_content, content_type="text/csv")
        r2 = self.client.post("/leads/upload/", {"file": uploaded}, format="multipart")
        self.assertEqual(r2.status_code, 200)
        self.assertTrue(len(r2.data["leads"]) >= 2)

        # 3) Call score endpoint
        r3 = self.client.post("/score/", {"offer_id": offer_id}, format="json")
        self.assertEqual(r3.status_code, 200)
        self.assertIn("results", r3.data)
        self.assertTrue(len(r3.data["results"]) >= 2)

        # Check LeadScore objects saved in DB
        scores = LeadScore.objects.filter(offer__id=offer_id)
        self.assertTrue(scores.exists())

        # 4) GET results JSON
        r4 = self.client.get("/results/")
        self.assertEqual(r4.status_code, 200)
        self.assertTrue(len(r4.data) >= 2)

        # 5) GET CSV export - ensure endpoint exists and returns CSV file content-type
        r5 = self.client.get("/results/export/")
        self.assertIn(r5.status_code, (200, 302))  # 200 OK or redirect if auth applied
        if r5.status_code == 200:
            self.assertIn("text/csv", r5["Content-Type"])
            content = r5.content.decode("utf-8")
            # CSV header check
            self.assertIn("name,role,company,intent,score,reasoning", content.lower())
