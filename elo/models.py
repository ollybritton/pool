from django.db import models
from django.db.models import Q

class Player(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Frame(models.Model):
    winning_player = models.ForeignKey(Player, related_name="frames_won", on_delete=models.CASCADE) # TODO: how to deal with matches between multiple people? maybe don't?
    losing_player = models.ForeignKey(Player, related_name="frames_lost", on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        if self.winning_player.name < self.losing_player.name:
            return f"({self.winning_player}) vs {self.losing_player}"
        else:
            return f"{self.losing_player} vs ({self.winning_player})"