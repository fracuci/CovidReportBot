import requests
import dbManager
import datetime


db_connection = dbManager.mongodb_connection().covid19DB
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

def str_to_list_vaccine(data):
    lines = data.split('\n')
    values = [l.split(',') for l in lines[1:]]

    return values

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


def fill_national_data(data_list, date):

    payload = {}

    payload['date'] = int(date)
    for i in range(0,len(data_list[0])):
        payload[data_list[0][i]] = data_list[1][i]

    #### scrivere in try-except ###
    db_connection.andamento_nazionale.insert_one(payload)


def fill_regional_data(data_list, date):

    for i in range(1, 22):
        payload = {}
        payload['date'] = int(date)

        for j in range(0,len(data_list[0])):
            payload[data_list[0][j]] = data_list[i][j]

        #### scrivere in try-except ###
        db_connection['andamento_'+regioni[i]].insert_one(payload)

def fill_vaccine_data(data_list, date):

    payload = {}
    payload['date'] = int(date)

    for d in data_list:
        regione = d[8]
        if '/' in regione:
            regione = regione.split(' / ')[0]

        payload[regione] = {'dosi_somministrate': d[1], 'dosi_consegnate': d[2], 'percentuale_somministrazione': d[3]}
    db_connection['vaccini'].insert_one(payload)

def collect_data():

    date = datetime.date.today().strftime("%Y%m%d")

    URL_italia = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/' \
                 'dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-' + date + '.csv'

    URL_regioni = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/' \
                  'dati-regioni/dpc-covid19-ita-regioni-' + date + '.csv'

    #chiedo il dato nazionale
    r_italia = requests.get(url=URL_italia)
    #processo e salvo il dato nazionale
    data_italia = str_to_list_national(r_italia.text)
    fill_national_data(data_italia, date)

    #chiedo il dato regione per regione
    r_regioni = requests.get(url=URL_regioni)
    #processo e salvo il dato regione per regione
    data_regioni = str_to_list_region(r_regioni.text)
    fill_regional_data(data_regioni, date)

    db_connection.close

###############à Utilizzare uta tantum per fillare il dataset (alcuni giorni delle regioni #################
#danno errori (saltato 29/10/2020 ############################################################################
def refill_dataset():
    # scrivere funzione per refill unatantum del dataset

    d1 = datetime.date(2020,12,25)  #aggiusta con start-end date
    d2 = datetime.date(2020,12,26)

    dd = [d1+ datetime.timedelta(days=x) for x in range((d2-d1).days + 1)]

    for d in dd:
        temp_date = d.strftime("%Y%m%d")
        print('DAY: '+ temp_date)
        URL_italia = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/' \
                     'dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-' + temp_date + '.csv'

        URL_regioni = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/' \
                      'dati-regioni/dpc-covid19-ita-regioni-' + temp_date + '.csv'

        # chiedo il dato nazionale
        r_italia = requests.get(url=URL_italia)
        # processo e salvo il dato nazionale
        data_italia = str_to_list_national(r_italia.text)
        fill_national_data(data_italia, temp_date)

        # chiedo il dato regione per regione
        r_regioni = requests.get(url=URL_regioni)
        # processo e salvo il dato regione per regione
        data_regioni = str_to_list_region(r_regioni.text)
        fill_regional_data(data_regioni, temp_date)

    db_connection.close



def collect_vaccine_data():

    date = datetime.date.today().strftime("%Y%m%d")
    URL = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/' \
          'vaccini-summary-latest.csv'

    r_vaccine = requests.get(url=URL)
    data_vaccine = str_to_list_vaccine(r_vaccine.text)
    data_vaccine.pop()
    #elaborazione del dato nazionale
    dosi_somministrate_nazionale= 0
    dosi_consegnate_nazionale = 0
    for d in data_vaccine:
        dosi_somministrate_nazionale = dosi_somministrate_nazionale + int(d[1])
        dosi_consegnate_nazionale = dosi_consegnate_nazionale + int(d[2])

    percentuale_somministrazione_nazionale = round(dosi_somministrate_nazionale/dosi_consegnate_nazionale,3)*100
    dato_nazionale = ['ITA', str(dosi_somministrate_nazionale), str(dosi_consegnate_nazionale),
                      str(percentuale_somministrazione_nazionale), str(date),'ITF', 'ITF1', '21', 'Italia']
    # #aggiunta dato nazionale a lista totale
    data_vaccine.append(dato_nazionale)
    #riempiemento del DB
    fill_vaccine_data(data_vaccine, date)

    db_connection.close

def collect_anag_vaccine_data():

    #date = datetime.date.today().strftime("%Y%m%d")
    URL = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/' \
          'anagrafica-vaccini-summary-latest.csv'
    r_anag_vaccine = requests.get(url=URL)

    data_anag_vaccine = str_to_list_vaccine(r_anag_vaccine.text)

    data_anag_vaccine.pop()

    anag_vaccine_dict = {}
    last_update = datetime.date.today().strftime("%d-%m-%Y")
    anag_vaccine_dict['last_update'] = last_update
    for d in data_anag_vaccine:
        anag_vaccine_dict[d[0]] = {'prima_dose': d[len(d)-5], 'seconda_dose': d[len(d)-4], 'guariti': d[len(d)-3],
                                   'terza_dose': d[len(d)-2], 'totale': d[1]}

    db_connection['last_report'].update_one({'id': 'last_report'}, {'$set': {'anag_vaccini': anag_vaccine_dict}})

    db_connection.close

    return anag_vaccine_dict