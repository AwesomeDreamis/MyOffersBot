from django.db import models


class Employer(models.Model):
    name = models.CharField(max_length=100)
    tg_chat_id = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    url = models.CharField(max_length=1000, blank=True)

    sent = models.BooleanField(default=False)
