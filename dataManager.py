import requests
import dbManager
import datetime


db_connection = dbManager.mongodb_connection().covid19DB
date = datetime.date.today().strftime("%Y%m%d")
regioni = ['fuffa', 'abruzzo','basilicata','calabria','campania','emiliaromagna','friulivg',
           'lazio','liguria','lombardia','marche','molise','pabolzano','patrento',
           'piemonte','puglia','sardegna','sicilia','toscana','umbria','vaosta','veneto']
#fuffa serve ad allinearsi ai dati scaricati :'D

def str_to_list_national(data):
    lines = data.split('\n')
    keys = lines[0].split(',')
    values = [l for l in lines[1:]] # non posso splittare qui per virgola perché è deleterio per le note :(
    #inizia la pulizia dei values riga per riga :(
    result_list = []
    result_list.append(keys[2:16])
    for v in values:
        elements = v.split(',')
        sub_elements = elements[2:16]
        result_list.append(sub_elements)
    return result_list

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


# def refill_dataset(data, start_date, end_date):
#     pass
#     # scrivere funzione per refill unatantum del dataset
#
#     d1 = datetime.date(2020,2,24)  #aggiusta con start-end date
#     d2= datetime.date(2020,11,22)
#
#     dd = [d1+ datetime.timedelta(days=x) for x in range((d2-d1).days + 1)]
#
#     for d in dd:
#         date = d1.strftime("%Y%m%d")
#
#         URL = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/' \
#           'dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-' + date + '.csv'
#
#         r = requests.get(url=URL)
#
#     db.andamento_nazionale.insert_one(r)
#     client.close()


def fill_national_data(data_list):

    payload = {}

    payload['date'] = int(date)
    for i in range(0,len(data_list[0])):
        payload[data_list[0][i]] = data_list[1][i]

    #### scrivere in try-except ###
    db_connection.andamento_nazionale.insert_one(payload)


def fill_regional_data(data_list):

    for i in range(1, 22):
        payload = {}
        payload['date'] = int(date)

        for j in range(0,len(data_list[0])):
            payload[data_list[0][j]] = data_list[i][j]

        #### scrivere in try-except ###
        db_connection['andamento_'+regioni[i]].insert_one(payload)


def collect_data():

    URL_italia = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/' \
                 'dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-' + date + '.csv'

    URL_regioni = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/' \
                  'dati-regioni/dpc-covid19-ita-regioni-' + date + '.csv'

    #chiedo il dato nazionale
    r_italia = requests.get(url=URL_italia)
    #processo e salvo il dato nazionale
    data_italia = str_to_list_national(r_italia.text)
    fill_national_data(data_italia)

    #chiedo il dato regione per regione
    r_regioni = requests.get(url=URL_regioni)
    #processo e salvo il dato regione per regione
    data_regioni = str_to_list_region(r_regioni.text)
    fill_regional_data(data_regioni)

    db_connection.close