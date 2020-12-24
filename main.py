# import schedule
# import requests
# import time
import subscriptionManager
import dataManager

# schedule.every().day.at("22:47").do(report)


def main():

    print("Controllo nuovi utenti e utenti che si de-registrano")
    subscriptionManager.process_subscription_request() #bisogna scrivere lo scheduler che ogni x tempo controlla i nuovi iscritti
    #bisogna scrivere lo scheduler che, se sono le 18.30 fa il bollettino
    # e lo invia a tutti gli iscritti

    print("Ho finito di controllare gli utenti.. se sono le 18 passo ai dati")

    print("Inizio a controllare i nuovi dati")
    #dataManager.collect_data()
    print("Ho finito di controllare i nuovi dati")


if __name__ == "__main__":
    main()


# while True:
#     schedule.run_pending()
#     time.sleep(1)
