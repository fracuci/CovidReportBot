from pymongo import MongoClient
import secrets

mongo_user = secrets.mongo_user
mongo_password = secrets.mongo_password
mongo_host = secrets.mongo_host
mongo_db = 'covid19DB'


#################### Manage Connection ###########################
def mongodb_connection():
    client = MongoClient("mongodb+srv://" + mongo_user + ":" + mongo_password + "@" +
                         mongo_host + "/" + mongo_db + "?retryWrites=true&w=majority")

    return client

######################################################################à

################### Manage Users ##################################

def write_newuser_db(db_client_conn, id, username):
    user = {'id': id, 'username': username}
    users = db_client_conn.users
    users.insert_one(user)
    return 'OK'


def remove_user_db(db_client_conn, id):
    users = db_client_conn.users
    users.delete_one({'id': id})
    return 'OK'


def get_user(db_client_conn, id):
    u = db_client_conn.users.find_one({'id': id})
    return u

def get_all_users(db_client_conn):

    users = db_client_conn.users.find()
    return users

##################################################################

##################### Manage update queue offset #################
def get_last_offset(db_client_conn):
    offset = db_client_conn.offset.find_one({'id': 'last_offset'})['value']
    return offset

def update_last_offset(db_client_conn, last_offset):
    offset = db_client_conn.offset.update_one({'id': 'last_offset'}, {'$set': {'value': last_offset}})
    return 'OK'

######################################################################################

########### cache request data and state in DB in order to recover state##############

def get_cached_request(db_client_conn):
    return db_client_conn.request_issue.find_one({'id': 'cache'})

def update_cached_request(db_client_conn, data):
    cache = db_client_conn.request_issue.update_one({'id': 'cache'}, {'$set': {'data': data}})
    return 'OK'

def get_request_issue_state(db_client_conn):
    return db_client_conn.request_issue.find_one({'id': 'trouble'})

def update_request_issue_state(db_client_conn, state):
    new_state = db_client_conn.request_issue.update_one({'id': 'trouble'}, {'$set': {'is_failed': state}})

#########################################################################################

################################### Manage Report Data ###############################

def get_last_report(db_client_conn):

    return db_client_conn['last_report'].find_one({'id': 'last_report'})['data']

################################## Manage Report Images #######################

def get_last_report_image(db_client_conn):

    return db_client_conn['last_report'].find_one({'id': 'last_report'})['image']

def get_last_weekly_report_image(db_client_conn):

    return db_client_conn['last_report'].find_one({'id': 'last_report'})['weekly_image']


#########################################################################################


def get_last_date(db_conn):
    date = db_conn.indices.find({"id":'date'})
    #controllare cosa tira fuori (deve essere l'int associato)
    return date

def write_date(db_conn, date):
    indices = db_conn.indices
    indices.insert_one({"id":"date", "value":date})
    return 'OK'

################################################################################

