from django.shortcuts import render

from django.views import generic
from django.db.models import Q
from django.urls import reverse

from django.http import HttpResponseRedirect

from .models import Player, Frame
from .forms import AddForm

class IndexView(generic.TemplateView):
    template_name = 'elo/index.html'

    def get_context_data(self, **kwargs):
        context = {}

        players = Player.objects.all()
        frames = Frame.objects.all().order_by("date")

        pairs = []
        already_had = set()

        for player1 in players:
            for player2 in players:
                sorted_pair = sorted([player1.name, player2.name])

                if player1 != player2 and not (sorted_pair[0], sorted_pair[1]) in already_had:
                    already_had.update([(sorted_pair[0], sorted_pair[1])])

                    frames_together = Frame.objects.all().filter(Q(winning_player=player1, losing_player=player2) | Q(winning_player=player2, losing_player=player1))

                    if len(frames_together) == 0:
                        continue
                    else:
                        last_to_break = frames_together.latest("date").breaking_player.name

                        if last_to_break == player1.name:
                            suggested_break = player2
                        else:
                            suggested_break = player1                    

                    pairs.append({"player1": player1, "player2": player2, "player1_wins": 0, "player2_wins": 0, "suggested_break": suggested_break})        

        for frame in frames:
            for pair in pairs:
                if frame.winning_player.name == pair["player1"].name and frame.losing_player.name == pair["player2"].name:
                    pair["player1_wins"] += 1
                elif frame.losing_player.name == pair["player1"].name and frame.winning_player.name == pair["player2"].name:
                    pair["player2_wins"] += 1

        context["players"] = players
        context["frames"] = frames
        context["pairs"] = pairs

        return context

class AddView(generic.FormView):
    template_name = "elo/add.html"
    form_class = AddForm
    success_url = "/add"

    def get_initial(self):
        initial = super().get_initial()

        winning_player_id = self.request.GET.get("winning_player_id", None)

        if winning_player_id:
            winning_player = Player.objects.get(id=winning_player_id)
            initial["winning_player"] = winning_player


        losing_player_id = self.request.GET.get("losing_player_id", None)

        if losing_player_id:
            losing_player = Player.objects.get(id=losing_player_id)
            initial["losing_player"] = losing_player

        
        breaking_player_id = self.request.GET.get("breaking_player_id", None)

        if breaking_player_id:
            breaking_player = Player.objects.get(id=breaking_player_id)
            initial["breaking_player"] = breaking_player
        
        return initial

    def form_valid(self, form):
        form.save()

        cleaned_data = form.cleaned_data
        winning_player_id = cleaned_data["winning_player"].id
        losing_player_id = cleaned_data["losing_player"].id
        breaking_player_id = cleaned_data["breaking_player"].id

        if winning_player_id == breaking_player_id:
            new_breaking_player_id = losing_player_id
        else:
            new_breaking_player_id = winning_player_id

        print(cleaned_data)

        return HttpResponseRedirect(reverse("elo:add") + f"?winning_player_id={winning_player_id}&losing_player_id={losing_player_id}&breaking_player_id={new_breaking_player_id}")
        
        # return super().form_valid(form)
    
