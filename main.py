from core import LongPoll
from core import VK
from log import Log
import config
from functions import newMessageEventHandler

vk = VK(config.TOKEN)
log = Log("[MAIN]").log


while True:
    try:
        LP = LongPoll(config.TOKEN)

        LP.addListener('message_new', newMessageEventHandler)
        log("Started", createfile=True)
        LP.run()
    except KeyboardInterrupt:
        break
    except Exception as err:
        print(f'НЕОТЛОВЛЕННАЯ ОШИБКА {err}')