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
    time.sleep(3)

    ############# DEVO CONSIDERARE CHE IL TIME DEL BOT È AVANTI DI UN'ORA (NON SO SE SIA
    ############# IN UTC, ECT O GMT ##############################
    hh, mm, ss = botTools.get_time()
    if hh == 18 and mm == 45 and (ss > 15 and ss < 19):
        print("Sono le "+str(hh)+":"+str(mm)+" .Controllo e aggiorno i dati sul database")
        dataManager.collect_data()
        time.sleep(60)

    hh, mm, ss = botTools.get_time()
    if hh == 19 and mm == 10 and (ss > 15 and ss < 19):
        print("Sono le " + str(hh) + ":" + str(mm) + " .Controllo, aggiorno i report e invio il messaggio brodcast")
        #daily_data_rep = reportManager.daily_national_data_report() # chiedo i dati giornalieri
        daily_report_image_buf = botTools.render_table_img(daily_data_rep) #renderizzo la tabella
        users = dbManager.get_all_users(db_connection)
        for u in users:
            daily_report_image_buf = botTools.render_table_img(daily_data_rep)
            reportManager.report_users_images(u,'Report giornaliero', daily_report_image_buf)

        daily_report_image_buf = botTools.render_table_img(daily_data_rep)
        daily_report_image_encoded = botTools.encode_image(daily_report_image_buf) #codifico in base64 per il db
        db_connection['last_report'].update_one({'id': 'last_report'}, {'$set': {'image': daily_report_image_encoded}})

        time.sleep(60)

        if datetime.datetime.today().weekday() == 0:  # controllo se è domenica

            weekly_data_rep = reportManager.weekly_national_data_report() # chiedo i dati settimanali
            weekly_report_image_buf = botTools.render_image(weekly_data_rep) #renderizzo l'immagine
            weekly_report_image_encoded = botTools.encode_image(weekly_report_image_buf) #codifico base64 per il db
            db_connection['last_report'].update_one({'id': 'last_report'}, {'$set': {'weekly_image': weekly_report_image_encoded}})
            #mando il messaggio con l'immagine a tutti gli utenti
            users = dbManager.get_all_users(db_connection)
            for u in users:
                weekly_report_image_buf = botTools.render_image(weekly_data_rep)
                reportManager.report_users_images(u, 'Report settimanale', weekly_report_image_buf)
            time.sleep(60)
