from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    release_date = models.DateField()
    genre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class GameReview(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.game.name} by {self.reviewer_name}"
