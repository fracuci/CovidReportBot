import secrets
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

bot_token = secrets.bot_token
############ subscriptionManager elements ###############
bot_message_welcome = 'Welcome'
bot_message_goodbye = 'Goodbye'

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
    ax.plot(data['week_dates'], data['week_rc_sint'])
    ax.plot(data['week_dates'], data['week_ti'])
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    #img = Image.open(buf, mode='r')
    return buf
