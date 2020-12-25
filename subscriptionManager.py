import requests
import dbManager
import botTools

db_connection = dbManager.mongodb_connection().covid19DB

bot_token = botTools.bot_token
bot_message_welcome = botTools.bot_message_welcome
bot_message_goodbye = botTools.bot_message_goodbye

data = None


def cache_update_request(request_data): #cache request in db if something went wrong last time

    up = dbManager.update_cached_request(db_connection, request_data)
    return up


def process_request(data):

    if len(data['result']) > 0:

        last_offset = data['result'][len(data['result'])-1]['update_id'] + 1
        dbManager.update_last_offset(db_connection, last_offset)

        for i in range(0, len(data['result'])):

            is_bot = data['result'][i]['message']['from']['is_bot']
            from_id = data['result'][i]['message']['from']['id']
            username = data['result'][i]['message']['from']['username']
            txt = data['result'][i]['message']['text']

            if is_bot:
                continue
            else: #it is not a bot
                if txt == '/start': #user has sent a "start message"
                    if dbManager.get_user(db_connection, from_id) is None: #check first if user already exists on DB
                        dbManager.write_newuser_db(db_connection, from_id, username)
                        URL_Messages = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' \
                                       + str(from_id) + \
                                       '&parse_mode=Markdown&text=' + bot_message_welcome

                        response = requests.get(URL_Messages)
                        try:# actually.. with Telegram Server when response code is NOT 200..????
                            response.raise_for_status()
                        except requests.exceptions.HTTPError as e:
                            dbManager.update_request_issue_state(db_connection, 1)
                            return 'Error:  ' + str(e)
                    else: #if user already exist skip.. it can be an error of double/multiple start request
                        continue

                if txt == '/stop': #user has sent a "start message"
                    if dbManager.get_user(db_connection, from_id) is None: #user does not exists
                        continue
                    else:
                        dbManager.remove_user_db(db_connection, from_id)
                        URL_Messages = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' \
                                       + str(from_id) + \
                                       '&parse_mode=Markdown&text=' + bot_message_goodbye

                        response = requests.get(URL_Messages)
                        try:# actually.. with Telegram Server when response code is NOT 200..????
                            response.raise_for_status()
                        except requests.exceptions.HTTPError as e:
                            dbManager.update_request_issue_state(db_connection, 1)
                            return 'Error:  '+str(e)
                else: #user has issued a different message
                    continue


def process_subscription_request(URL_Update=None):
    offset = dbManager.get_last_offset(db_connection)
    URL_Updates = 'https://api.telegram.org/bot' + bot_token + '/getUpdates?offset=' + str(offset)

    prev_status = dbManager.get_request_issue_state(db_connection)

    if prev_status == 1:
        data_bak = dbManager.get_cached_request(db_connection)
        process_request(data_bak)

        update_request = requests.get(url=URL_Updates)
        data_curr = update_request.json()
        cache_update_request(data_curr)

        db_connection.close

    else:
        update_request = requests.get(url=URL_Updates)
        data_curr = update_request.json()
        cache_update_request(data)
        process_request(data_curr)

        db_connection.close