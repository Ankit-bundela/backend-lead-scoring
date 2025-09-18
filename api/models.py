from django.db import models

class Offer(models.Model):
    name = models.CharField(max_length=255)
    value_props = models.JSONField()
    ideal_use_cases = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Lead(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    linkedin_bio = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class LeadScore(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    intent = models.CharField(max_length=20)
    reasoning = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
