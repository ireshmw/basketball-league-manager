from django.db import models


class UserType(models.Model):
    type = models.CharField(max_length=20)

    class Meta:
        db_table = "%s_%s" % (__package__, "user_type")

    def __str__(self):
        return self.type


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    height = models.PositiveIntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Team(models.Model):
    team_name = models.CharField(max_length=255)
    coach = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.team_name


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'team'],
                name='player_constrains',
            )
        ]

    def __str__(self):
        return self.user.__str__()


class PlayRound(models.Model):
    play_round_name = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "%s_%s" % (__package__, "play_round")

    def __str__(self):
        return self.play_round_name


class Game(models.Model):
    play_round = models.ForeignKey(PlayRound, models.CASCADE)
    game_name = models.CharField(max_length=255)
    game_date = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return self.game_name + ' ' + self.game_date.__str__()


class GameTeam(models.Model):
    team = models.ForeignKey(Team, models.SET_NULL, blank=True, null=True)
    game = models.ForeignKey(Game, models.CASCADE, blank=True, null=True, related_name='game_teams')
    score = models.PositiveIntegerField()

    class Meta:
        db_table = "%s_%s" % (__package__, "game_team")
        constraints = [
            models.UniqueConstraint(fields=['team', 'game'], name='game_team_constraints')
        ]

    def __str__(self):
        return self.team.__str__() + ' ' + self.game.__str__() + ' ' + self.score.__str__()


class GamePlayer(models.Model):
    game_team = models.ForeignKey(GameTeam, models.CASCADE, blank=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True, related_name='payer_game')
    score = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        db_table = "%s_%s" % (__package__, "game_player")
        constraints = [
            models.UniqueConstraint(fields=['game_team', 'player'], name='game_player_constraints')
        ]

    def __str__(self):
        return self.player.__str__()
