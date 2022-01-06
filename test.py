import math

import requests
import dbManager
import csv
import datetime
import botTools
import reportManager
import dataManager
import io
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates
from matplotlib import ticker
import numpy as np
from PIL import Image
import time

import glob
import base64

regioni = ['abruzzo','basilicata','calabria','campania','emiliaromagna','friulivg',
           'lazio','liguria','lombardia','marche','molise','pabolzano','patrento',
           'piemonte','puglia','sardegna','sicilia','toscana','umbria','vaosta','veneto']

#
db_connection = dbManager.mongodb_connection().covid19DB
#
user = '551420370'
text = """ Fixato bug sull'aggiornamento della data
 """

#
# users_test = [{'id':551420370}]
# users_prod = dbManager.get_all_users(db_connection.covid19DB)
# bot_message_update = """
# *Aggiornamento Bot:*\n- Da oggi verrà inviato anche il grafico giornaliero sulle vaccinazioni\ne il grafico settimanale che riporta l'andamento delle vaccinazioni per fasce d'età anagrafica\n
# E' possibile ricevere questi report anche on demand tramite i comandi inline \n
# /andamentovaccinazioni e\n
# /anagraficavaccinazionisett\n
# - E' stata migliorata la modalità di invio messaggi push e le informazioni contenute in essi\n
# Ricordo che è possibile disabilitare i messaggi push dal comando inline\n
# /stop\n
# continuando comunque ad utilizzare il bot tramite richieste on demand con i suddetti comandi\n
#
# Seguono esempi di grafici disponibili (dati in aggiornamento)\n
# Saluti
# """


# for u in users_test:
#     #print(u, u['id'])
#     URL_Messages = 'https://api.telegram.org/bot' + botTools.bot_token + '/sendMessage?chat_id=' \
#                                        + str(u['id']) + \
#                                        '&parse_mode=Markdown&text=' + bot_message_update
#     r = requests.get(URL_Messages)
#     print(r)



# for u in users_prod:
#     URL_Messages = 'https://api.telegram.org/bot' + botTools.bot_token + '/sendMessage?chat_id=' \
#                                        + str(u['id']) + \
#                                        '&parse_mode=Markdown&text=' + bot_message_update
#     r = requests.get(URL_Messages)
#     print(r)

# reportManager.report_multiprocessing(users_prod, daily_top_region_pos_txt, daily_report_figure,
#                                           daily_report_figure_vaccini, 'daily')


#reportManager.report_multiprocessing(users_prod,'Report settimanale', weekly_report_figure, weekly_anag_vaccini_report_figure, 'weekly')

# weekly_anag_vaccini_rep = dbManager.get_last_report_anag_vaccini(db_connection.covid19DB)
# print(weekly_anag_vaccini_rep)



###################à Eliminare record spurii ##############
# i = db_connection.list_collection_names()
#
# for el in i:
#     if 'andamento' in el:
#         if db_connection[el].find_one({'date': 20211224}) is not None:
#             print(db_connection[el].find_one({'date': 20211224}))
#             db_connection[el].delete_one({'date': 20211224})
#             print('eliminato')
#             print(db_connection[el].find_one({'date': 20211224}))
####################################################################


#stats = reportManager.count_stats()
#vax = reportManager.count_vaccinazioni()


# now = datetime.datetime.now()
# now_2 = datetime.datetime.strptime('2021-12-23 00:10:26.938113', '%Y-%m-%d %H:%M:%S.%f')
# today19pm = now.replace(hour=19, minute=0, second=0, microsecond=0)
# print(now_2)
# print(today19pm)
# print(now_2 < today19pm)

#render_image_stats(stats, vax)
