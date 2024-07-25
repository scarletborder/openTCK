from src.utils.link.rpc.rpc_linker import RpcLinker
import src.utils.link.link_menu as LM
from src.battle.choose_skill import ParserSkill
from src.utils.pkui.utils import NewUI
import src.utils.logging.utils as Logging

import src.storage.battle as SBA
import src.storage.lobby as SLB
import src.storage.signal as Signal
from src.storage.buffer import ReadInput

import asyncio


async def SendThingsForever(Linker: RpcLinker):
    while True:
        await Signal.could_type.wait()
        content = await ReadInput()  # vanilla input
        if content is None or len(content) == 0:
            continue
        if content[0] == "!":
            # 发送message
            asyncio.create_task(Linker.SendMessage(content[1:]))
            continue
        elif (await LM.RunMenuCommand(content, Linker)) is True:
            # 执行了菜单指令
            continue
        else:
            # action
            if Signal.could_send_action.is_set() is False:
                # 现在不能发送action
                NewUI.PrintChatArea("It is not right time to send action")
                continue
            else:
                # parser first
                ok, msg, sk = ParserSkill(
                    SLB.My_Player_Info.GetId(), content, SBA.Current_Game
                )
                if ok is False or sk is None:
                    Logging.Infoln("Fail to summon skill to send: " + str(msg))
                    continue
                else:
                    # sendaction
                    asyncio.create_task(Linker.SendAction(content, sk))
                    # 禁用
                    Signal.could_send_action.clear()
                    # t.add_done_callback()
                    ...

                # ~ 时间到了也禁用
                # 最后发送
