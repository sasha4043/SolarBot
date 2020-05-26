from vk_api import VkApi, vk_api
from vk_api.utils import get_random_id
import random
import vk
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json


vk_session = vk_api.VkApi(token="токен")
longpoll = VkBotLongPoll(vk=vk_session, group_id=ид_группы)
vk = vk_session.get_api()

def fio(uid):
	return vk.users.get(user_ids=uid)[0]['first_name']+" "+vk.users.get(user_ids=uid)[0]['last_name']

def fios(uid):
	sps=""
	j=0
	for i in uid:
		if j>0:
			sps+=", "
		sps+=vk.users.get(user_ids=i)[0]['first_name']+" "+vk.users.get(user_ids=i)[0]['last_name']
		j+=1
	return sps

def spli(li):
	sps=""
	j=0
	for i in li:
		if j>0:
			sps+=", "
		sps+=str(i)
		j+=1
	return sps

def admin_add(uid):
	with open('admlist.json') as f:
		file_content = f.read()
		admlist = json.loads(file_content)
	if admlist['ids'].count(uid) > 0:
		return 1
	else:
		admlist['ids'].append(uid)
		with open('admlist.json', 'w') as f:
			f.write(json.dumps(admlist))
		return 2

def admin_del(uid):
	with open('admlist.json') as f:
		file_content = f.read()
		admlist = json.loads(file_content)
	if admlist['ids'].count(uid) == 0:
		return 1
	else:
		admlist['ids'].remove(uid)
		with open('admlist.json', 'w') as f:
			f.write(json.dumps(admlist))
		return 2

def admin_list_names():
	with open('admlist.json') as f:
		file_content = f.read()
		admlist = json.loads(file_content)
		return fios(admlist['ids'])

