from random import randint
import requests
import re

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType


random_id = 3894509385098345435098455309811504
random_id += randint(-100000000, 100000000)

token = 'eb61814709b24cabae08164846dba09848ffe4dede2'
token += '68dbf020972e7eb3312099948d4707fa3c97e2aaa3'

vk_session = vk_api.VkApi(token=token)
vk_session._auth_token()
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

message = 'Привет :)\n\nТы можешь написать мне dog,'
message += ' и я отправлю тебе рандомного пёса!'

helper_message = 'Я не понимаю тебя :('
helper_message += '\n\nПопробуй написать "Привет" или что-то типа того'

allowed_extension = ('jpg','jpeg','png')

greetings = (
    'hi', 'hey', 'howdy', 'hiya', 'yo', 'nice to see you', 'hello',
    'long time no see', 'good day', 'good afternoon', 'good everning', 'хей',
    'привет', 'приветствую', 'добрый день', 'добрый вечер', 'доброе утро',
    'здравствуйте', 'здравствуй', 'рад тебя видеть', 'давно не виделись',
    'сколько лет, сколько зим', 'давненько не виделись', 'хай', 'приуэт'
    )
    
answers = (
    'Держи', 'Держи :)', 'НЫААА', 'НЫААА!!!!!!!!', 'Получайте-с',
    'Получай', 'Получай :)', 'Пёса заказывали?', 'Лови', 'Лови :)',
    'Пёсель доставлен успешно!', 'Пёсель доставлен успешно! :)',
    'Наслаждайся', 'Наслаждайся :)', 'Получите, распишитесь'
    )

dog_names = (
    'dog', 'doggy', 'dogggy', 'пёсель', 'пёс', 'собачка', 'собака',
    'собакен', 'hound', 'pooch', 'псина', 'пес', 'песель', 'дог'
    )
    

def get_url():
    '''Получает URL картинки.'''
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    '''Вызывает get_url(), пока функция не получит картинку.'''
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def bot_random_dog(random_id, token, vk_session):
    '''Обрабатывает принятые сообщения.'''
    for event in longpoll.listen():
        if (event.type == VkEventType.MESSAGE_NEW
            and event.to_me and event.text):
            
            if event.text.lower() in greetings: 
                random_id+=1
                vk.messages.send(
                    random_id=random_id,
                    user_id=event.user_id,
                    message=message
                    )
            elif event.text.lower() in dog_names:
                random_id+=1
                upload = VkUpload(vk_session)
                image_url = get_image_url()
                
                with requests.Session() as session:
                    image = session.get(image_url, stream=True)
                    
                photo = upload.photo_messages(photos=image.raw)[0]
                vk.messages.send(
                    random_id=random_id,
                    user_id=event.user_id,
                    attachment='photo{}_{}'.format(photo['owner_id'],
                    photo['id']),
                    message=answers[randint(0,len(answers)-1)]
                    )
            else:
                random_id+=1
                vk.messages.send(
                    random_id=random_id,
                    user_id=event.user_id,
                    message=helper_message
                    )
                
bot_random_dog(random_id, token, vk_session)
