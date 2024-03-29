import dbManager
import datetime
import botTools
import requests
import operator
import collections
import multiprocessing
import math

############################################# FUNZIONAMENTO ###########################################################
# Per il messaggio di testo giornaliero deve esser prima chiamata la funz. daily_national_data_report per poi passare #
# i dati generati al botTools.format_message che formatta i dati in un messaggio di testo                             #
# Per il reporto settimanale e mensile (solo grafico) va prima chiamata la weekly_national_data_report o la           #
# monthly_national_data_report che scarica i dati. I dati devono essere poi passati al botTools.render_image          #
# che crea l'immagine come byte-array.                                                                                #
# Il messaggio di testo formattato va infine passato al report_users_text che manda il messaggio di testo mentre      #
# l'immmagine deve essere passata al report_users_images                                                              #
#######################################################################################################################

db_connection = dbManager.mongodb_connection().covid19DB

bot_token = botTools.bot_token
regioni = {'Abruzzo':'abruzzo','Basilicata':'basilicata','Calabria':'calabria','Campania':'campania',
           'Emilia-Romagna':'emiliaromagna','Friuli-Venezia Giulia':'friulivg', 'Lazio':'lazio','Liguria':'liguria',
           'Lombardia':'lombardia','Marche':'marche','Molise':'molise','Provincia Autonoma Bolzano':'pabolzano',
           'Provincia Autonoma Trento':'patrento', 'Piemonte':'piemonte','Puglia':'puglia','Sardegna':'sardegna',
           'Sicilia':'sicilia','Toscana':'toscana','Umbria':'umbria' ,"Valle d'Aosta":'vaosta','Veneto':'veneto'}

##################### Richiesta dati per report Covid giornaliero e settimanale al DB ###############
def daily_national_data_report():

    # restituisce  i dati di ieri e oggi

    today_date = datetime.date.today()
    yesterday_date = today_date - datetime.timedelta(1)

    report_data = {'today': today_date.strftime("%d-%m-%Y")}
    today = int(today_date.strftime("%Y%m%d"))
    yesterday = int(yesterday_date.strftime("%Y%m%d"))

    today_query = db_connection.andamento_nazionale.find_one({'date': {'$eq': today}})
    yesterday_query = db_connection.andamento_nazionale.find_one({'date': {'$eq': yesterday}})



    report_data['ric_sint_oggi'] = int(today_query['ricoverati_con_sintomi'])
    report_data['ric_sint_ieri'] = int(yesterday_query['ricoverati_con_sintomi'])
    report_data['delta_ric_sint'] = report_data['ric_sint_oggi'] - report_data['ric_sint_ieri']

    report_data['terapia_int_oggi'] = int(today_query['terapia_intensiva'])
    report_data['terapia_int_ieri'] = int(yesterday_query['terapia_intensiva'])
    report_data['delta_terap_int'] = report_data['terapia_int_oggi'] - report_data['terapia_int_ieri']

    report_data['tot_ospedal_oggi'] = int(today_query['totale_ospedalizzati'])
    report_data['tot_ospedal_ieri'] = int(yesterday_query['totale_ospedalizzati'])
    report_data['delta_ospedal'] = report_data['tot_ospedal_oggi'] - report_data['tot_ospedal_ieri']

    report_data['tot_positivi_oggi'] = int(today_query['totale_positivi'])
    report_data['tot_positivi_ieri'] = int(yesterday_query['totale_positivi'])
    report_data['delta_tot_positivi'] = report_data['tot_positivi_oggi'] - report_data['tot_positivi_ieri']

    report_data['nuovi_positivi_oggi'] = int(today_query['nuovi_positivi'])
    report_data['nuovi_positivi_ieri'] = int(yesterday_query['nuovi_positivi'])
    report_data['delta_nuovi_positivi'] = report_data['nuovi_positivi_oggi'] - report_data['nuovi_positivi_ieri']

    report_data['deceduti_oggi'] = int(today_query['deceduti'])
    report_data['deceduti_ieri'] = int(yesterday_query['deceduti'])
    report_data['delta_deceduti'] = report_data['deceduti_oggi'] - report_data['deceduti_ieri']

    report_data['tamponi_oggi'] = int(today_query['tamponi']) - int(yesterday_query['tamponi'])

    try:
        report_data['perc_positivita_oggi'] = round(100*(report_data['nuovi_positivi_oggi']/report_data['tamponi_oggi']), 3)

    except Exception as e:

        report_data['perc_positivita_oggi'] = 0

    # text_message = botTools.format_message(report_data)
    #
    # return text_message
    db_connection['last_report'].update_one({'id': 'last_report'}, {'$set': {'data': report_data}})
    db_connection.close

    return report_data


