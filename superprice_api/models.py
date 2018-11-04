from django.db import models


class Fruits(models.Model):
    title = models.CharField(max_length=255, null=False)
    price = models.FloatField(null=False)
    stock = models.IntegerField(null=False)
    sold = models.IntegerField(null=False)



    def __str__(self):
        return "{} - {} - {} - {}".format(self.title, self.price, self.stock, self.sold)

class Images(models.Model):
    image = models.ImageField(upload_to='images/')
    date = models.DateField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.image, self.date)

