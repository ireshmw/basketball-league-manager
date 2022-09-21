from django.contrib import admin

from data.models import UserType, User, Team, Player, Game, GameTeam, PlayRound, GamePlayer

admin.site.register(UserType)
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(PlayRound)
admin.site.register(Game)
admin.site.register(GameTeam)
admin.site.register(GamePlayer)