def weekly_national_data_report():
    today_date = datetime.date.today() - datetime.timedelta(1)
    # restituisce i dati dell'ultima settimana da plottare
    today = int(today_date.strftime("%Y%m%d"))
    l_week_date = today_date - datetime.timedelta(21) #int(date.strftime("%Y%m%d")) - 7  # ultima settimana
    l_week = int(l_week_date.strftime("%Y%m%d"))

    lweek_query = db_connection.andamento_nazionale.find({'date': {'$gte': l_week,'$lte': today}})

    db_connection.close

    week_dates = [] #date dell'ultima settimana
    week_rc_sint = [] #ricoverati con sintomi ultima settimana
    week_ti = [] # terapia intensiva ultima settimana
    week_np = [] # nuovi positivi ultima settimana
    week_d = [] #deceduti  ultima settimana

    for el in lweek_query:

        d = datetime.datetime.strptime(str(el['date']),"%Y%m%d")
        week_dates.append(d)
        week_rc_sint.append(int((el['ricoverati_con_sintomi'])))
        week_ti.append(int((el['terapia_intensiva'])))
        week_np.append(int((el['nuovi_positivi'])))
        week_d.append(int(el['deceduti']))

    week_data = {'dates':week_dates, 'rc_sint':week_rc_sint,'ti':week_ti,
    'np':week_np, 'd':week_d}

    return week_data

# def monthly_national_data_report():  ####TO BE ENABLED
#     #restituisce i dati dell'ultimo  mese da plottare
#     today = int(date.strftime("%Y%m%d"))
#
#     l_month = int(date.strftime("%Y%m%d")) - 30 # ultimo mese
#
#     lmonth_query = db_connection.andamento_nazionale.find({'date': {'$gte': l_month}, 'date': {'$lte':today}})
#     db_connection.close
#
#     month_dates = []  # date dell'ultimo mese
#     month_rc_sint = []  # ricoverati con sintomi ultimo mese
#     month_ti = []  # terapia intensiva ultimo mese
#     month_np = []  # nuovi positivi ultimo mese
#     month_d = []  # deceduti  ultimo mese
#
#     for el in lmonth_query:
#
#         d = datetime.datetime.strptime(str(el['date']),"%Y%m%d")
#         month_dates.append(d)
#         month_rc_sint.append((el['ricoverati_con_sintomi']))
#         month_ti.append((el['terapia_intensiva']))
#         month_np.append((el['nuovi_positivi']))
#         month_d.append(el['deceduti'])
#
#
#     month_data = {'dates':month_dates, 'rc_sint':month_rc_sint,'ti':month_ti,
#     'np':month_np, 'd':month_d}
#
#     return month_data

# def report_all_users_text(text_message): ## DEPRECATED
#     users = dbManager.get_all_users(db_connection)
#     for u in users:
#         URL_text_Messages = 'https://api.telegram.org/bot' + botTools.bot_token + '/sendMessage?chat_id=' \
#                             + str(u['id']) + \
#                                        '&parse_mode=Markdown&text=' + text_message
#         requests.get(URL_text_Messages)
#
#     return '200 OK'

