from django.db import models


class Question(models.Model):
    job_id = models.CharField(max_length=200)
