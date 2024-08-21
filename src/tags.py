#Tag class

class Tag():

    def __init__(self, src, target):
        import player, mob, items
        self._src: player.Player | mob.Mob | items.Item = src
        self._target: player.Player | mob.Mob = target
        self._id = "Anon Tag"

        self._on_attack = False
        self._on_hit = True

    @property
    def id(self) -> str:
        return self._id
    @property
    def on_attack(self) -> str:
        return self._on_attack
    @property
    def on_hit(self) -> str:
        return self._on_hit
    @property
    def src(self) -> str:
        return self._src
    @property
    def target(self) -> str:
        return self._target
    
    def apply(self):
        raise NotImplementedError