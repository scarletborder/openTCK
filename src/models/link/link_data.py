from src.constant.enum.link_event import LinkEvent


class LinkData:
    def __init__(self, data_type: LinkEvent, uid: int, content):
        self.data_type = data_type
        self.uid = uid
        self.content = content

    def Parser(self) -> dict:
        return {
            "msg": f"uid:{self.uid}\r|type:{self.data_type.name}\r|content:{self.content}"
        }


class MessageData(LinkData):
    def __init__(self, uid: int, msg_str: str):
        super().__init__(LinkEvent.CHATMESSAGE, uid, msg_str)

    def Parser(self) -> dict:
        return {"msg": f":{self.content}", "uid": self.uid}


class LobbyUpdateData(LinkData):
    def __init__(self, uid: int, lobby):
        super().__init__(LinkEvent.LOBBYUPDATE, uid, lobby)

    def Parser(self) -> dict:
        return {"lobby": self.content}


class LobbyAssignData(LinkData):
    def __init__(self, uid: int, content):
        super().__init__(LinkEvent.LOBBYASSIGN, uid, content)

    def Parser(self) -> dict:
        return {"value": self.content}


class BattleActionData(LinkData):
    def __init__(self, uid: int, sk):
        """
        @`sk_dump`:技能的实例化
        """
        super().__init__(LinkEvent.BATTLEACTION, uid, sk)

    def Parser(self) -> dict:
        return {"skill": self.content, "uid": self.uid}


class BattleResultData(LinkData):
    def __init__(self, uid: int, game):
        super().__init__(LinkEvent.BATTLERESULT, uid, game)

    def Parser(self) -> dict:
        return {"game": self.content}


class BattleStartData(LinkData):
    """
    Will be deprecated, game, which `turn` is `0`, must be the start of a game
    """

    def __init__(self, uid: int, game):
        super().__init__(LinkEvent.BATTLESTART, uid, game)

    def Parser(self) -> dict:
        return {"game": self.content}