for event in longpoll.listen():
	if event.type == VkBotEventType.MESSAGE_NEW:
		print(event.obj.message)
		msg=event.obj.message['text']
		id=event.obj.message['from_id']
		if msg==":пинг":
			if event.from_user:
				vk.messages.send(user_id=id, 
						 random_id=random.randint(0, 2**64), 
						 message="Понг")
			elif event.from_chat:
				vk.messages.send(chat_id=event.chat_id, 
						 random_id=random.randint(0, 2**64), 
						 message="Понг")
		elif msg==":кик":
			if 'reply_message' in event.obj.message and event.from_chat:
				if event.from_chat and id==ид_админа:				# Потом здесь вместо id==ид_админа, будет проверка наличия пользователя в списке админов
					vk.messages.removeChatUser(chat_id=event.chat_id, 
								   member_id=event.obj.message['reply_message']['from_id'])
				else:
					vk.messages.send(chat_id=event.chat_id, 
							 random_id=random.randint(0, 2**64), 
							 message="Пшёл нах")
			else:
					vk.messages.send(chat_id=event.chat_id, 
							 random_id=random.randint(0, 2**64), 
							 message="А кого?")
		elif msg==":id":
			if 'reply_message' in event.obj.message:
				if event.from_user:
					vk.messages.send(user_id=id, 
							 random_id=random.randint(0, 2**64), 
							 message='ID '+'[id'+str(event.obj.message['reply_message']['from_id'])+'|пользователя]: '+str(event.obj.message['reply_message']['from_id']))
				elif event.from_chat:
					vk.messages.send(chat_id=event.chat_id, 
							 random_id=random.randint(0, 2**64), 
							 message='ID '+'[id'+str(event.obj.message['reply_message']['from_id'])+'|пользователя]: '+str(event.obj.message['reply_message']['from_id']))
			elif 'fwd_messages' in event.obj.message and len(event.obj.message['fwd_messages'])==1:
				if event.from_user:
					vk.messages.send(user_id=id, 
							 random_id=random.randint(0, 2**64), 
							 message='ID '+'[id'+str(event.obj.message['fwd_message'][0]['from_id'])+'|пользователя]: '+str(event.obj.message['fwd_message'][0]['from_id']))
				elif event.from_chat:
					vk.messages.send(chat_id=event.chat_id, 
							 random_id=random.randint(0, 2**64), 
							 message='ID '+'[id'+str(event.obj.message['fwd_message'][0]['from_id'])+'|пользователя]: '+str(event.obj.message['fwd_message'][0]['from_id']))
			else:
				if event.from_user:
					vk.messages.send(user_id=id, 
							 random_id=random.randint(0, 2**64), 
							 message='ID '+'[id'+str(id)+'|пользователя]: '+str(id))
				elif event.from_chat:
					vk.messages.send(chat_id=event.chat_id, 
							 random_id=random.randint(0, 2**64), 
							 message='ID '+'[id'+str(id)+'|пользователя]: '+str(id))
		elif msg==":name":
			stm='Имя '+'[id'+str(id)+'|пользователя]: '+fio(id)
			if 'reply_message' in event.obj.message:
				stm='Имя '+'[id'+str(event.obj.message['reply_message']['from_id'])+'|пользователя]: '+fio(event.obj.message['reply_message']['from_id'])
			elif 'fwd_messages' in event.obj.message and len(event.obj.message['fwd_messages'])>0:
				stm='Имена пользователей: '+fios(event.obj.message['fwd_messages'][i]['from_id'] for i in range(len(event.obj.message['fwd_messages'])))
			if event.from_user:
				vk.messages.send(user_id=id, 
								 random_id=random.randint(0, 2**64), 
								 message=stm)
			elif event.from_chat:
				vk.messages.send(chat_id=event.chat_id, 
								 random_id=random.randint(0, 2**64), 
								 message=stm)
		elif msg==":probe":
			stm="Просто сообщение"
			if 'reply_message' in event.obj.message:
				stm="Ответ на сообщение от "+fio(event.obj.message['reply_message']['from_id'])
			elif 'fwd_messages' in event.obj.message and len(event.obj.message['fwd_messages'])>0:
				stm="Пересланные сообщения от "+fios(event.obj.message['fwd_messages'][i]['from_id'] for i in range(len(event.obj.message['fwd_messages'])))
			if event.from_user:
				vk.messages.send(user_id=id, 
						 random_id=random.randint(0, 2**64), 
						 message=stm+" в ЛС")
			elif event.from_chat:
				vk.messages.send(chat_id=event.chat_id, 
						 random_id=random.randint(0, 2**64), 
						 message=stm+" в беседу")
		elif msg==":listadm":
			if event.from_chat:
				vk.messages.send(chat_id=event.chat_id, 
						 random_id=random.randint(0, 2**64), 
						 message=admin_list_names())
		elif msg==":addadm":
			if 'reply_message' in event.obj.message:
				atat=admin_add(event.obj.message['reply_message']['from_id'])
				if atat == 2:
					if event.from_user:
						vk.messages.send(user_id=id, 
								 random_id=random.randint(0, 2**64), 
								 message='[id'+str(event.obj.message['reply_message']['from_id'])+'|Пользователь] получил админку')
					elif event.from_chat:
						vk.messages.send(chat_id=event.chat_id, 
								 random_id=random.randint(0, 2**64), 
								 message='[id'+str(event.obj.message['reply_message']['from_id'])+'|Пользователь] получил админку')
				elif atat == 1:
					if event.from_user:
						vk.messages.send(user_id=id, 
								 random_id=random.randint(0, 2**64), 
								 message='У [id'+str(event.obj.message['reply_message']['from_id'])+'|пользователя] и так есть админка')
					elif event.from_chat:
						vk.messages.send(chat_id=event.chat_id, 
								 random_id=random.randint(0, 2**64), 
								 message='У [id'+str(event.obj.message['reply_message']['from_id'])+'|пользователя] и так есть админка')
		elif msg==":deladm":
			if 'reply_message' in event.obj.message:
				atat=admin_del(event.obj.message['reply_message']['from_id'])
				if atat == 2:
					if event.from_user:
						vk.messages.send(user_id=id, 
								 random_id=random.randint(0, 2**64), 
								 message='[id'+str(event.obj.message['reply_message']['from_id'])+'|Пользователь] лишился админки')
					elif event.from_chat:
						vk.messages.send(chat_id=event.chat_id, 
								 random_id=random.randint(0, 2**64), 
								 message='[id'+str(event.obj.message['reply_message']['from_id'])+'|Пользователь] лишился админки')
				elif atat == 1:
						if event.from_user:
							vk.messages.send(user_id=id, 
									 random_id=random.randint(0, 2**64), 
									 message='У [id'+str(event.obj.message['reply_message']['from_id'])+'|пользователя] и так нет админки')
						elif event.from_chat:
							vk.messages.send(chat_id=event.chat_id, 
									 random_id=random.randint(0, 2**64), 
									 message='У [id'+str(event.obj.message['reply_message']['from_id'])+'|пользователя] и так нет админки')
