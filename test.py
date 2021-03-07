import requests
import dbManager
import csv
import datetime
import botTools
import reportManager
import dataManager
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker
import numpy as np
from PIL import Image
import base64

regioni = ['abruzzo','basilicata','calabria','campania','emiliaromagna','friulivg',
           'lazio','liguria','lombardia','marche','molise','pabolzano','patrento',
           'piemonte','puglia','sardegna','sicilia','toscana','umbria','vaosta','veneto']

#
db_connection =dbManager.mongodb_connection()
#
user = '551420370'
text = """ Fixato bug sull'aggiornamento della data
 """


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
    for d,val in zip(data['dates'],data['rc_sint']):
        axs[0].text(d,val + 10, str(val), fontsize=8)
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
    # buf = io.BytesIO()
    # fig.savefig(buf)
    # buf.seek(0)
    #img = Image.open(buf, mode='r')
    return fig #buf #img.show()#buf


def render_table_img(data_dictionary):
    val1 = ('Giorno: '+data_dictionary['today'], 'Giorno precedente', 'Variazione')
    val2 = ["Ricoverati con sintomi", "Terapia intensiva", "Tot ospedalizzati", "Tot positivi",
            "Nuovi positivi", "Deceduti", "Tamponi", "Percentuale positività"]

    lista = [[str(data_dictionary['ric_sint_oggi']), str(data_dictionary['ric_sint_ieri']),
             str(data_dictionary['delta_ric_sint'])], [str(data_dictionary['terapia_int_oggi']),
             str(data_dictionary['terapia_int_ieri']), str(data_dictionary['delta_terap_int'])],
             [str(data_dictionary['tot_ospedal_oggi']), str(data_dictionary['tot_ospedal_ieri']),
             str(data_dictionary['delta_ospedal'])], [str(data_dictionary['tot_positivi_oggi']),
             str(data_dictionary['tot_positivi_ieri']), str(data_dictionary['delta_tot_positivi'])],
             [str(data_dictionary['nuovi_positivi_oggi']), str(data_dictionary['nuovi_positivi_ieri']),
             str(data_dictionary['delta_nuovi_positivi'])], [str(data_dictionary['deceduti_oggi']),
             str(data_dictionary['deceduti_ieri']), str(data_dictionary['delta_deceduti'])],
             [str(data_dictionary['tamponi_oggi']), " ", " "],[str(data_dictionary['perc_positivita_oggi']), " ", " "]]

    fig, ax = plt.subplots()
    table = plt.table(cellText=lista,
                         rowLabels=val2,
                         rowLoc='right',
                         colLabels=val1,
                         loc='center')

    table[(1, -1)].set_facecolor("#ffff00")
    table[(2, -1)].set_facecolor("#ffff00")
    table[(3, -1)].set_facecolor("#ffff00")
    table[(4, -1)].set_facecolor("#ffff00")
    table[(5, -1)].set_facecolor("#ffff00")
    table[(6, -1)].set_facecolor("#ffff00")
    table[(7, -1)].set_facecolor("#ffff00")
    table[(8, -1)].set_facecolor("#ffff00")
    table[(0,0)].set_facecolor("#00FFFF")
    table[(0,1)].set_facecolor("#00FFFF")
    table[(0, 2)].set_facecolor("#00FFFF")

    ax.set_xticks([])

    ax.set_title('Report giornaliero Covid19 in Italia',
                 fontweight="bold")

    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.box(on=None)
    table.scale(1.2,2)
    pos = ax.get_position()
    pos.x0 = 0.35  # for example 0.2, choose your value
    ax.set_position(pos)
    #fig.tight_layout()
    # buf = io.BytesIO()
    # fig.savefig(buf)
    # buf.seek(0)
    # img = Image.open(buf, mode='r')
    return fig #buf  # img.show()#buf

def buf_image(figure):
    buf = io.BytesIO()
    figure.savefig(buf)
    buf.seek(0)
    return buf

# d = reportManager.daily_national_data_report()
# figure = render_table_img(d)
# buf = botTools.buf_image(figure)
# img = Image.open(buf)
# img.show()
#print(d)

