from django.db import models


class Deal(models.Model):
    deal_id = models.IntegerField()
    deal_name = models.CharField(max_length=250, blank=True, null=True)
    deal_stage = models.CharField(max_length=250, blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    deal_type = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.deal_id)


class HubToken(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_in = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.access_token)
