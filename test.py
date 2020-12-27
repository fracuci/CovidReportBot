import requests
import dbManager
import csv
import datetime
import botTools
import reportManager
import io
import matplotlib.pyplot as plt
from PIL import Image
import base64

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
db_connection = dbManager.mongodb_connection().covid19DB
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



# d = weekly_national_data_report()
# img = botTools.render_image(d)
#
# report_users_images(img)

# graph_data = reportManager.weekly_national_data_report() # chiedo i dati settimanali
# img = botTools.render_image(graph_data) #renderizzo l'immagine
# #mando il messaggio con l'immagine a tutti gli utenti
# reportManager.report_users_images(img)

# def weekly_national_data_report():
#     # restituisce i dati dell'ultima settimana da plottare
#     today = 20201224#int(date.strftime("%Y%m%d"))
#     l_week = today - 7 #int(date.strftime("%Y%m%d")) - 7  # ultima settimana
#
#     lweek_query = db_connection.andamento_nazionale.find({'date': {'$gte': l_week,'$lte': today}})
#
#     db_connection.close
#
#     week_dates = [] #date dell'ultima settimana
#     week_rc_sint = [] #ricoverati con sintomi ultima settimana
#     week_ti = [] # terapia intensiva ultima settimana
#     week_np = [] # nuovi positivi ultima settimana
#     week_d = [] #deceduti  ultima settimana
#
#     for el in lweek_query:
#
#         d = datetime.datetime.strptime(str(el['date']),"%Y%m%d")
#         week_dates.append(d)
#         week_rc_sint.append(int((el['ricoverati_con_sintomi'])))
#         week_ti.append(int((el['terapia_intensiva'])))
#         week_np.append(int((el['nuovi_positivi'])))
#         week_d.append(int(el['deceduti']))
#
#     week_data = {'dates':week_dates, 'rc_sint':week_rc_sint,'ti':week_ti,
#     'np':week_np, 'd':week_d}
#
#     return week_data
#
# def report_users_images(img_message):
#     users = dbManager.get_all_users(db_connection)
#     for u in users:
#         #avviso prima che sto mandando l'immagine del report settimanale
#         URL_text_Messages = 'https://api.telegram.org/bot' + botTools.bot_token + '/sendMessage?chat_id=' \
#                             + str(551420370) + \
#                             '&parse_mode=Markdown&text='+'Report settimanale monitoraggio Covid19'
#         requests.get(URL_text_Messages)
#
#         URL_img_Messages = 'https://api.telegram.org/bot' + botTools.bot_token + '/sendPhoto?chat_id=' \
#                            + str(u['id'])
#         requests.post(URL_img_Messages, files={'photo': img_message}, data={'document': 'photo'})
#
#     return '200 OK'
#
# graph_data = weekly_national_data_report() # chiedo i dati settimanali
# img = botTools.render_image(graph_data) #renderizzo l'immagine
# # #mando il messaggio con l'immagine a tutti gli utenti
# report_users_images(img)

# def render_table_img(data_dictionary):
#     val1 = ('Dati', 'Giorno: '+data_dictionary['today'], 'Giorno precedente', 'Variazione')
#     val2 = ["Ricoverati con sintomi", "Terapia intensiva", "Tot ospedalizzati", "Tot positivi",
#             "Nuovi positivi", "Deceduti", "Tamponi", "Percentuale positività"]
#
#     lista = [[str(data_dictionary['ric_sint_oggi']), str(data_dictionary['ric_sint_ieri']),
#              str(data_dictionary['delta_ric_sint'])], [str(data_dictionary['terapia_int_oggi']),
#              str(data_dictionary['terapia_int_ieri']), str(data_dictionary['delta_terap_int'])],
#              [str(data_dictionary['tot_ospedal_oggi']), str(data_dictionary['tot_ospedal_ieri']),
#              str(data_dictionary['delta_ospedal'])], [str(data_dictionary['tot_positivi_oggi']),
#              str(data_dictionary['tot_positivi_ieri']), str(data_dictionary['delta_tot_positivi'])],
#              [str(data_dictionary['nuovi_positivi_oggi']), str(data_dictionary['nuovi_positivi_ieri']),
#              str(data_dictionary['delta_nuovi_positivi'])], [str(data_dictionary['deceduti_oggi']),
#              str(data_dictionary['deceduti_ieri']), str(data_dictionary['delta_deceduti'])],
#              [str(data_dictionary['tamponi_oggi']), " ", " "],[str(data_dictionary['perc_positivita_oggi']), " ", " "]]
#
#     fig, ax = plt.subplots()
#
#     table = plt.table(cellText=lista,
#                          rowLabels=val2,
#                          colLabels=val1,
#                          loc='center')
#
#     ax.set_xticks([])
#
#     ax.set_title('Report giornaliero Covid19 in Italia',
#                  fontweight="bold")
#
#     ax = plt.gca()
#     ax.get_xaxis().set_visible(False)
#     ax.get_yaxis().set_visible(False)
#     plt.box(on=None)
#     table.scale(1,1.5)
#     pos = ax.get_position()
#     pos.x0 = 0.25  # for example 0.2, choose your value
#     ax.set_position(pos)
#     fig.tight_layout()
#     buf = io.BytesIO()
#     fig.savefig(buf)
#     buf.seek(0)
#     # img = Image.open(buf, mode='r')
#     return buf  # img.show()#buf
#
# def get_last_report_image(db_client_conn):
#
#     return db_client_conn['last_report'].find_one({'id': 'last_report'})['image']
#
# def encode_image(buf):
#
#     data = io.BytesIO.read(buf)
#     return base64.b64encode(data)
#
# def decode_image(base64file):
#
#     data = base64.b64decode(base64file)
#     buf = io.BytesIO()
#     buf.write(data)
#     buf.seek(0)
#     return buf
#
# data = reportManager.weekly_national_data_report()#dbManager.get_last_report(db_connection)
# buf = botTools.render_image(data)#render_table_img(data)
# enc = encode_image(buf)
# db_connection['last_report'].update_one({'id': 'last_report'}, {'$set': {'weekly_image': enc}})
# data64_from_db = dbManager.get_last_weekly_report_image(db_connection)#get_last_report_image(db_connection)
# buf_from_db = decode_image(data64_from_db)
# img = Image.open(buf_from_db, mode='r')
# img.show()
#
# users = dbManager.get_all_users(db_connection)
# text = 'ORE 22:35 e 22:37 TEST AGGIORNAMENTO PRODUZIONE'
# for u in users:
#         #avviso prima che sto mandando l'immagine del report settimanale
#         URL_text_Messages = 'https://api.telegram.org/bot' + botTools.bot_token + '/sendMessage?chat_id=' \
#                             + str(u['id']) + \
#                             '&parse_mode=Markdown&text='+ text
#         response = requests.get(URL_text_Messages)

bot_token = botTools.bot_token
URL_Updates = 'https://api.telegram.org/bot' + bot_token + '/getUpdates'
update_request = requests.get(url=URL_Updates)
data = update_request.json()
print(data)

username = data['result'][0]['message']['from']

if 'username' in username:
    print('ce')
else:
    print('non ce')

db_connection.close
