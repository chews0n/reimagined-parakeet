from django.db import models


class PredResults(models.Model):
    """A data model to store the input and results."""
    previous_day_pool_price = models.FloatField()
    mean_temp = models.FloatField()
    rolling_30day_avg = models.FloatField()
    alberta_internal_load = models.FloatField()
    ng_price = models.FloatField()
    spd_of_max_gust = models.FloatField()
    day_of_year = models.FloatField()
    total_precip = models.FloatField()
    is_public_holiday = models.FloatField()
    pool_price = models.FloatField()

    class Meta:
        """Tells Django how to use plural names of Pred Results."""
        verbose_name_plural = 'Pred results'

    def __str__(self):
        return self.classification