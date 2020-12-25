import secrets
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import datetime

bot_token = secrets.bot_token
############ subscriptionManager elements ###############
bot_message_welcome = """Benvenuto. Questo Bot ti notificherà ogni giorno sull'andamento nazionale dei dati sul Covid 19. Se non vuoi più ricevere notifiche digita */stop*.
                         *ATTENZIONE* per motivi logistici non è assicurato il servizio il _sabato_ e la _domenica_"""

bot_message_goodbye = """Sei stato eliminato dalla lista degli utenti. Non riceverai più notifiche sull'andamento nazionale dei dati sul Covid 19. Arrivederci!"""

############# reportManager elements ###################

def format_message(data_dictionary):

    message = """
     Report giornaliero Covid19 in Italia \n"""+\
    """| *Dati* | *""" + data_dictionary['today'] + """* | *Ieri* | *Variazione* | \n""" + \
    "| ------ | -------------------------- | ----- | ----------------- | \n"+ \
    "| Ricoverati con sintomi | " + str(data_dictionary['ric_sint_oggi']) + " | " + str(data_dictionary['ric_sint_ieri']) + " | " + str(data_dictionary['delta_ric_sint']) + " | \n" + \
    "| Terapia intensiva | " + str(data_dictionary['terapia_int_oggi']) + " | " + str(data_dictionary['terapia_int_ieri']) + " | " + str(data_dictionary['delta_terap_int']) + " | \n" + \
    "| Tot ospedalizzati | " + str(data_dictionary['tot_ospedal_oggi']) + " | " + str(data_dictionary['tot_ospedal_ieri']) + " | " + str(data_dictionary['delta_ospedal']) + " | \n" + \
    "| Tot positivi | " + str(data_dictionary['tot_positivi_oggi']) + " | " + str(data_dictionary['tot_positivi_ieri']) + " | " + str(data_dictionary['delta_tot_positivi']) + " | \n" + \
    "| Nuovi positivi | " + str(data_dictionary['nuovi_positivi_oggi']) + " | " + str(data_dictionary['nuovi_positivi_ieri']) + " | " + str(data_dictionary['delta_nuovi_positivi']) + " | \n" + \
    "| Deceduti | " + str(data_dictionary['deceduti_oggi']) + " | " + str(data_dictionary['deceduti_ieri']) + " | " + str(data_dictionary['delta_deceduti']) + " | \n" + \
    "| Tamponi | " + str(data_dictionary['tamponi_oggi']) + " |  |  | \n" + \
    "| *Percentuale positività*  | " + str(data_dictionary['perc_positivita_oggi']) + "% |  |  | \n"

    return message


def render_image(data):
    fig, ax = plt.subplots()
    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(formatter)
    locator = mdates.DayLocator()
    ax.xaxis.set_major_locator(locator)
    ax.plot(data['dates'], data['rc_sint'])
    ax.plot(data['dates'], data['ti'])
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    #img = Image.open(buf, mode='r')
    return buf

def get_time():
    # restituisce ore e minuti
    hh = datetime.datetime.now().hour
    mm = datetime.datetime.now().minute

    return (hh,mm)
