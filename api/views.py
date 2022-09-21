from rest_framework.decorators import api_view
from rest_framework.response import Response

from services.services import CoachService, GameService, TeamService, PlayerService, PlayRoundService


@api_view(['GET'])
def get_dashboard(request):
    return Response(PlayRoundService.get_dash_board())


@api_view(['GET'])
def get_all_games(request):
    return Response(GameService.get_all_game_details())


@api_view(['GET'])
def get_teams(request):
    return Response(TeamService.get_teams(request))


@api_view(['GET'])
def get_players_of_team(request, pk):
    return Response(PlayerService.get_players_by_team_id(request, pk))


@api_view(['GET'])
def get_player(request, pk):
    return Response(PlayerService.get_player(pk))


@api_view(['GET'])
def get_team_of_coach(request, pk):
    return Response(TeamService.get_team_full_detail_by_coach_id(request, pk))


@api_view(['GET'])
def get_players_of_coach(request, coach_id):
    return Response(PlayerService.get_players_by_coach_id(request, coach_id))


@api_view(['GET'])
def get_above_90_percentile_players_of_coach(request, coach_id):
    return Response(CoachService.get_players_abow_90_percentile(request, coach_id))






