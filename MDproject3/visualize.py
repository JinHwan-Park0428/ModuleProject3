import pymysql
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime

plt.style.use('ggplot')

class Mdproject3:
    def __init__(self):
        self.connectdb = pymysql.connect(host='jinhwan-instance.cn73pxf4sggf.us-west-2.rds.amazonaws.com', user='admin', password='1q2w3e4r5t', port=3306, db='mydb',
                                         charset='utf8')
        self.cursor = self.connectdb.cursor()
        # self.barchart()
        self.per_5m_linechart()
        self.cursor.close()
        self.connectdb.close()

    def newtime(self, x):
        return x.strftime('%Y-%m-%d %H:%M:%S')

    def time_minute(self, x):
        return x.split(' ')[1].split(".")[0].split(":")[1]

    def time_hour(self, x):
        return x.split(' ')[1].split(".")[0].split(":")[0]

    def save_data(self):
        show_db = '''SELECT * FROM my_project_stock'''
        self.cursor.execute(show_db)
        data = self.cursor.fetchall()
        pddata = pd.DataFrame(data, columns=["quantity", "price", "days_range", "title", "open_price", "ratio", "search_time"])
        pddata["search_time"] = pddata["search_time"].map(lambda x: self.newtime(x))
        pddata["time_hour"] = pddata["search_time"].map(lambda x: self.time_hour(x))
        pddata["time_minute"] = pddata["search_time"].map(lambda x: self.time_minute(x))

        # print(pddata.sort_values("search_time", ascending=True))
        return pddata

    def barchart(self):
        self.save_data()
        new_time_list = []
        for time in self.search_time_list[:5]:
            new_time_list.append(time.minute)
        price_index = range(len(self.price_list[:5]))

        fig = plt.figure()
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.bar(price_index, self.price_list[:5], align='center', color='darkblue')
        ax1.xaxis.set_ticks_position('bottom')
        ax1.yaxis.set_ticks_position('left')
        plt.xticks(price_index, new_time_list, rotation=0, fontsize='large')
        plt.ylim(58500, 59000)
        plt.yticks(np.arange(58500, 59100, 100))

        plt.xlabel('minutes')
        plt.ylabel('Price')
        plt.title('Data per minute for {}th BTC Price'.format(self.search_time_list[0].day))
        plt.savefig('bar_plot.png', dpi=400, bbox_inches='tight')
        plt.show()

    def per_5m_linechart(self):
        df = self.save_data()
        hours = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]

        for i in hours:
            ndata = df[df["time_hour"] == i]
            if len(ndata) != 0:
                fig = plt.figure()
                ax1 = fig.add_subplot(1, 1, 1)
                ax1.plot(ndata["price"], marker=r'o', color=u'blue', linestyle='-', label='Blue Solid')
                plt.xticks(range(len(ndata["time_minute"])), ndata["time_minute"], rotation=0, fontsize="large")
                ax1.xaxis.set_ticks_position('bottom')
                ax1.yaxis.set_ticks_position('left')

                ax1.set_title("Data per 5min for {}O'clock BTC Price".format(i))
                plt.xlabel('minutes')
                plt.ylabel('price')
                # plt.legend(loc='best')

                plt.savefig('line_plot' +i+ '.png', dpi=400, bbox_inches='tight')
                plt.show()


if __name__ == '__main__':
    Mdproject3()
