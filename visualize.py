import pymysql
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime

plt.style.use('ggplot')

class Mdproject3:
    def __init__(self):
        self.connectdb = pymysql.connect(host='jinhwan-instance.cn73pxf4sggf.us-west-2.rds.amazonaws.com',
                                         user='admin',
                                         password='1q2w3e4r5t',
                                         port=3306,
                                         db='mydb',
                                         charset='utf8')
        self.cursor = self.connectdb.cursor()
        # self.save_data()
        self.by_minute_temper()
        self.cursor.close()
        self.connectdb.close()

    def newtime(self, x):
        return x.strftime('%Y-%m-%d %H:%M:%S')

    def time_minute(self, x):
        return x.split(' ')[1].split(".")[0].split(":")[1]

    def time_hour(self, x):
        return x.split(' ')[1].split(".")[0].split(":")[0]

    def time_day(self, x):
        return x.split(' ')[0].split("-")[2]

    def change_temp(self, x):
        x = round((x-32)*(5/9), 1)
        return x
    def delete_per(self, x):
        return int(x.replace("%", ""))


    def save_data(self):
        show_db = '''SELECT * FROM my_project_weather'''
        self.cursor.execute(show_db)
        data = self.cursor.fetchall()
        pddata = pd.DataFrame(data, columns=["temper", "humid", "high_temp", "low_temp", "title", "wind", "weather", "search_time"])
        pddata["search_time"] = pddata["search_time"].map(lambda x: self.newtime(x))
        pddata["time_day"] = pddata["search_time"].map(lambda x: self.time_day(x))
        pddata["time_hour"] = pddata["search_time"].map(lambda x: self.time_hour(x))
        pddata["time_minute"] = pddata["search_time"].map(lambda x: self.time_minute(x))
        pddata["temper"] = pddata["temper"].map(lambda x: self.change_temp(x))
        pddata["humid"] = pddata["humid"].map(lambda x: self.delete_per(x))
        pddata["high_temp"] = pddata["high_temp"].map(lambda x: self.change_temp(x))
        pddata["low_temp"] = pddata["low_temp"].map(lambda x: self.change_temp(x))
        return pddata

    def by_minute_temper(self):
        df = self.save_data()

        # print(df)

        hours = set()
        days = set()
        cities = set()

        for i in df["time_day"]:
            days.add(i)
        days = list(days)
        days.sort()

        for i in df["time_hour"]:
            hours.add(i)
        hours = list(hours)
        hours.sort()

        for i in df["title"]:
            cities.add(i)
        cities = list(cities)
        # print(cities)

        # Sdata = pd.DataFrame()
        # Pdata = pd.DataFrame()
        # Tdata = pd.DataFrame()
        # Ndata = pd.DataFrame()
        # Ldata = pd.DataFrame()

        for i in cities:
            if "Seoul" in i:
                Sdata = df[df["title"] == i]
            elif "To" in i:
                Tdata = df[df["title"] == i]
            elif "Pa" in i:
                Pdata = df[df["title"] == i]
            elif "New" in i:
                Ndata = df[df["title"] == i]
            else :
                Ldata = df[df["title"] == i]

        Sdata = Sdata.reset_index(drop=True)
        Tdata = Tdata.reset_index(drop=True)
        Pdata = Pdata.reset_index(drop=True)
        Ndata = Ndata.reset_index(drop=True)
        Ldata = Ldata.reset_index(drop=True)
        print(Sdata)


        # for k in cities:
        for j in days:
            for i in hours:
                fig = plt.figure()
                ax1 = fig.add_subplot(1, 1, 1)
                ax1.plot(Sdata[(Sdata["time_hour"] == i) & (Sdata["time_day"] == j)]["temper"], marker=r'o', color=u'blue', linestyle='-', label= "Seoul")
                ax1.plot(Tdata[(Tdata["time_hour"] == i) & (Tdata["time_day"] == j)]["temper"], marker=r'o', color=u'red', linestyle='-', label= "Tokyo")
                ax1.plot(Pdata[(Pdata["time_hour"] == i) & (Pdata["time_day"] == j)]["temper"], marker=r'o', color=u'green', linestyle='-', label= "Paris")
                ax1.plot(Ndata[(Ndata["time_hour"] == i) & (Ndata["time_day"] == j)]["temper"], marker=r'o', color=u'yellow', linestyle='-', label= "New York")
                ax1.plot(Ldata[(Ldata["time_hour"] == i) & (Ldata["time_day"] == j)]["temper"], marker=r'o', color=u'pink', linestyle='-', label= "Los Angeles")
                plt.xticks(range(len(Sdata[Sdata["time_hour"]==i]["time_minute"])), Sdata[Sdata["time_hour"]==i]["time_minute"], rotation=0, fontsize="large")
                ax1.xaxis.set_ticks_position('bottom')
                ax1.yaxis.set_ticks_position('left')
                ax1.set_title("{0}th {1}hour temper".format(j, i))
                plt.xlabel('minutes')
                plt.ylabel('temper')
                plt.legend(loc='best')
                # plt.savefig(k+'price'+j+'day'+i+'hour price.png', dpi=400, bbox_inches='tight')
                plt.show()

    def by_stock_ratio(self):
        df = self.save_data()
        Bdf = pd.DataFrame()
        Edf = pd.DataFrame()
        Ldf = pd.DataFrame()
        stocks = set()

        for i in df["title"]:
            stocks.add(i)
        stocks = list(stocks)

        for i in stocks:
            if "Bitcoin" in i:
                Bdf["ratio"] = df["ratio"][df["title"] == i]
            elif "Litecoin" in i:
                Ldf["ratio"] = df["ratio"][df["title"] == i]
            else:
                Edf["ratio"] = df["ratio"][df["title"] == i]

        Bdf["ratio"] = Bdf["ratio"].map(lambda x: self.ratio_parse(x))
        Ldf["ratio"] = Ldf["ratio"].map(lambda x: self.ratio_parse(x))
        Edf["ratio"] = Edf["ratio"].map(lambda x: self.ratio_parse(x))

        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.plot(Bdf["ratio"], marker=r'o', color=u'blue', linestyle='-', label='Bitcoin')
        ax1.plot(Ldf["ratio"], marker=r'+', color=u'red', linestyle='--', label='Litecoin')
        ax1.plot(Edf["ratio"], marker=r'*', color=u'green', linestyle='-.', label='Ethereum')
        plt.yticks(np.arange(-10.0, 10.0, 2.0))
        ax1.xaxis.set_ticks_position('bottom')
        ax1.yaxis.set_ticks_position('left')
        ax1.set_title("Rate by cryptocurrency")
        plt.xlabel('Data volume')
        plt.ylabel('Ratio')
        plt.legend(loc='best')
        plt.savefig('crypto_ratio_plot.png', dpi=400, bbox_inches='tight')
        plt.show()


if __name__ == '__main__':
    Mdproject3()
