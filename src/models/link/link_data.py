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
    def Parser(self) -> dict:
        return {"msg": f":{self.content}", "uid": self.uid}


class LobbyUpdateData(LinkData):
    def Parser(self) -> dict:
        return self.content


class BattleActionData(LinkData):
    def Parser(self) -> dict:
        content = dict(self.content)
        content.update({"uid": self.uid})
        return content


class BattleResultData(LinkData):
    def Parser(self) -> dict:
        return self.content
