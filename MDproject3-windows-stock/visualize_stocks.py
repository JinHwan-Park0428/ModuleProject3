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
        self.by_stock_price()
        self.by_stock_ratio()
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

    def ratio_parse(self, x):
        return float(x.split(' ')[1].replace('(', '').replace(')', '').replace('%', ''))

    def save_data(self):
        show_db = '''SELECT * FROM my_project_stock'''
        self.cursor.execute(show_db)
        data = self.cursor.fetchall()
        pddata = pd.DataFrame(data, columns=["quantity", "price", "days_range", "title", "open_price", "ratio", "search_time", "id"])
        pddata["search_time"] = pddata["search_time"].map(lambda x: self.newtime(x))
        pddata["time_day"] = pddata["search_time"].map(lambda x: self.time_day(x))
        pddata["time_hour"] = pddata["search_time"].map(lambda x: self.time_hour(x))
        pddata["time_minute"] = pddata["search_time"].map(lambda x: self.time_minute(x))
        return pddata

    def by_stock_price(self):
        df = self.save_data()
        deleteSql = """TRUNCATE savestockprice"""
        try:
            time.sleep(1)
            self.cursor.execute(deleteSql)
            print("제거 완료")
            self.connectdb.commit()
        except Exception as e:
            print(e)

        hours = set()
        days = set()
        stocks = set()

        for i in df["time_day"]:
            days.add(i)
        days = list(days)
        days.sort()

        for i in df["time_hour"]:
            hours.add(i)
        hours = list(hours)
        hours.sort()

        for i in df["title"]:
            stocks.add(i)
        stocks = list(stocks)

        for k in stocks:
            for j in days:
                for i in hours:
                    ndata = df[(df["time_hour"] == i) & (df["time_day"] == j) & (df["title"] == k)]
                    ndata = ndata.reset_index()
                    if len(ndata) != 0:
                        fig = plt.figure()
                        ax1 = fig.add_subplot(1, 1, 1)
                        ax1.plot(ndata["price"], marker=r'o', color=u'blue', linestyle='-', label= k)
                        plt.xticks(range(len(ndata["price"])), range(len(ndata["price"])), rotation=0, fontsize="large")
                        ax1.xaxis.set_ticks_position('bottom')
                        ax1.yaxis.set_ticks_position('left')
                        ax1.set_title("{0}th {1}hour {2} Price".format(j, i, k))
                        plt.xlabel('data check')
                        plt.ylabel('price')
                        plt.legend(loc='best')
                        plt.savefig(k+'price'+j+'day'+i+'hour price.png', dpi=400, bbox_inches='tight')
                        savepath = '/static/'+k+'price'+j+'day'+i+'hour price.png'
                        insertSql = 'INSERT INTO savestockprice(stock_title, time_day, time_hour, savepath) VALUES(%s, %s, %s, %s)'
                        try:
                            time.sleep(1)
                            self.cursor.execute(insertSql, (k, j, i, savepath))
                            print("데이터 추가 완료")
                            self.connectdb.commit()
                        except Exception as e:
                            print(e)
                        plt.show()

    def by_stock_ratio(self):
        df = self.save_data()

        deleteSql = """TRUNCATE savestockratio"""
        try:
            time.sleep(1)
            self.cursor.execute(deleteSql)
            print("제거 완료")
            self.connectdb.commit()
        except Exception as e:
            print(e)

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
        ax1.xaxis.set_ticks_position('bottom')
        ax1.yaxis.set_ticks_position('left')
        ax1.set_title("Rate by cryptocurrency")
        plt.xlabel('data check')
        plt.ylabel('ratio')
        plt.legend(loc='best')
        plt.savefig('crypto_ratio_plot.png', dpi=400, bbox_inches='tight')
        savepath = '/static/crypto_ratio_plot.png'
        insertSql = """INSERT INTO savestockratio(datacount, savepath) VALUES(%s, %s)"""
        try:
            time.sleep(1)
            self.cursor.execute(insertSql, (str(len(Bdf)), savepath))
            print("데이터 추가")
            self.connectdb.commit()
        except Exception as e:
            print(e)
        plt.show()


if __name__ == '__main__':
    Mdproject3()