# for i in range(0,3):
#
#     buf = buf_image(figure)
#     reportManager.report_users_images(user, 'test', buf)

# bot_token = botTools.bot_token
# URL_Updates = 'https://api.telegram.org/bot' + bot_token + '/getUpdates'
# update_request = requests.get(url=URL_Updates)
# data = update_request.json()
# print(data)
#
# username = data['result'][0]['message']['from']
#
# if 'username' in username:
#     print('ce')
# else:
#     print('non ce')

print(datetime.datetime.today().weekday())



#dataManager.collect_vaccine_data()
#reportManager.daily_national_data_vaccine_report()
#dataManager.collect_anag_vaccine_data()

# daily_data_rep_vaccini = dbManager.get_last_report_vaccine(db_connection.covid19DB)
weekly_anag_vaccini_rep = dbManager.get_last_report_anag_vaccini(db_connection.covid19DB)
print(weekly_anag_vaccini_rep)

daily_top_region_pos = dbManager.get_last_report_top_reg_nuovi_pos(db_connection.covid19DB)

def render_bar_chart_vaccini(data_dictionary):

    dates = [data_dictionary['yesterday'], data_dictionary['today']]
    dosi_somm = [int(data_dictionary['dosi_naz_somm_ieri']), int(data_dictionary['dosi_naz_somm_oggi'])]
    dosi_cons = [int(data_dictionary['dosi_naz_cons_ieri']), int(data_dictionary['dosi_naz_cons_oggi'])]

    x = np.arange(len(dates))  # the label locations
    width = 0.15# the width of the bars

    fig, ax = plt.subplots()
    ax.bar(x - width/2,dosi_somm, width, label='Dosi somministrate')
    ax.bar(x + width/2,dosi_cons, width, label='Dosi consegnate')
    ax.axhline(y= dosi_somm[1], xmax = 1, linestyle ='--')
    ax.axhline(y= dosi_cons[1], xmax = 1, color= 'orange', linestyle ='--')
    ax.annotate('{0} (+ {1})'.format(dosi_somm[1], dosi_somm[1] - dosi_somm[0]),
                xy=(0.5, dosi_somm[1]), xytext=(0,3),
                textcoords="offset points",
                ha='center', va='bottom')
    ax.annotate('{0} (+ {1})'.format(dosi_cons[1], dosi_cons[1] - dosi_cons[0]),
                xy=(0.5, dosi_cons[1]), xytext=(0, 1),
                textcoords="offset points",
                ha='center', va='bottom')


    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Conteggio')
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-1, 1))
    ax.yaxis.set_major_formatter(formatter)
    ax.set_title('    Report giornaliero dosi somministrate/consegnate')
    ax.set_xticks(x)
    ax.set_xticklabels(dates)
    ax.legend(
               #loc='lower center',
               bbox_to_anchor=(0.5, 0.5, 0.0, 0.0), fontsize='small')

    return fig


