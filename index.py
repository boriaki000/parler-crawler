import sys
sys.path.append('lib')

import json
import os
import requests
import logging
from pytz import timezone, utc
from datetime import datetime
from time import sleep
from googletrans import Translator
from parler import Parler

# Parler
mst = os.environ['PARLER_MST']
jst = os.environ['PARLER_JST']
client = Parler(mst, jst)

# Translator
translator = Translator()
# Other
discord_webhook = os.environ['DISCORD_WEBHOOK']
logger = logging.getLogger()
if os.environ.get('LOG_LEVEL') and os.environ['LOG_LEVEL'] == 'debug':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
retry_count = 3
text_prefix = '```'
default_mode = {
    "src":"en"
    ,"dest":"ja"
}

def handler(event, context):
    user_id = event['user_id']
    user_name = event['user_name']
    time_distance = int(event['time_distance'])
    if event.get('basetime'):
        basetime = datetime.strptime(event['basetime'], '%Y-%m-%d %H:%M:%S')
    else:
        basetime = datetime.now()

    if event.get('timezone'):
        timezone_str = event['timezone']
    else:
        timezone_str = utc.zone
    pytz_timezone = timezone(timezone_str)

    if event.get('trans_mode'):
        trans_mode = event['trans_mode']
    else:
        trans_mode = default_mode

    logger.info('--- PARAM ---')
    logger.info('target_user:' + str(user_name))
    logger.info('basetime:' + str(basetime))
    logger.info('time_distance:' + str(time_distance))
    logger.info('timezone:' + timezone_str)

    result = get_posts(user_id, basetime, time_distance, pytz_timezone, trans_mode)

    if event.get('testmode'):
        logger.debug('test mode >> user name:' + user_name)
        show_test_result(result)
    else:
        post_to_discord(result, user_name)

def get_posts(user_id, basetime, time_distance, pytz_timezone, trans_mode):
    logger.info('START:Get Posts')
    for i in range(0, retry_count):
        try:
            parlerData = client.getPostsOfUserId(user_id, 20)
            result = []
            for post in parlerData['posts']:
                if not post['body'] and post['depth'] != '0':
                    continue

                created_at = datetime.strptime(str(post['createdAt']), '%Y%m%d%H%M%S')
                distance = basetime - created_at
                if distance.days == 0 and distance.seconds < time_distance:
                    text = post['body']
                    if not trans_mode.get('skip_mode'):
                        text = translator.translate('translated:' + text, src=trans_mode['src'], dest=trans_mode['dest']).text
                    result.append({'created_at':str(pytz_timezone.localize(created_at))
                                ,'text':text_prefix + text + text_prefix
                                ,'url':'https://parler.com/post/' + post['_id']})
        except Exception as e:
            logger.warn('Error occurs in get_posts\n')
            logger.warn(str(e) + '\n')
            sleep(i * 5)
        else:
            logger.info('END  :Get Posts')
            return result

    logger.error('get_posts could not be completed. Please rerun for below user id.\n')
    logger.error('user_id >> ' + user_id + '\n') 
    raise Exception('Inner Error')

def post_to_discord(result, user_name):
    logger.info('START:Post to Discord')
    if result:
        result.reverse()
        for item in result:
            call_discord_api(item, user_name)
    logger.info('END  :Post to Discord')

def call_discord_api(item, user_name):
    content = user_name + ' ' + item['created_at'] + '\n' + item['text'] + '\n' + item['url']
    for i in range(0, retry_count):
        try:
            response = requests.post(
                discord_webhook
                ,json.dumps({'content': content})
                ,headers={'Content-Type': 'application/json'}
            )
            if response.status_code != requests.codes['no_content']:
                raise Exception('Webhook returned not expected code >>' + str(response))
        except Exception as e:
            logger.warn('Error occurs in post_to_discord.\n')
            logger.warn(str(e) + '\n')
            sleep(i * 5)
        else:
            logger.info('success!')
            return response

    logger.error('Could not post below content.\n')
    logger.error('user_name >> ' + item['user_name'] + '\n') 
    logger.error('created_at >> ' + item['created_at'] + '\n') 
    raise Exception('Inner Error')

def show_test_result(result):
    logger.debug('test mode')
    if result:
        logger.debug(len(result))
        for res in result:
            logger.debug(res['created_at'])
            logger.debug(res['text'])
            logger.debug(res['url'])
    else:
        logger.debug('no posts')
