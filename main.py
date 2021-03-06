import time
import updateManager
import dataManager
import dbManager
import reportManager
import botTools
import datetime


db_connection = dbManager.mongodb_connection().covid19DB

daily_data_rep = dbManager.get_last_report(db_connection)
daily_vaccine_data_rep = dbManager.get_last_report_vaccine(db_connection)
weekly_data_rep = reportManager.weekly_national_data_report()
weekly_anag_vaccini_rep = dbManager.get_last_report_anag_vaccini(db_connection)

while True:

    print("Controllo utenti..")
    updateManager.process_subscription_request(daily_data_rep, weekly_data_rep, daily_vaccine_data_rep,
                                               weekly_anag_vaccini_rep)
    time.sleep(2)
    #
    # ############# DEVO CONSIDERARE CHE IL TIME DEL BOT È AVANTI DI UN'ORA (NON SO SE SIA
    # ############# IN UTC, ECT O GMT ##############################
    hh, mm, ss = botTools.get_time()
    if hh == 17 and mm == 45 and (ss > 10 and ss < 55):
        print("Sono le "+str(hh)+":"+str(mm)+" .Controllo e aggiorno i dati sul database")
        dataManager.collect_data()
        dataManager.collect_vaccine_data()
        # dataManager.collect_anag_vaccine_data()
        time.sleep(60) # COOL DOWN PER LE CONNESSIONI AL DB

    hh, mm, ss = botTools.get_time()
    if hh == 18 and mm == 10 and (ss > 10 and ss < 55):
        print("Sono le " + str(hh) + ":" + str(mm) + " .Controllo, aggiorno i report e invio il messaggio brodcast")
        # dati per report andamento covid
        daily_data_rep = reportManager.daily_national_data_report() # aggiorno il report dati giornaliero
        weekly_data_rep = reportManager.weekly_national_data_report()  # aggiorno il report dati settimanali
        # dati per report andamento vaccini
        daily_data_rep_vaccini = reportManager.daily_national_data_vaccine_report()

        users = dbManager.get_all_users(db_connection)
        # immagine report andamento covid
        daily_report_figure = botTools.render_table_img(daily_data_rep) #renderizzo la tabella
        # immagine report andamento vaccini
        daily_report_figure_vaccini = botTools.render_bar_chart_vaccini(daily_vaccine_data_rep)

        # multi_processing immagini
        reportManager.report_multiprocessing(users, daily_report_figure, daily_report_figure_vaccini, 'daily')

        time.sleep(60) # FINISCO IL MINUTO DI AGGIORNAMENTO E FACCIO COOL DOWN DEI PROCESSI

        if datetime.datetime.today().weekday() == 6:  # controllo se è domenica

            weekly_data_rep = reportManager.weekly_national_data_report() # chiedo i dati settimanali
            weekly_anag_vaccini_rep = dataManager.collect_anag_vaccine_data() #chiedo/aggiorno direttamente dati
            #anagrafica vaccini

            #mando il messaggio con l'immagine a tutti gli utenti
            users = dbManager.get_all_users(db_connection)
            weekly_report_figure = botTools.render_image(weekly_data_rep)
            weekly_anag_vaccini_report_figure = botTools.render_bar_chart_anag_vaccini(weekly_anag_vaccini_rep)

            reportManager.report_multiprocessing(users, weekly_report_figure, weekly_anag_vaccini_report_figure, 'weekly')

            time.sleep(60) # FINISCO IL MINUTO DI AGGIORNAMENTO E FACCIO COOL DOWN DEI PROCESSI

