from core import VK
from log import Log
import config

vk = VK(config.TOKEN)

log = Log("[FUNCS]").log

def detectSpam(text) -> bool:
    if 't.me/' in text:
        return True
    return False

def newMessageEventHandler(obj):
    if 'message' in obj:
        message = obj['message']
        if type(config.CONV_TO_LISTEN) == list:
            if message['peer_id'] not in [c+config.PEER_ADD_NUM for c in config.CONV_TO_LISTEN]:
                if config.CONV_TO_LISTEN != []:
                    return None
        else:
            if message['peer_id'] != config.PEER_ADD_NUM+config.CONV_TO_LISTEN:
                if config.CONV_TO_LISTEN != 0:
                    return None
        if detectSpam(message['text']):
            vk.api("messages.delete", message_ids=message['id'], spam=1, delete_for_all=1)
            vk.api("messages.removeChatUser", chat_id=message['chat_id'], user_id=message['from_id'])
