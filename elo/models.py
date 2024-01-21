from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

class Player(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Frame(models.Model):
    winning_player = models.ForeignKey(Player, related_name="frames_won", on_delete=models.CASCADE) 
    losing_player = models.ForeignKey(Player, related_name="frames_lost", on_delete=models.CASCADE)
    breaking_player = models.ForeignKey(Player, related_name="frames_broken", on_delete=models.CASCADE)

    date = models.DateTimeField()

    def clean(self):
        if self.breaking_player not in [self.winning_player, self.losing_player]:
            raise ValidationError("breaking player must either be winning player or the losing player")
        
        if self.winning_player == self.losing_player:
            raise ValidationError("players cannot play with themselves")

    def __str__(self):
        if self.winning_player.name < self.losing_player.name:
            return f"({self.winning_player}) vs {self.losing_player}"
        else:
            return f"{self.losing_player} vs ({self.winning_player})"