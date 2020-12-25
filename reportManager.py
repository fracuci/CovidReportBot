import dbManager
import datetime
import botTools
import requests

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
date = datetime.date.today()
bot_token = botTools.bot_token
regioni = ['abruzzo','basilicata','calabria','campania','emiliaromagna','friulivg',
           'lazio','liguria','lombardia','marche','molise','pabolzano','patrento',
           'piemonte','puglia','sardegna','sicilia','toscana','umbria','vaosta','veneto']


def daily_national_data_report():
    # restituisce un messaggio di testo formattato con i dati di ieri e oggi
    report_data = {'today': date.strftime("Oggi: %d-%m-%Y")}
    today = int(date.strftime("%Y%m%d"))
    yesterday = today-1

    today_query = db_connection.andamento_nazionale.find_one({'date': {'$eq': today}})
    yesterday_query = db_connection.andamento_nazionale.find_one({'date': {'$eq': yesterday}})

    db_connection.close

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

    report_data['perc_positivita_oggi'] = round(100*(report_data['nuovi_positivi_oggi']/report_data['tamponi_oggi']), 3)

    # text_message = botTools.format_message(report_data)
    #
    # return text_message

    return report_data


def weekly_national_data_report():
    # restituisce i dati dell'ultima settimana da plottare
    today = int(date.strftime("%Y%m%d"))
    l_week = int(date.strftime("%Y%m%d")) - 7  # ultima settimana

    lweek_query = db_connection.andamento_nazionale.find({'date': {'$gte': l_week}, 'date': {'$lte': today}})
    db_connection.close

    week_dates = [] #date dell'ultima settimana
    week_rc_sint = [] #ricoverati con sintomi ultima settimana
    week_ti = [] # terapia intensiva ultima settimana
    week_np = [] # nuovi positivi ultima settimana
    week_d = [] #deceduti  ultima settimana

    for el in lweek_query:

        d = datetime.datetime.strptime(str(el['date']),"%Y%m%d")
        week_dates.append(d)
        week_rc_sint.append((el['ricoverati_con_sintomi']))
        week_ti.append((el['terapia_intensiva']))
        week_np.append((el['nuovi_positivi']))
        week_d.append(el['deceduti'])

    week_data = {'dates':week_dates, 'rc_sint':week_rc_sint,'ti':week_ti,
    'np':week_np, 'd':week_d}

    return week_data

def monthly_national_data_report():
    #restituisce i dati dell'ultimo  mese da plottare
    today = int(date.strftime("%Y%m%d"))

    l_month = int(date.strftime("%Y%m%d")) - 30 # ultimo mese

    lmonth_query = db_connection.andamento_nazionale.find({'date': {'$gte': l_month}, 'date': {'$lte':today}})
    db_connection.close

    month_dates = []  # date dell'ultimo mese
    month_rc_sint = []  # ricoverati con sintomi ultimo mese
    month_ti = []  # terapia intensiva ultimo mese
    month_np = []  # nuovi positivi ultimo mese
    month_d = []  # deceduti  ultimo mese

    for el in lmonth_query:

        d = datetime.datetime.strptime(str(el['date']),"%Y%m%d")
        month_dates.append(d)
        month_rc_sint.append((el['ricoverati_con_sintomi']))
        month_ti.append((el['terapia_intensiva']))
        month_np.append((el['nuovi_positivi']))
        month_d.append(el['deceduti'])


    month_data = {'dates':month_dates, 'rc_sint':month_rc_sint,'ti':month_ti,
    'np':month_np, 'd':month_d}

    return month_data



def report_users_text(text_message):
    users = dbManager.get_all_users(db_connection)
    for u in users:
        URL_text_Messages = 'https://api.telegram.org/bot' + botTools.bot_token + '/sendMessage?chat_id=' \
                            + str(u['id']) + \
                                       '&parse_mode=Markdown&text=' + text_message
        requests.get(URL_text_Messages)

    return '200 OK'

def report_users_images(img_message):
    users = dbManager.get_all_users(db_connection)
    for u in users:
        URL_img_Messages = 'https://api.telegram.org/bot' + botTools.bot_token + '/sendPhoto?chat_id=' \
                           + str(u['id'])
        requests.post(URL_img_Messages, files={'photo': img_message}, data={'document': 'photo'})

    return '200 OK'

####################### DA VEDERE SE IN FUTURO SI POTRÀ SCRIVERE QUELLA PER LE REGIONI (SPERIAMO FINISCA #####
###################### TUTTO PRIMA :( ########################################################################
# def daily_regional_status():
#
#     for r in regioni:
#         res = db['andamento_'+r].find_one({'date': {'$eq': date}})
###### da studiare perché l'untente della regione x vorrà solo il report della regione x
###### non di tutte e 20 le regioni (21 perché trentino alto adige è patrenot+pabolzano)


#txt = daily_national_data_report()
#img = render_image(WM_national_data_report())