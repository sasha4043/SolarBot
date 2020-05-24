from vk_api import VkApi, vk_api
from vk_api.utils import get_random_id
import random
import vk
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk_session = vk_api.VkApi(token="токен группы")
longpoll = VkBotLongPoll(vk=vk_session, group_id=ид_группы)
vk = vk_session.get_api()

def fio(user_id):
	return str(vk.users.get(user_ids=user_id)['first_name']+" "+vk.users.get(user_ids=user_id)['last_name'])  # не работает

for event in longpoll.listen():
	if event.type == VkBotEventType.MESSAGE_NEW:
		print(event.obj.message)
		msg=event.obj.message['text']
		id=event.obj.message['from_id']
		if msg==":пинг":
			if event.from_user:
				vk.messages.send(user_id=id, random_id=random.randint(0, 2**64), message="Понг")
			elif event.from_chat:
				vk.messages.send(chat_id=event.chat_id, random_id=random.randint(0, 2**64), message="Понг")
		elif msg==":кик":
			if 'reply_message' in event.obj.message and event.from_chat:
				if event.from_chat and id==ид_админа:
					vk.messages.removeChatUser(chat_id=event.chat_id, member_id=event.obj.message['reply_message']['from_id'])
				else:
					vk.messages.send(chat_id=event.chat_id, random_id=random.randint(0, 2**64), message="Пшёл нах")
			else:
					vk.messages.send(chat_id=event.chat_id, random_id=random.randint(0, 2**64), message="А кого?")
		elif msg==":id":
			if 'reply_message' in event.obj.message:
				if event.from_user:
					vk.messages.send(user_id=id, random_id=random.randint(0, 2**64), message=str(event.obj.message['reply_message']['from_id']))
				elif event.from_chat:
					vk.messages.send(chat_id=event.chat_id, random_id=random.randint(0, 2**64), message=str(event.obj.message['reply_message']['from_id']))
			else:
				if event.from_user:
					vk.messages.send(user_id=id, random_id=random.randint(0, 2**64), message=str(id))
				elif event.from_chat:
					vk.messages.send(chat_id=event.chat_id, random_id=random.randint(0, 2**64), message=str(id))
		elif msg==":probe":
			stm="Просто сообщение"
			if 'reply_message' in event.obj.message:
				stm="Ответ на сообщение")
			elif 'fwd_messages' in event.obj.message:
				stm="Пересланные сообщения")
			if event.from_user:
				vk.messages.send(user_id=id, random_id=random.randint(0, 2**64), message=stm+" в ЛС")
			elif event.from_chat:
				vk.messages.send(chat_id=event.chat_id, random_id=random.randint(0, 2**64), message=stm+" в беседу")