# def report_single_user(from_id, img_message): #### DEPRECATED
#
#     URL_img_Messages = 'https://api.telegram.org/bot' + botTools.bot_token + '/sendPhoto?chat_id=' \
#                        + str(from_id)
#     requests.post(URL_img_Messages, files={'photo': img_message}, data={'document': 'photo'})
#
#     return '200 OK'

##################### Richiesta dati per report Vaccini giornaliero e settimanale al DB #################
def daily_national_data_vaccine_report():
    today_date = datetime.date.today()
    yesterday_date = today_date - datetime.timedelta(1)

    report_data = {'today': today_date.strftime("%d-%m-%Y")}
    report_data['yesterday'] = yesterday_date.strftime("%d-%m-%Y")
    today = int(today_date.strftime("%Y%m%d"))
    yesterday = int(yesterday_date.strftime("%Y%m%d"))

    today_query = db_connection.vaccini.find_one({'date': {'$eq': today}})
    yesterday_query = db_connection.vaccini.find_one({'date': {'$eq': yesterday}})

    report_data['dosi_naz_somm_oggi'] = int(today_query['Italia']['dosi_somministrate'])
    report_data['dosi_naz_somm_ieri'] = int(yesterday_query['Italia']['dosi_somministrate'])
    report_data['delta_dosi_naz_somm'] = report_data['dosi_naz_somm_oggi'] - report_data['dosi_naz_somm_ieri']

    report_data['dosi_naz_cons_oggi'] = int(today_query['Italia']['dosi_consegnate'])
    report_data['dosi_naz_cons_ieri'] = int(yesterday_query['Italia']['dosi_consegnate'])
    report_data['delta_dosi_naz_cons'] = report_data['dosi_naz_cons_oggi'] - report_data['dosi_naz_cons_ieri']

    try:
        report_data['perc_somm'] = round(report_data['dosi_naz_somm_oggi'] / report_data['dosi_naz_cons_oggi'], 3)*100

    except Exception as e:

        report_data['perc_somm'] = 0


    db_connection['last_report'].update_one({'id': 'last_report'}, {'$set': {'data_vaccini': report_data}})

    return report_data

def daily_top_region_nuovi_pos():
    today_date = datetime.date.today()
    yesterday_date = today_date - datetime.timedelta(1)

    today = int(today_date.strftime("%Y%m%d"))
    yesterday = int(yesterday_date.strftime("%Y%m%d"))

    perc_pos_regioni = {}
    nuovi_pos_regione = {}


    for k in regioni:
        andamento_regione_oggi = db_connection['andamento_'+regioni[k]].find_one({'date': {'$eq': today}})
        andamento_regione_ieri = db_connection['andamento_' + regioni[k]].find_one({'date': {'$eq': yesterday}})

        if andamento_regione_ieri != None and andamento_regione_oggi!= None:
            diff_tamponi = int(andamento_regione_oggi['tamponi']) - int(andamento_regione_ieri['tamponi'])

            try:
                perc_pos_regioni[regioni[k]] = {'den': k, 'perc_pos':round(100*(int(andamento_regione_oggi['nuovi_positivi'])/diff_tamponi),3)}
            except Exception as e:
                perc_pos_regioni[regioni[k]] = {'den': k, 'perc_pos': 0}

            nuovi_pos_regione[regioni[k]] = int(andamento_regione_oggi['nuovi_positivi'])


    top_regioni = collections.Counter(nuovi_pos_regione).most_common(20)
    top_regioni_dict = {}

    for el in top_regioni:
        top_regioni_dict[el[0]] = {'denom': perc_pos_regioni[el[0]]['den'],'nuovi_positivi': el[1],
                                     'perc_positivita':perc_pos_regioni[el[0]]['perc_pos']/100}

    db_connection['last_report'].update_one({'id': 'last_report'}, {'$set': {'top_5_reg_perc_pos': top_regioni_dict}})
    return top_regioni_dict


