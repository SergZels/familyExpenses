import matplotlib.pyplot as plt
import datetime
import os.path
from peewee import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "botBD.db")
db = SqliteDatabase(db_path)

def diagramBuilder(labels, sizes):
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.set_title(f'Витрати за місяць {sum(sizes)} грн.')
    plt.savefig("testplor.png")

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

    def statNew():

        now = datetime.datetime.now()
        st = ""
        count = Credet.select().where((Credet.date.year == now.year) & (Credet.date.month == now.month)).count()
        cost = []
        if count > 0:
            for categ in ["Продукти", "Одяг", "Подарунки", "Красота", "Дитині", "Аптека", "Інше"]:
                monthredet = 0
                for i in Credet.select().where((Credet.date.year == now.year) & (Credet.date.month == now.month) & (Credet.category == categ)):
                    monthredet += int(i.cash)
                cost.append(monthredet)
                st+=f"{categ} - {monthredet} грн.\n"

        labels = "Продукти", "Одяг", "Подарунки", "Красота", "Дитині", "Аптека", "Інше"
        diagramBuilder(labels, cost)
        return st
