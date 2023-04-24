import matplotlib.pyplot as plt
import numpy as np
import datetime
import os.path
from peewee import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "botBD.db")
db = SqliteDatabase(db_path)

class Credet(Model):
    category = TextField()
    cash = IntegerField(default=0)
    description = TextField()
    date = DateField(default=datetime.date.today)

    class Meta:
        database = db

class botBDnew():

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        db.create_tables([Credet])

    def recCredet(self, category: str, cash: str, desc: str):
        Credet.create(category=category, cash=cash, description=desc)

    def statNew() -> str:

        now = datetime.datetime.now()
        st = ""
        cash_vudatku = []
        datalabels = []
        fig, ax = plt.subplots()

        count = Credet.select().where((Credet.date.year == now.year) & (Credet.date.month == now.month)).count()
        monthredet = 0

        if count > 0:
            for i in Credet.select().order_by(Credet.category).where((Credet.date.year == now.year) & (Credet.date.month == now.month)):
                monthredet += int(i.cash)
                # cash_vudatku.append(i.cash)
                st += f"{i.date} витратили {i.cash} грн на {i.description}\n"

            st += f"\nВитрати за місяць {monthredet} грн.\n\n"#MAX виручка {max(cash_viruhka)} грн.\nMIN виручка {min(cash_viruhka)} грн.\nСередня виручка {round(mean(cash_viruhka))} грн."
        #
        x = np.arange(len(datalabels))  # the label locations
        width = 0.4  # the width of the bars

        fig, ax = plt.subplots()

        rects = ax.bar(x + width / 2, cash_vudatku, width, label='Витрати')

        ax.set_ylabel('Виручка грн.')
        ax.set_title(f'Виручка за {now.strftime("%m")} місяць!')
        ax.set_xticks(x, datalabels)
        ax.legend()

        # це відступ від тексту до цифри
        ax.bar_label(rects, padding=2)

        fig.tight_layout()

            # plt.show()
        plt.savefig("testplor.png")

        return st

    # def statLastMounth() -> str:
    #
    #     now = datetime.datetime.now()
    #     month = now.month
    #     if month > 1:
    #         now = now.replace(month=now.month - 1)
    #     else:
    #         now = now.replace(month=12, year=now.year - 1)
    #     st = ""
    #     cash_viruhka = []
    #     cash_vudatku = []
    #     datalabels = []
    #     monthcash = 0
    #     cash_todey = 0
    #     fig, ax = plt.subplots()
    #
    #     count = Stat.select().where((Stat.date.year == now.year) & (Stat.date.month == now.month)).count()
    #     if count > 0:
    #         for i in Stat.select().where((Stat.date.year == now.year) & (Stat.date.month == now.month)):
    #             cash = int(i.cashAM) + int(i.cashPM)
    #             monthcash = monthcash + cash
    #             st += f"{i.date} було {cash} грн ({i.cashAM} {i.cashPM})\n"
    #             cash_viruhka.append(cash)
    #             datalabels.append(i.date.strftime("%d"))
    #             try:
    #                 Srd = Credet.get(Credet.date == i.date)
    #             except:
    #                 cash_vudatku.append(0)
    #             else:
    #                 cash_vudatku.append(Srd.cash)
    #
    #         count2 = Credet.select().where((Credet.date.year == now.year) & (Credet.date.month == now.month)).count()
    #         monthredet = 0
    #         st += "\n"
    #         if count2 > 0:
    #             for i in Credet.select().where((Credet.date.year == now.year) & (Credet.date.month == now.month)):
    #                 monthredet += int(i.cash)
    #                 # cash_vudatku.append(i.cash)
    #                 st += f"{i.date} витратили {i.cash} грн на {i.description}\n"
    #
    #         st += f"\nВиручка за місяць {monthcash}\nВитрати за місяць {monthredet}\n\nMAX виручка {max(cash_viruhka)} грн.\nMIN виручка {min(cash_viruhka)} грн.\nСередня виручка {round(mean(cash_viruhka))} грн."
    #
    #         x = np.arange(len(datalabels))  # the label locations
    #         width = 0.4  # the width of the bars
    #
    #         fig, ax = plt.subplots()
    #
    #         rects1 = ax.bar(x - width / 2, cash_viruhka, width, label='Виручка')
    #         rects2 = ax.bar(x + width / 2, cash_vudatku, width, label='Витрати')
    #
    #         ax.set_ylabel('Виручка грн.')
    #         ax.set_title(f'Виручка за {now.strftime("%m")} місяць!')
    #         ax.set_xticks(x, datalabels)
    #         ax.legend()
    #
    #         ax.bar_label(rects1, padding=2)  # це відступ від тексту до цифри
    #         ax.bar_label(rects2, padding=2)
    #
    #         fig.tight_layout()
    #
    #         # plt.show()
    #         plt.savefig("testplor.png")
    #
    #         return st
