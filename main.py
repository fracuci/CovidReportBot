import time
import updateManager
import dataManager
import dbManager
import reportManager
import botTools
import datetime


db_connection = dbManager.mongodb_connection().covid19DB
daily_data_rep = dbManager.get_last_report(db_connection)
weekly_data_rep = reportManager.weekly_national_data_report()


while True:

    print("Controllo utenti..")
    updateManager.process_subscription_request(daily_data_rep, weekly_data_rep)
    time.sleep(2)
    #
    # ############# DEVO CONSIDERARE CHE IL TIME DEL BOT È AVANTI DI UN'ORA (NON SO SE SIA
    # ############# IN UTC, ECT O GMT ##############################
    hh, mm, ss = botTools.get_time()
    if hh == 17 and mm == 45 and (ss > 10 and ss < 55):
        print("Sono le "+str(hh)+":"+str(mm)+" .Controllo e aggiorno i dati sul database")
        dataManager.collect_data()
        time.sleep(60) # COOL DOWN PER LE CONNESSIONI AL DB

    hh, mm, ss = botTools.get_time()
    if hh == 18 and mm == 10 and (ss > 10 and ss < 55):
        print("Sono le " + str(hh) + ":" + str(mm) + " .Controllo, aggiorno i report e invio il messaggio brodcast")
        daily_data_rep = reportManager.daily_national_data_report() # aggiorno il report dati giornaliero
        weekly_data_rep = reportManager.weekly_national_data_report()  # aggiorno il report dati settimanali

        users = dbManager.get_all_users(db_connection)
        daily_report_figure = botTools.render_table_img(daily_data_rep) #renderizzo la tabella

        reportManager.report_multiprocessing(users, daily_report_figure, 'daily')

        time.sleep(60) # FINISCO IL MINUTO DI AGGIORNAMENTO E FACCIO COOL DOWN DEI PROCESSI

        if datetime.datetime.today().weekday() == 6:  # controllo se è domenica

            weekly_data_rep = reportManager.weekly_national_data_report() # chiedo i dati settimanali

            #mando il messaggio con l'immagine a tutti gli utenti
            users = dbManager.get_all_users(db_connection)
            weekly_report_figure = botTools.render_image(weekly_data_rep)

            reportManager.report_multiprocessing(users, weekly_report_figure, 'weekly')

            time.sleep(60) # FINISCO IL MINUTO DI AGGIORNAMENTO E FACCIO COOL DOWN DEI PROCESSI