def render_bar_chart_anag_vaccini(data_dictionary):

    last_update = data_dictionary['last_update']
    age_range = [k for k in data_dictionary]
    age_range.pop(0)

    prime_dosi = []
    seconde_dosi = []
    totali = []

    for ar in age_range:
        prime_dosi.append(int(data_dictionary[ar]['prima_dose']))
        seconde_dosi.append(int(data_dictionary[ar]['seconda_dose']))
        totali.append(int(data_dictionary[ar]['totale']))

    width = 0.85  # the width of the bars
    fig, ax = plt.subplots()

    print(prime_dosi)
    print(seconde_dosi)
    p_d = ax.bar(age_range, prime_dosi, width, label='Prime dosi', color='springgreen')
    s_d = ax.bar(age_range, seconde_dosi, width, bottom=prime_dosi,  label='Seconde dosi', color='seagreen')


    ax.set_ylabel('Conteggio')
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-1, 1))
    ax.yaxis.set_major_formatter(formatter)
    ax.set_title("        Report settimanale dosi somministrate per fascia d'età")
    ax.legend(loc='upper left')
        #loc='lower center',
        #bbox_to_anchor=(0.5, 0.5, 0.0, 0.0), fontsize='small')

    ax.tick_params(axis='x', rotation=45)

    for i in range(0, len(p_d)):
        height_el_p_d = p_d[i].get_height()
        height_el_s_d = s_d[i].get_height()
        ax.annotate('{:.1f}K'.format(height_el_p_d/1000), xy=(p_d[i].get_x() + p_d[i].get_width()/2,
                    height_el_p_d/2), xytext=(0, 0), textcoords="offset points", ha='center',
                    va='bottom', fontsize=8, fontweight='bold')

        ax.annotate('{:.1f}K'.format(height_el_s_d/1000), xy=(s_d[i].get_x() + s_d[i].get_width()/2,
                    height_el_s_d/2.3 + height_el_p_d), xytext=(0, 0), textcoords="offset points", ha='center',
                    va='bottom', fontsize=8, fontweight='bold')

        ax.annotate('{:.1f}K'.format(totali[i] / 1000), xy=(s_d[i].get_x() + s_d[i].get_width() / 2,
                    height_el_s_d + height_el_p_d + 10000), xytext=(0, 0), textcoords="offset points", ha='center',
                    va='bottom', fontsize=8, fontweight='bold')

    return fig

def format_text_top_5_reg_nuovi_pos(data_dictionary):
    txt = "Report giornaliero\nTop 5 regioni per nuovi positivi (perc. positività):\n"

    for k in data_dictionary:

        s =   "-" + data_dictionary[k]['denom'] + ' '+ str(data_dictionary[k]['nuovi_positivi'])+ \
             ' '+'({:.1%})'.format(data_dictionary[k]['perc_positivita'])+ " \n"

        txt = txt+s
    return txt

    # txt = "Top 5 regioni per nuovi positivi:" \
    # "-" + {}.format + " \n" +
    # "-" + +" \n" +
    # "-" + +" \n" +
    # "-" + +" \n" +
    # "-" + +" \n" +
# figure = render_bar_chart_anag_vaccini(weekly_anag_vaccini_rep)
# buf = botTools.buf_image(figure)
# img = Image.open(buf)
# img.show()


daily_data_rep = dbManager.get_last_report(db_connection.covid19DB)
daily_data_rep_vaccini = dbManager.get_last_report_vaccine(db_connection.covid19DB)
daily_report_figure = botTools.render_table_img(daily_data_rep)
daily_top_region_pos_txt = botTools.format_text_top_5_reg_nuovi_pos(daily_top_region_pos)
daily_report_figure_vaccini = botTools.render_bar_chart_vaccini(daily_data_rep_vaccini)

weekly_anag_vaccini_rep = dbManager.get_last_report_anag_vaccini(db_connection.covid19DB)
weekly_anag_vaccini_report_figure = botTools.render_bar_chart_anag_vaccini(weekly_anag_vaccini_rep)
weekly_data_rep = reportManager.weekly_national_data_report()
weekly_report_figure = botTools.render_image(weekly_data_rep)

users_test = [{'id':551420370}]
users_prod = dbManager.get_all_users(db_connection.covid19DB)
bot_message_update = """
*Aggiornamento Bot:*\n- Da oggi verrà inviato anche il grafico giornaliero sulle vaccinazioni\ne il grafico settimanale che riporta l'andamento delle vaccinazioni per fasce d'età anagrafica\n
E' possibile ricevere questi report anche on demand tramite i comandi inline \n
/andamentovaccinazioni e\n
/anagraficavaccinazionisett\n
- E' stata migliorata la modalità di invio messaggi push e le informazioni contenute in essi\n
Ricordo che è possibile disabilitare i messaggi push dal comando inline\n
/stop\n
continuando comunque ad utilizzare il bot tramite richieste on demand con i suddetti comandi\n

Seguono esempi di grafici disponibili (dati in aggiornamento)\n
Saluti 
"""


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


reportManager.report_multiprocessing(users_prod,'Report settimanale', weekly_report_figure, weekly_anag_vaccini_report_figure, 'weekly')

db_connection.close