class GameruleConf:
    def __init__(self, drain_when_hurt: bool = True) -> None:
        self.drain_when_hurt = drain_when_hurt
        pass

    def ToDict(self) -> dict:
        return {"drain_when_hurt": self.drain_when_hurt}
