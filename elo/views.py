from django.shortcuts import render

from django.views import generic

from .models import Player, Frame

class IndexView(generic.TemplateView):
    template_name = 'elo/index.html'

    def get_context_data(self, **kwargs):
        context = {}

        players = Player.objects.all()
        frames = Frame.objects.all().order_by("date")

        pairs = []

        for player1 in players:
            for player2 in players:
                if player1 != player2:
                    pairs.append({"player1": player1.name, "player2": player2.name, "player1_wins": 0, "player2_wins": 0})        

        for frame in frames:
            for pair in pairs:
                if frame.winning_player.name == pair["player1"] and frame.losing_player.name == pair["player2"]:
                    pair["player1_wins"] += 1
                elif frame.losing_player.name == pair["player1"] and frame.winning_player.name == pair["player2"]:
                    pair["player2_wins"] += 1

        context["players"] = players
        context["frames"] = frames
        context["pairs"] = pairs

        return context
