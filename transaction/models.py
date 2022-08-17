from django.db import models


class Transaction(models.Model):
    product_code = models.CharField(max_length=200, null=False)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.product_code+'_'+str(self.quantity)+'_'+str(self.price)
