import pymysql
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
import time

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
        self.by_minute_temper()
        self.temper_with_humid()
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
        x = round((x - 32) * (5 / 9), 1)
        return x

    def delete_per(self, x):
        return int(x.replace("%", ""))

    def save_data(self):
        show_db = '''SELECT * FROM my_project_weather'''
        self.cursor.execute(show_db)
        data = self.cursor.fetchall()
        pddata = pd.DataFrame(data, columns=["temper", "humid", "high_temp", "low_temp", "title", "wind", "weather",
                                             "search_time", "id"])
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

        deleteSql = """TRUNCATE saveweathertemp"""
        try:
            time.sleep(1)
            self.cursor.execute(deleteSql)
            print("제거 완료")
            self.connectdb.commit()
        except Exception as e:
            print(e)

        hours = set()
        days = set()

        for i in df["time_day"]:
            days.add(i)
        days = list(days)
        days.sort()

        for i in df["time_hour"]:
            hours.add(i)
        hours = list(hours)
        hours.sort()

        for j in days:
            for i in hours:
                Sdata = df[(df["time_hour"] == i) & (df["time_day"] == j) & (df["title"] == "Seoul")]
                Sdata = Sdata.reset_index(drop=True)
                Tdata = df[(df["time_hour"] == i) & (df["time_day"] == j) & (df["title"] == "Tokyo")]
                Tdata = Tdata.reset_index(drop=True)
                Pdata = df[(df["time_hour"] == i) & (df["time_day"] == j) & (df["title"] == "Paris")]
                Pdata = Pdata.reset_index(drop=True)
                Ldata = df[(df["time_hour"] == i) & (df["time_day"] == j) & (df["title"] == "Los Angeles")]
                Ldata = Ldata.reset_index(drop=True)
                Ndata = df[(df["time_hour"] == i) & (df["time_day"] == j) & (df["title"] == "New York")]
                Ndata = Ndata.reset_index(drop=True)
                if len(Sdata) != 0:
                    minute_test = set()
                    for k in Sdata["time_minute"]:
                        minute_test.add(k)
                    minute_test = list(minute_test)
                    minute_test.sort()

                    fig = plt.figure()
                    ax1 = fig.add_subplot(1, 1, 1)
                    ax1.plot(Sdata["temper"], marker=r'o', color=u'blue', linestyle='-', label="Seoul")
                    ax1.plot(Tdata["temper"], marker=r'o', color=u'red', linestyle='-', label="Tokyo")
                    ax1.plot(Pdata["temper"], marker=r'o', color=u'green', linestyle='-', label="Paris")
                    ax1.plot(Ndata["temper"], marker=r'o', color=u'yellow', linestyle='-', label="New York")
                    ax1.plot(Ldata["temper"], marker=r'o', color=u'pink', linestyle='-', label="Los Angeles")
                    plt.xticks(range(len(Sdata["temper"])), range(len(Sdata["temper"])), rotation=0,
                               fontsize="large")
                    ax1.xaxis.set_ticks_position('bottom')
                    ax1.yaxis.set_ticks_position('left')
                    ax1.set_title("{0}th {1}hour temper".format(j, i))
                    plt.xlabel('data count')
                    plt.ylabel('temper')
                    plt.legend(loc='best')
                    plt.savefig("{}day {}hour cities's temper.png".format(j, i), dpi=400, bbox_inches='tight')
                    savepath = '/static/'+"{}day {}hour cities's temper.png".format(j, i)
                    insertSql = 'INSERT INTO saveweathertemp(time_day, time_hour, savepath) VALUES(%s, %s, %s)'
                    try:
                        time.sleep(1)
                        self.cursor.execute(insertSql, (j, i, savepath))
                        print("데이터 추가 완료")
                        self.connectdb.commit()
                    except Exception as e:
                        print(e)
                    plt.show()

    def temper_with_humid(self):
        df = self.save_data()

        deleteSql = """TRUNCATE saveweathertempwithhumid"""
        try:
            time.sleep(1)
            self.cursor.execute(deleteSql)
            print("제거 완료")
            self.connectdb.commit()
        except Exception as e:
            print(e)

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

        for i in cities:
            for j in days:
                for k in hours:
                    ndata = df[(df["time_hour"] == k) & (df["time_day"] == j) & (df["title"] == i)]
                    ndata.reset_index(drop=True)
                    if len(ndata) != 0:
                        minute_test = set()
                        for h in ndata["time_minute"]:
                            minute_test.add(h)
                        minute_test = list(minute_test)
                        minute_test.sort()

                        fig, ax1 = plt.subplots()

                        color = 'tab:red'
                        ax1.set_xlabel('data count')
                        ax1.set_ylabel('temper', color=color)
                        ax1.plot(range(len(ndata["temper"])), ndata["temper"], marker=r'*', linestyle="-", color=color)
                        ax1.tick_params(axis='y', labelcolor=color)
                        plt.xticks(range(len(ndata["temper"])), range(len(ndata["temper"])), rotation=0,
                                   fontsize="large")
                        ax1.set_title("{} {}day {}hour temper with humid".format(i, j, k))

                        ax2 = ax1.twinx()
                        color = 'tab:blue'
                        ax2.set_ylabel('humid', color=color)
                        ax2.plot(range(len(ndata["temper"])), ndata["humid"], marker=r'o', linestyle='-', color=color)
                        ax2.set_ylim(bottom=0, top=100)
                        ax2.tick_params(axis='y', labelcolor=color)
                        fig.tight_layout()
                        plt.savefig("{}day {}hour cities's temwhum.png".format(j, k), dpi=400, bbox_inches='tight')
                        savepath = '/static/'+"{}day {}hour cities's temwhum.png".format(j, k)
                        insertSql = 'INSERT INTO saveweathertempwithhumid(title, time_day, time_hour, savepath) VALUES(%s, %s, %s, %s)'
                        try:
                            time.sleep(1)
                            self.cursor.execute(insertSql, (i, j, k, savepath))
                            print("데이터 추가 완료")
                            self.connectdb.commit()
                        except Exception as e:
                            print(e)
                        plt.show()


if __name__ == '__main__':
    Mdproject3()
