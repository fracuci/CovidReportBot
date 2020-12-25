import requests
import dbManager
import csv
import datetime

regioni = ['abruzzo','basilicata','calabria','campania','emiliaromagna','friulivg',
           'lazio','liguria','lombardia','marche','molise','pabolzano','patrento',
           'piemonte','puglia','sardegna','sicilia','toscana','umbria','vaosta','veneto']

#
# update_request = requests.get(url=URL)
# d = update_request.json()
#
# var = d['result'][0]['message']['date']
#
# print(type(var))

# client = dbManager.mongodb_connection()
# #
# db = client.covid19DB
# w = dbManager.write_date(db,'15')
#
# print(w)
#
# res = dbManager.update_last_queue_date(db,'16')
# print(res)
#
# up = dbManager.get_last_date(db)
#
# print(up)

#client.close()

#a = dbManager.db_connection().indices.insert_one({"ciao":"mamma"})

#print(a)

#db.users.find_one()

#print(db.users.find_one({'id': 'idfcidsajnbc'}))



#print(r)



# offset = 255574905
# URL_Updates = 'https://api.telegram.org/bot'+bot_token+'/getUpdates?offset='+str(offset)
# #
# update_request = requests.get(url=URL_Updates)
# #
# data = dbManager.get_cached_request(db)
# # r = dbManager.update_cached_request(db,data)
#
# print(data['data'])
#
# client.close()

##############################################
# def str_to_dict(data):
#     lines = data.split('\n')
#     keys = lines[0].split(',')
#     values_list = [l.split(',') for l in lines[1:]]
#     values = [[k] for k in keys]
#     # print(len(values))
#     # for i in range (0, len(values)):
#     #     print(values[i], i)
#     dictionary = {}
#     for i in range (0,len(values_list)):
#         #print(values_list[i], len(values_list[i]))
#         for j in range(0,len(values_list[i])):
#             if j < 20:
#                 values[j].append(values_list[i][j])
#     for i in range (0,len(values)):
#         dictionary[values[i][0]] = values[i][1:]
#     return dictionary

def str_to_list_region(data):
    lines = data.split('\n')
    keys = lines[0].split(',')
    values = [l for l in lines[1:]] # non posso splittare qui per virgola perché è deleterio per le note :(
    #inizia la pulizia dei values riga per riga :(
    result_list = []
    result_list.append(keys[3:20])
    for v in values:
        elements = v.split(',')
        sub_elements = elements[3:20]
        result_list.append(sub_elements)
    return result_list



#
# date = '20201212'#d1.strftime("%Y%m%d")
#
# URL_regioni = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/' \
#           'dati-regioni/dpc-covid19-ita-regioni-' + date + '.csv'
#
# URL_italia = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/' \
#          'dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-'+date+'.csv'
#
# r = requests.get(url=URL_regioni)
#
# d = str_to_list_region(r.text)
########################à DROP DELLE COLLECTION REGIONI USARE CON PRUDENZA!!! :) #######################
# db_connection = dbManager.mongodb_connection().covid19DB
#
# for i in range(0, len(regioni)):
#
#     try:
#         db_connection.drop_collection('andamento_'+regioni[i])
#     except:
#         continue
#
# db_connection.close

################################################################################################

# client = dbManager.mongodb_connection()
#
# db = client.covid19DB
#
# date = int(datetime.date.today().strftime("%Y%m%d"))
#
# res = db.andamento_nazionale.find_one({'date':{'$eq': date}})
#
# # date = datetime.date.today().strftime("%Y%m%d")
#
# for el in res:
#     print(el)
#
# print(res)
# client.close

# today = datetime.date.today()
#
# l_week = [int(today.strftime("%Y%m%d")) - x for x in range(1,8)]
# print(l_week)