from django.db import models


class Property(models.Model):
    address_number = models.IntegerField(default=0)
    address_street = models.CharField(max_length=200)
    address_city = models.CharField(max_length=200)
    parcel_id = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    zoning = models.CharField(max_length=200)
    sale_date = models.CharField(max_length=200)
    sale_price = models.CharField(max_length=200)
    legal_reference = models.CharField(max_length=200)
    seller = models.CharField(max_length=200)
    assessment_year = models.CharField(max_length=200)
    land_area = models.CharField(max_length=200)
    building_value = models.CharField(max_length=200)
    extra_features_value = models.CharField(max_length=200)
    land_value = models.CharField(max_length=200)
    total_value = models.CharField(max_length=200)
    narrative_description = models.CharField(max_length=200)
    last_updated = models.DateTimeField("date published")

    def __str__(self):
        return "%s %s" % (self.address_number, self.address_street)
