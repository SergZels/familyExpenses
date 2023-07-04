import matplotlib.pyplot as plt
import datetime
import os.path
from peewee import *
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "botBD.db")
db = SqliteDatabase(db_path)


def diagramBuilder(labels, sizes, monOrYear="місяць"):
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.set_title(f'Витрати за {monOrYear} {sum(sizes)} грн.')
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
        st = "Статистика:\n"
        count = Credet.select().where((Credet.date.year == now.year) & (Credet.date.month == now.month)).count()
        cost = []
        labels = []
        if count > 0:
            for categ in ["Продукти", "Одяг", "Подарунки", "Красота", "Дитині", "Аптека", "Хімія", "Господарство", "Інше"]:
                monthredet = 0
                for i in Credet.select().where((Credet.date.year == now.year) & (
                        Credet.date.month == now.month) & (Credet.category == categ)):
                    monthredet += int(i.cash)

                if monthredet > 0:
                    cost.append(monthredet)
                    labels.append(categ)
                    st += f"{categ} - {monthredet} грн.\n"
                    if categ == "Інше":
                        st += "\nСклад іншого:\n"
                        for i in Credet.select().where(
                                (Credet.date.year == now.year) & (Credet.date.month == now.month) & (
                                        Credet.category == categ)):
                            st += f"{i.description} - {int(i.cash)}грн.\n"

        diagramBuilder(labels, cost)
        st+= f"\nСередні витрати - {str(round(sum(cost)/now.day))} грн. в день"

        return st

    def statLastMounth():
        now = datetime.datetime.now()

        month = now.month
        if month > 1:
            now = now.replace(month=now.month - 1)
        else:
            now = now.replace(month=12, year=now.year - 1)
        st = "Статистика:\n"
        count = Credet.select().where((Credet.date.year == now.year) & (Credet.date.month == now.month)).count()
        cost = []
        labels = []
        if count > 0:
            for categ in ["Продукти", "Одяг", "Подарунки", "Красота", "Дитині", "Аптека", "Хімія", "Господарство",
                          "Інше"]:
                monthredet = 0
                for i in Credet.select().where((Credet.date.year == now.year) & (
                        Credet.date.month == now.month) & (Credet.category == categ)):
                    monthredet += int(i.cash)

                if monthredet > 0:
                    cost.append(monthredet)
                    labels.append(categ)
                    st += f"{categ} - {monthredet} грн.\n"
                    if categ == "Інше":
                        st += "\nСклад іншого:\n"
                        for i in Credet.select().where(
                                (Credet.date.year == now.year) & (Credet.date.month == now.month) & (
                                        Credet.category == categ)):
                            st += f"{i.description} - {int(i.cash)}грн.\n"

        diagramBuilder(labels, cost, monOrYear="минулий місяць")
        st += f"\nСередні витрати - {str(round(sum(cost) / now.day))} грн. в день"

        return st

    def MyYear():
        st = "Статистика:\n"
        now = datetime.datetime.now()
        cost = []
        labels = []
        for categ in ["Продукти", "Одяг", "Подарунки", "Красота", "Дитині", "Аптека", "Хімія", "Господарство",
                      "Інше"]:
            monthredet = 0
            for i in Credet.select().where((Credet.date.year == now.year) & (Credet.category == categ)):
                monthredet += int(i.cash)

            if monthredet > 0:
                cost.append(monthredet)
                labels.append(categ)
                st += f"{categ} - {monthredet} грн.\n"

        diagramBuilder(labels, cost, monOrYear="рік")
        day_count = Credet.select(fn.DATE_TRUNC('day', Credet.date)).where(
            Credet.date.year == now.year
        ).distinct().count()

        st += f"\nСередні витрати - {str(round(sum(cost) / day_count))} грн. в день"
        return st


    def statHTML(self):
        now = datetime.datetime.now()

        count = Credet.select().where((Credet.date.year == now.year) & (Credet.date.month == now.month)).count()

        if count > 0:
            bdMonth = Credet.select().where((Credet.date.year == now.year) & (Credet.date.month == now.month))

            env = Environment(loader=FileSystemLoader(BASE_DIR))

            # Отримайте шаблон за його ім'ям
            template = env.get_template('tamplate.html')

            # Передайте дані з бази даних до шаблону та згенеруйте HTML-вихідний код
            html_output = template.render(db=bdMonth, month=now.month, year=now.year)

            with open('statistic.html', 'w', encoding='utf-8') as file:
                file.write(html_output)
