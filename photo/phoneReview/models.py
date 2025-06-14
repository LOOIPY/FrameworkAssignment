from django.db import models

# Create your models here.
class Phone(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='phones/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.brand} {self.name}"

class Review(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.phone.name} by {self.reviewer_name}"
