import secrets
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import datetime
#from PIL import Image ################ TEMPORANEO TOGLIERE!!!

bot_token = secrets.bot_token
############ subscriptionManager elements ###############
bot_message_welcome = """Benvenuto. Questo Bot ti notificherà ogni giorno sull'andamento nazionale dei
dati sul Covid 19. Se non vuoi più ricevere notifiche digita */stop* o utilizza i comandi inline.
*ATTENZIONE* per motivi logistici potrebbe non essere assicurato il servizio il *SABATO* e la *DOMENICA*"""

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

# def render_image(data): #### OLD BUT GOLD
#     fig, ax1 = plt.subplots()
#
#     formatter = mdates.DateFormatter("%m/%d")
#     locator = mdates.DayLocator()
#
#     color = 'tab:red'
#     ax1.xaxis.set_major_formatter(formatter)
#     ax1.xaxis.set_major_locator(locator)
#     ax1.set_ylabel('Ricoverati con sintomi', color=color)
#     ax1.tick_params(axis='y', labelcolor=color)
#     ax1.tick_params(axis='x', rotation=45)
#     ax1.plot(data['dates'], data['rc_sint'], color= color)
#
#     ax2 = ax1.twinx()
#     ax2.xaxis.set_major_formatter(formatter)
#     ax2.xaxis.set_major_locator(locator)
#     color = 'tab:blue'
#     ax2.set_ylabel('Ricoverati terapia intensiva', color=color)
#     ax2.tick_params(axis='y', labelcolor=color)
#     ax2.tick_params(axis='x', rotation=45)
#     ax2.plot(data['dates'], data['ti'], color= color)
#
#     fig.tight_layout()
#     buf = io.BytesIO()
#     fig.savefig(buf)
#     buf.seek(0)
#     #img = Image.open(buf, mode='r')
#     return buf #img.show()#buf

def render_image(data):
    fig, axs = plt.subplots(3)

    formatter = mdates.DateFormatter("%m/%d")
    locator = mdates.DayLocator()

    color = 'tab:orange'
    axs[0].xaxis.set_major_formatter(formatter)
    axs[0].xaxis.set_major_locator(locator)
    axs[0].set_ylabel('Ricoverati con \nsintomi', color=color)
    axs[0].tick_params(axis='y', labelcolor=color)
    axs[0].tick_params(axis='x', rotation=45)
    axs[0].grid(color='b', ls='-.', lw=0.25)
    axs[0].plot(data['dates'], data['rc_sint'], color= color)
    plt.setp(axs[0].get_xticklabels(), visible=False)

    axs[1].xaxis.set_major_formatter(formatter)
    axs[1].xaxis.set_major_locator(locator)
    color = 'tab:red'
    axs[1].set_ylabel('Ricoverati terap\n intensiva', color=color)
    axs[1].tick_params(axis='y', labelcolor=color)
    axs[1].tick_params(axis='x', rotation=45)
    axs[1].grid(color='b', ls='-.', lw=0.25)
    axs[1].plot(data['dates'], data['ti'], color= color)
    plt.setp(axs[1].get_xticklabels(), visible=False)

    axs[2].xaxis.set_major_formatter(formatter)
    axs[2].xaxis.set_major_locator(locator)
    color = 'tab:blue'
    axs[2].set_ylabel('Nuovi positivi', color=color)
    axs[2].tick_params(axis='y', labelcolor=color)
    axs[2].tick_params(axis='x', rotation=45)
    axs[2].grid(color='b', ls='-.', lw=0.25)
    axs[2].plot(data['dates'], data['np'], color= color)

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    #img = Image.open(buf, mode='r')
    return buf #img.show()#buf

def get_time():
    # restituisce ore e minuti
    hh = datetime.datetime.now().hour
    mm = datetime.datetime.now().minute
    ss = datetime.datetime.now().second

    return (hh,mm, ss)
