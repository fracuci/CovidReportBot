import requests
import dbManager
import csv
import datetime
import botTools
import reportManager
import io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

db_connection.close