def count_vaccinazioni():

    rs = db_connection['last_report'].find_one({'id': 'last_report'})['anag_vaccini']
    age_range = [k for k in rs]
    age_range.pop(0)

    vaccinazioni= {'05-29': {'seconda': 0, 'terza': 0}, '30-59': {'seconda': 0, 'terza': 0}
                   ,'60+': {'seconda': 0, 'terza': 0}}

    for ar in age_range:

        if ar in ('05-11', '12-19', '20-29'):
            vaccinazioni['05-29']['seconda'] += int(rs[ar]['seconda_dose'])
            vaccinazioni['05-29']['terza'] += int(rs[ar]['dose_booster'])
        elif ar in ('30-39', '40-49', '50-59'):
            vaccinazioni['30-59']['seconda'] += int(rs[ar]['seconda_dose'])
            vaccinazioni['30-59']['terza'] += int(rs[ar]['dose_booster'])
        else:
            vaccinazioni['60+']['seconda'] += int(rs[ar]['seconda_dose'])
            vaccinazioni['60+']['terza'] += int(rs[ar]['dose_booster'])

    return vaccinazioni


def count_stats():

    now = datetime.datetime.now()
    #now_test = datetime.datetime.strptime('2021-12-23 19:10:26.938113', '%Y-%m-%d %H:%M:%S.%f')
    today18pm = now.replace(hour=18, minute=0, second=0, microsecond=0)

    if now < today18pm:
        today = datetime.date.today() - datetime.timedelta(1)
        yesterday = today - datetime.timedelta(1)
    else:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(1)

    yesterday_date = int(yesterday.strftime('%Y%m%d'))
    last_year = today - datetime.timedelta(365)
    #last_year_date = int(last_year.strftime('%Y%m%d'))
    last_year_date = 20200901

    rs = list(db_connection['andamento_nazionale'].find({'date': { '$gt': last_year_date}}))
    rs_vaccini = list(db_connection['vaccini'].find({'date': { '$gte': yesterday_date}}))
    platea = db_connection['platea_nazionale'].find_one({'id': 'last'})['platea']

    positivi= {}
    perc_pos = {}
    terap_intens = {}
    deceduti = {}
    vaccini_somministrati = int(rs_vaccini[1]['Italia']['dosi_somministrate']) - int(rs_vaccini[0]['Italia']['dosi_somministrate'])
    vaccini_consegnati = int(rs_vaccini[1]['Italia']['dosi_consegnate']) - int(rs_vaccini[0]['Italia']['dosi_consegnate'])

    vaccini = {'somministrati': vaccini_somministrati, 'consegnati': vaccini_consegnati}


    for i in range(1, len(rs)):
        positivi[datetime.datetime.strptime(str(rs[i]['date']), "%Y%m%d")] = int(rs[i]['nuovi_positivi'])
        terap_intens[datetime.datetime.strptime(str(rs[i]['date']), "%Y%m%d")] = int(rs[i]['terapia_intensiva'])
        try:
            tamponi_i = int(rs[i]['tamponi'])
            tamponi_i_meno_uno = int(rs[i-1]['tamponi'])
            delta_tamponi = tamponi_i - tamponi_i_meno_uno

            deceduti_i = int(rs[i]['deceduti'])
            deceduti_i_meno_uno = int(rs[i-1]['deceduti'])
            delta_deceduti = deceduti_i - deceduti_i_meno_uno

            if delta_tamponi > 0:
                perc_pos[datetime.datetime.strptime(str(rs[i]['date']), "%Y%m%d")] = (int(rs[i]['nuovi_positivi'])/delta_tamponi)*100
            else:
                perc_pos[datetime.datetime.strptime(str(rs[i]['date']), "%Y%m%d")] = 0

            if delta_deceduti > 0:
                deceduti[datetime.datetime.strptime(str(rs[i]['date']), "%Y%m%d")] = delta_deceduti
            else:
                deceduti[datetime.datetime.strptime(str(rs[i]['date']), "%Y%m%d")] = 0

        except Exception:
            perc_pos[datetime.datetime.strptime(str(rs[i]['date']), "%Y%m%d")] = 0

    return (positivi, perc_pos, terap_intens, deceduti, vaccini, platea)


