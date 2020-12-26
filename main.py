import time
import subscriptionManager
import dataManager
import dbManager
import reportManager
import botTools
import datetime

db_connection = dbManager.mongodb_connection().covid19DB
data_rep = dbManager.get_last_report(db_connection)
db_connection.close
txt_rep = botTools.format_message(data_rep)

while True:

    print("Controllo utenti..")
    subscriptionManager.process_subscription_request(txt_rep)
    time.sleep(3)

    ############# DEVO CONSIDERARE CHE IL TIME DEL BOT È AVANTI DI UN'ORA (NON SO SE SIA
    ############# IN UTC, ECT O GMT ##############################
    hh, mm = botTools.get_time()
    if (hh == 19 and mm == 45):
        print("Sono le "+str(hh)+":"+str(mm)+" .Controllo e aggiorno i dati sul database")
        dataManager.collect_data()


    hh, mm = botTools.get_time()
    if (hh == 20 and mm == 5):
        print("Sono le " + str(hh) + ":" + str(mm) + " .Controllo, aggiorno i report e invio il messaggio brodcast")
        data_rep = reportManager.daily_national_data_report()
        txt_rep = botTools.format_message(data_rep)
        reportManager.report_all_users_text(txt_rep)

        if datetime.datetime.today().weekday() == 6:  # controllo se è domenica
            graph_data = reportManager.weekly_national_data_report() # chiedo i dati settimanali
            img = botTools.render_image(graph_data) #renderizzo l'immagine
            #mando il messaggio con l'immagine a tutti gli utenti
            reportManager.report_users_images(img)