import pymysql
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

plt.style.use('ggplot')
connectdb = pymysql.connect(host='localhost', user='root', password='', port=3306, db='mydb', charset='utf8')
cursor = connectdb.cursor()


def Look_db():
    quantity_list = []
    price_list = []
    days_max_list = []
    days_min_list = []
    title_list = []
    search_time_list = []
    new_time_list = []
    show_db = '''SELECT * FROM my_project_md3stock'''
    cursor.execute(show_db)
    data = cursor.fetchone()
    if data != None:
        while data:
            print("\nQuantity: {0}, Price: {1}, Days_range: {2}, Title: {3}, search_time: {4}".format(data[0],
                                                                                                      data[1],
                                                                                                      data[2],
                                                                                                      data[3],
                                                                                                      data[4]))
            quantity_list.append(data[0])
            price_list.append(data[1])
            days_max_list.append(data[2].strip().split(" - ")[1])
            days_min_list.append(data[2].strip().split(" - ")[0])
            title_list.append(data[3])
            search_time_list.append(data[4])
            data = cursor.fetchone()
    else:
        print("\n데이터가 존재하지 않습니다.")

    # print(search_time_list)
    price_index = range(len(price_list[:5]))
    # for i in search_time_list[:5]:
    #     new_time_list.append(datetime.strptime(i, '%Y-%m-%d %H:%M:%S'))

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.bar(price_index, price_list[:5], align='center', color='darkblue')
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_ticks_position('left')
    plt.xticks(price_index, new_time_list, rotation=90, fontsize='small')
    plt.ylim(58500, 59000)
    plt.yticks(np.arange(58500, 59100, 100))

    plt.xlabel('datetime')
    plt.ylabel('Quantity')
    plt.title('BTC Graph')

    # plt.savefig('bar_plot.png', dpi=400, bbox_inches='tight')
    plt.show()


Look_db()
