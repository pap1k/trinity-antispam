from core import VK
from log import Log
import sys
import config
import spam_level
from spam_dicts import *

vk = VK(config.TOKEN)

log = Log("[FUNCS]").log

alpha = {
    'a': 'а',
    'e': 'е',
    'c': 'с',
    'w': 'ш',
    '0': 'о',
    'o': 'о',
    'x': 'х',
    'p': 'р',
    't': 'т',
    '3': 'з',
    'k': 'к',
    'u': 'и',
    'h': 'н',
    'y': 'у',
    'z': 'з',
    'v': 'в'
}

def perform(text) -> str:
    text = text.lower().strip()
    for letter in alpha:
        text = text.replace(letter, alpha[letter])
    return text

def detectSpam(text) -> int:
    def check(obsc):
        for ob in obsc:
            if ob in text: return True
        return False
    if check(kick_url):
        return spam_level.KICK
    if check(announce_urls):
        return spam_level.ANNOUNCE
    text = perform(text)
    if check(announce_words):
        return spam_level.ANNOUNCE
    if check(kick_words):
        return spam_level.KICK
    return spam_level.NONE

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

        if message['text'] == "":
            return None
        result = detectSpam(message['text'])
        if result == spam_level.KICK:
            if '-test' in sys.argv:
                vk.api("messages.send", peer_id=config.CONV_TO_ANNOUNCE+config.PEER_ADD_NUM, message="[БОТ]\n(test)Удалил это сообщение:", forward_messages=message['id'])
            else:
                vk.api("messages.send", peer_id=config.CONV_TO_ANNOUNCE+config.PEER_ADD_NUM, message="[БОТ]\nУдалил это сообщение:", forward_messages=message['id'])
                vk.api("messages.delete", message_ids=message['id'], spam=1, delete_for_all=1)
                vk.api("messages.removeChatUser", chat_id=message['peer_id']-config.PEER_ADD_NUM, user_id=message['from_id'])
        elif result == spam_level.ANNOUNCE:
            vk.api("messages.send", peer_id=config.CONV_TO_ANNOUNCE+config.PEER_ADD_NUM, message="[БОТ]\nВозможно насрали в чате:", forward_messages=message['id'])
        
