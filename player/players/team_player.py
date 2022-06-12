from player.players.aggressive_player import *
from player.players.altruistic_player import *


class TeamPlayer(AggressivePlayer, AltruisticPlayer):
    """
    Type of player that plays in a teams game mode
    """

    def __init__(self, id, name):
        AggressivePlayer.__init__(self, id, name)
        AltruisticPlayer.__init__(self, id, name)


t = TeamPlayer(0, "t")