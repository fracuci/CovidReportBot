import time
import subscriptionManager
import dataManager
import reportManager
import botTools


while True:

    print("Controllo utenti..")
    subscriptionManager.process_subscription_request()
    time.sleep(3)

    hh, mm = botTools.get_time()
    if (hh == 19 and mm == 45):
        print("Sono le "+str(hh)+":"+str(mm)+" .Controllo e aggiorno i dati sul database")
        dataManager.collect_data()

    hh, mm = botTools.get_time()
    if (hh == 20 and mm == 5):
        print("Sono le " + str(hh) + ":" + str(mm) + " .Controllo e aggiorno i dati sul database")
        data_rep = reportManager.daily_national_data_report()
        txt_rep = botTools.format_message(data_rep)
        reportManager.report_users_text(txt_rep)