from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    timeout_seconds = 100

class CheapTalk(Page):
    timeout_seconds = 100
    form_model = models.Player
    form_fields = ['ct_upfront_amount', 'ct_promised_amount']
    def is_displayed(self):
        return self.player.id_in_group == 1

class CheapTalkWaitPage(WaitPage):
    body_text = "Please wait for the Player 1 to finish Cheap Talk stage"



class PrisonersDilemma(Page):
    form_model = models.Player
    form_fields = ['pd_decision']
    def vars_for_template(self):
        return {
            'player_1': self.player.id_in_group == 1,
            'ct_promised_amount': self.group.get_player_by_id(1).ct_promised_amount,
            'ct_upfront_amount': self.group.get_player_by_id(1).ct_upfront_amount,
        }


class PrisonersDilemmaWaitPage(WaitPage):
    body_text = "Please wait for the Player 1 to finish Cheap Talk stage"



class RewardCooperation(Page):
    timeout_seconds = 100
    form_model = models.Player
    form_fields = ['ct_actual_amount']
    def is_displayed(self):
        if self.player.pd_decision.lower() == 'cooperate' and self.player.other_player().pd_decision.lower() == 'cooperate':
            return self.player.id_in_group == 1

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()




class Results(Page):
    def vars_for_template(self):
        return {
            'my_decision': self.player.pd_decision.lower(),
            'other_player_decision': self.player.other_player().pd_decision.lower(),
            'same_choice': self.player.pd_decision == self.player.other_player().pd_decision,
        }


page_sequence = [
    Introduction,
    CheapTalk,
    CheapTalkWaitPage,
    PrisonersDilemma,
    PrisonersDilemmaWaitPage,
    RewardCooperation,
    ResultsWaitPage,
    Results
]
