from rest_framework import serializers

from data.models import Game, GameTeam, Team, GamePlayer, UserType, User, Player, PlayRound


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['type']


class UserSerializer(serializers.ModelSerializer):
    user_type = UserTypeSerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'height', 'user_type']


class UserSerializerWithoutType(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'height']


class PlayerSerializer(serializers.ModelSerializer):
    player_data = UserSerializerWithoutType(source='user')
    average_score = serializers.SerializerMethodField()
    player_link = serializers.HyperlinkedIdentityField(view_name='single-player')

    def get_average_score(self, obj):
        return obj.average_score

    class Meta:
        model = Player
        fields = ['id', 'player_data', 'average_score', 'player_link']


class PlayerSerializerSingle(serializers.ModelSerializer):
    player_data = UserSerializerWithoutType(source='user')
    average_score = serializers.SerializerMethodField()
    game_count = serializers.SerializerMethodField()

    def get_average_score(self, obj):
        return obj.average_score

    def get_game_count(self, obj):
        return obj.game_count

    class Meta:
        model = Player
        fields = ['id', 'player_data', 'average_score', 'game_count']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'team_name']


class TeamSerializerDashboard(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_score(self, obj):
        return obj.score

    def get_name(self, obj):
        return obj.team.team_name

    class Meta:
        model = Team
        fields = ['id', 'name', 'score']


class TeamSerializerWithoutCoachDetails(serializers.ModelSerializer):
    average_score = serializers.SerializerMethodField()
    players = serializers.HyperlinkedIdentityField(view_name='team-players')

    def get_average_score(self, obj):
        return obj.average_score

    class Meta:
        model = Team
        fields = ['id', 'team_name', 'average_score', 'players']


class TeamSerializerFull(serializers.ModelSerializer):
    coach_data = UserSerializerWithoutType(source='coach')
    average_score = serializers.SerializerMethodField()
    players = serializers.HyperlinkedIdentityField(view_name='team-players')

    def get_average_score(self, obj):
        return obj.average_score

    class Meta:
        model = Team
        fields = ['id', 'team_name', 'average_score', 'coach_data', 'players']


class GameTeamSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = GameTeam
        fields = ['score', 'team']


class GameReverseSerializer(serializers.ModelSerializer):
    game_teams = GameTeamSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'game_date', 'game_teams']


class GamePlayerSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    average_score = serializers.SerializerMethodField()

    def get_average_score(self, obj):
        return obj.average_score

    class Meta:
        model = GamePlayer
        fields = ['id', 'player', 'average_score']


class GameSetSerializer(serializers.ModelSerializer):
    game_teams = TeamSerializerDashboard(source='game_teams_data', many=True, read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'game_name', 'game_date', 'game_teams']


class PlayRoundSerializer(serializers.ModelSerializer):
    games = GameSetSerializer(source='game_set', many=True, read_only=True)

    class Meta:
        model = PlayRound
        fields = ['id', 'play_round_name', 'games']