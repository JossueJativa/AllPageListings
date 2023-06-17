from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


## Modelos de la base de datos
class Categories(models.Model):
    id = models.AutoField(primary_key=True, unique=True, auto_created=True, editable=False)
    category = models.CharField(max_length=64)

    def __str__ (self):
        return f"{self.category}"
    
class Listings(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    image = models.CharField(max_length=64)
    price_start = models.CharField(max_length=64)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category_listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    active = models.BooleanField(default=True)

    
    def __str__ (self):
        return f" {self.pk} {self.name} {self.description} {self.image} {self.category} {self.user} {self.active} {self.price_start}"
    
class Comments(models.Model):
    comment = models.CharField(max_length=64)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")

    def __str__ (self):
        return f"{self.comment} {self.user} {self.listing}"
    
class Bids (models.Model):
    price_bids = models.DecimalField(max_digits=12, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_dibs")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing_dibs")

    def __str__ (self):
        return f"{self.price_bids} {self.user} {self.listing}"
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing_watchlist")

    def __str__ (self):
        return f"{self.user} {self.listing}"