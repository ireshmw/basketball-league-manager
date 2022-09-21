from django.db.models import Avg, Count, Prefetch

from data.models import Player, Team, GameTeam, Game,  PlayRound
from data.serializer import GameReverseSerializer, PlayerSerializer, \
    PlayerSerializerSingle,  TeamSerializerFull, TeamSerializerWithoutCoachDetails, PlayRoundSerializer


class TeamService(object):
    @staticmethod
    def get_teams(request):
        try:
            team_list = Team.objects \
                .select_related('coach') \
                .annotate(average_score=Avg('gameteam__score'))
            res = TeamSerializerFull(team_list, many=True, context={'request': request})
            return res.data
        except Team.DoesNotExist:
            return 'Cannot find Teams'

    @staticmethod
    def get_team_full_detail_by_coach_id(request, pk):
        try:
            team = Team.objects.filter(coach_id=pk) \
                .annotate(average_score=Avg('gameteam__score')).get()
            res = TeamSerializerWithoutCoachDetails(team, context={'request': request})
            return res.data
        except Team.DoesNotExist:
            return 'Cannot find Team'

    @staticmethod
    def get_team_by_coach_id(coach_id) -> Team | None:
        try:
            return Team.objects.get(coach_id=coach_id)
        except Team.DoesNotExist:
            return None


class PlayerService(object):
    @staticmethod
    def get_all_players():
        player_list = Player.objects.all()
        return player_list

    @staticmethod
    def get_players_by_team_id(request, team_id):
        try:
            player_list = Player.objects \
                .select_related('user', 'team') \
                .filter(team__id=team_id) \
                .annotate(average_score=Avg('payer_game__score'))
            res = PlayerSerializer(player_list, many=True, context={'request': request})
            return res.data
        except Player.DoesNotExist:
            return 'Cannot find the players'

    @staticmethod
    def get_players_by_coach_id(request, coach_id):
        try:
            player_list = Player.objects \
                .select_related('user', 'team') \
                .filter(team__coach_id=coach_id) \
                .annotate(average_score=Avg('payer_game__score'))
            res = PlayerSerializer(player_list, many=True, context={'request': request})
            return res.data
        except Player.DoesNotExist:
            return 'Cannot find the players'

    @staticmethod
    def get_player(pk):
        try:
            player = Player.objects.filter(id=pk) \
                .select_related('user', 'team') \
                .annotate(average_score=Avg('payer_game__score')) \
                .annotate(game_count=Count('payer_game__player')).get()

            res = PlayerSerializerSingle(player)
            return res.data
        except Player.DoesNotExist:
            return 'Cannot find the Player'


class CoachService(object):
    @staticmethod
    def get_players_abow_90_percentile(request, coach_id):
        team = TeamService.get_team_by_coach_id(coach_id)
        if team:
            player_list = Player.objects \
                .filter(team__id=team.id) \
                .annotate(average_score=Avg('payer_game__score')).order_by('average_score')

            if player_list.__len__() > 0:
                percentile = player_list.__len__() * 0.9
                rounded_pos = round(percentile)

                if rounded_pos > 1:
                    filtered_players = player_list[rounded_pos - 1:]
                else:
                    filtered_players = player_list
                res = PlayerSerializer(filtered_players, many=True, context={'request': request})
                return res.data
            else:
                return 'There are no players'
        else:
            return 'Coach does not exist'


class PlayRoundService(object):
    @staticmethod
    def get_dash_board():
        try:
            play_round_data = PlayRound.objects \
                .prefetch_related('game_set',
                                  Prefetch('game_set__game_teams', queryset=GameTeam.objects.select_related('team'),
                                           to_attr='game_teams_data'))

            ser = PlayRoundSerializer(play_round_data, many=True)
            return ser.data
        except PlayRound.DoesNotExist:
            return 'Cannot find the Games'


class GameService(object):
    @staticmethod
    def get_all_game_details():
        try:
            game_data = Game.objects.prefetch_related('game_teams__team')
            ser = GameReverseSerializer(game_data, many=True)
            return ser.data
        except Game.DoesNotExist:
            return 'Cannot find the Games'