###########################################################################################################à


def report_users_images(user_id, text, img_message):

        #avviso prima che sto mandando l'immagine del report settimanale
        # URL_text_Messages = 'https://api.telegram.org/bot' + botTools.bot_token + '/sendMessage?chat_id=' \
        #                     + str(user_id) + \
        #                     '&parse_mode=Markdown&text='+ text
        # requests.get(URL_text_Messages)

        URL_img_Messages = 'https://api.telegram.org/bot' + botTools.bot_token + '/sendPhoto?chat_id=' \
                           + str(user_id)
        r = requests.post(URL_img_Messages, files={'photo': img_message}, data={'document': 'photo', 'caption':text})
        print(r.text)

        return '200 OK'



def enqueue_process_day(user, txt, figure, figure_vaccine):

    daily_report_image_buf = botTools.buf_image(figure)  # bufferizzo e mando
    report_users_images(str(user), txt, daily_report_image_buf)

    daily_report_image_vaccine_buf = botTools.buf_image((figure_vaccine))
    report_users_images(str(user),'Statistiche ultimo anno e vaccinazioni', daily_report_image_vaccine_buf)

def enqueue_process_week(user,txt, figure, figure_vaccine):

    weekly_report_image_buf = botTools.buf_image(figure)
    report_users_images(str(user), 'Report settimanale', weekly_report_image_buf)

    weekly_report_image_anag_vaccini_buf = botTools.buf_image(figure_vaccine)
    report_users_images(str(user), 'Anagrafica vaccinazioni settimanale\n' +
    'Dose booster: dose di richiamo dopo completamento ciclo vaccinale (terza dose)\n'+
    'Pregressa infezione: diritto a GP per 6 mesi dalla guarigione da Covid 19\n' +
    'fonte: ARS Regione Toscana https://www.ars.toscana.it'
    , weekly_report_image_anag_vaccini_buf)

def report_multiprocessing(users,txt, figure, figure_vaccine, type):
# IMPLEMENTATO MULTI-PROCESSING PER L'INVIO DEI REPORT -> SCALATO DI 1/3 IL TEMPO DI PROCESSING
# https://www.quantstart.com/articles/Parallelising-Python-with-Threading-and-Multiprocessing/

    target = None
    if type == 'daily':
        target = enqueue_process_day
    else:
        target = enqueue_process_week

    jobs = []
    for u in users:
        process = multiprocessing.Process(target=target,
                                          args=(u['id'],
                                                txt, figure, figure_vaccine))
        jobs.append(process)

    i = len(jobs)
    if i < 101:

        for j in jobs:
            j.start()

        for j in jobs:
            j.join()

    else: # NON PIÙ DI 100 PROCESSI SPAWNATI CONTEMPORANEAMENTE!!!!
        ### ES: 341 processi da gestire, molt = 341//100 = 3,
        # da 0 a 99 é 0*100 + 0,1,2.. 99
        # da 100 a 199 é 1*100 + 0,1,2.. 99
        # ..
        # da 300 a 341 é range normale da un numero ad un altro (nell'esempio da 300 a i-1 = 341 [len(jobs) = 342])

        molt = i // 100

        for k in range(0, molt):
            for j in range(0,100): # [0-99]- [100-199] - [200 - 299]... è matematica!!
                jobs[j + k*100].start()

            for j in range(0,100):
                jobs[j + k*100].join()

        for k in range(molt*100, i):
            jobs[k].start()

        for k in range(molt * 100, i):
            jobs[k].join()