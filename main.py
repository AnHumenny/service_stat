from time import sleep
from tkinter import messagebox
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
from mysql.connector import connect
from tkinter import *
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from collections import OrderedDict
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import random
import pandas as pd

class Win(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('fttx Гомель')
        self.geometry('1200x700')
        self.date_start = tk.StringVar()
        self.date_end = tk.StringVar()
        self.street_all = tk.StringVar()
        self.temp = None
        self.start_analutic()

    def start_analutic(self):
        for widget in Win.winfo_children(self):
            widget.destroy()
        frame_1 = Frame(self, width=1200)
        frame_1.pack()
        frame_line = Frame(frame_1, relief=SUNKEN, width=1200, height=50)
        frame_line.pack(pady=5)
        my_date_1 = tk.Label(frame_1, width=50, text='Данные по абонентам за период с YYYY-MM-DD')
        my_date_1.pack(pady=5)
        my_date_2 = tk.Entry(frame_1, width=10, textvariable=self.date_start)
        my_date_2.pack(pady=5)
        my_date_3 = tk.Label(frame_1, width=10, text='по ')
        my_date_3.pack(pady=5)
        my_date_4 = tk.Entry(frame_1, width=10, textvariable=self.date_end)
        my_date_4.pack(pady=5)
        button_send_bar = tk.Button(frame_1, text='Посмотреть BAR', width=15, command=self.select_plt_bar)
        button_send_bar.pack(pady=5)
        button_send_barh = tk.Button(frame_1, text='Посмотреть BARH', width=15, command=self.select_plt_barh)
        button_send_barh.pack(pady=5)
        button_send_pie = tk.Button(frame_1, text='Посмотреть PIE', width=15, command=self.select_plt_pie)
        button_send_pie.pack(pady=5)
        button_send_ring = tk.Button(frame_1, text='Посмотреть RING', width=15, command=self.select_plt_ring)
        button_send_ring.pack(pady=5)
        label_line = Label(frame_1,
                           text='В строке, улицы через запятую')
        label_line.pack(pady=5)
        label_entry = Entry(frame_1, textvariable=self.street_all, width=66)
        label_entry.pack(pady=5)
        button_send_line = tk.Button(frame_1, text='Посмотреть LINE', width=15, command=self.select_plt_line)
        button_send_line.pack(pady=5)
        but_ex = tk.Button(frame_1, width=18, text='Выход', command=self.exit_all)
        but_ex.pack(pady=5)

# вертикальная столбчатая, для малого обьёма
    def select_plt_bar(self):
        temp = 'bar'
        street_all = None
        date_start = self.date_start.get()
        date_end = self.date_end.get()
        self.result(temp, date_start, date_end,  street_all)

# горизонтальная столбчатая
    def select_plt_barh(self):
        temp = 'barh'
        street_all = None
        date_start = self.date_start.get()
        date_end = self.date_end.get()
        self.result(temp, date_start, date_end, street_all)

#кольцо проценты
    def select_plt_ring(self):
        temp = 'ring'
        street_all = None
        date_start = self.date_start.get()
        date_end = self.date_end.get()
        self.result(temp, date_start, date_end, street_all)

#круг проценты
    def select_plt_pie(self):
        temp = 'pie'
        street_all = None
        date_start = self.date_start.get()
        date_end = self.date_end.get()
        self.result(temp, date_start, date_end, street_all)

#детальная инфографика по улицам, берёт из .csv
    def select_plt_line(self):
        temp = 'line'
        street_all = self.street_all.get()
        date_start = self.date_start.get()
        date_end = self.date_end.get()
        self.result(temp, date_start, date_end, street_all)

    @staticmethod
    def validate_date(date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def create_csv(self):
        connection = connect(host=os.getenv('host'), port=os.getenv('port'), user=os.getenv('user'),
                               password=os.getenv('password'), database=os.getenv('database'))
        date_start = self.date_start.get()
        date_end = self.date_end.get()
        current_year = date_end[:4]
        query = """
        SELECT TRIM(street) AS street, DATE_FORMAT(date, '%Y-%m') AS month FROM info WHERE date BETWEEN %s AND %s
        """
        cursor = connection.cursor()
        cursor.execute(query, (date_start, date_end))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        df = pd.DataFrame(results, columns=['street', 'month'])
        count_df = df.groupby(['street', 'month']).size().unstack(fill_value=0)
        count_df = count_df.transpose()
        count_df.to_csv(f'{current_year}.csv')
        sleep(1)
        return

    def result(self, temp, date_start, date_end, street_all):
        result_query = dict()
        sorted_street = []
        list_query = []
        set_street = set()
        temp = temp
        year = self.date_end.get()[:4]
        if date_start is None or date_end is None:
            self.start_analutic()
        if not self.validate_date(date_start) or not self.validate_date(date_end):
            messagebox.showinfo("Ошибка", "Неверный формат даты! Используйте YYYY-MM-DD.")
            return
        else:
            try:
                conn = connect(host=os.getenv('host'), port=os.getenv('port'), user=os.getenv('user'),
                               password=os.getenv('password'), database=os.getenv('database'))
                cursor = conn.cursor()
                query_date = "SELECT date, street FROM info WHERE date BETWEEN %s AND %s"
                cursor.execute(query_date, (date_start, date_end))
                result = cursor.fetchall()
                for row in result:
                    set_street.add(row[1].strip())
                print(set_street)
                sorted_street = sorted(set_street)
                for query, row in enumerate(sorted_street):
                    cursor = conn.cursor()
                    query = "SELECT street FROM info WHERE date BETWEEN %s AND %s AND street = %s "
                    cursor.execute(query, (date_start, date_end, row))
                    result = cursor.fetchall()
                    for rows in result:
                        result_query[rows] = result_query.get(rows, 0) + 1  # в словарь result_query
                    list_query = [[key, value] for key, value in result_query.items()]
                    cursor.close()
                conn.close()
            except OSError as err:
                print('Error message', err)
        for widget in self.winfo_children():
            widget.destroy()
            button_resend_date = tk.Button(self, text='Вернутся к вводу данных', command=self.start_analutic)
            button_resend_date.pack()
            plt.minorticks_on()
            plt.grid(which='major')  # включаем основную сетк
            plt.grid(which='minor', linestyle='-.')  # включаем дополнительную сетку
            plt.tight_layout()
            matplotlib.style.use('ggplot')
            plt.minorticks_on()
            fig = matplotlib.pyplot.figure()
            if temp == 'bar':
                d = OrderedDict(sorted(list_query, key=lambda x: x[0]))  # вертикальная диаграмма
                values = list(d.values())  # столбчатая диаграмма
                plt.xlabel('Ось X', labelpad=120)  # Увеличиваем отступ для метки оси X
                axes = plt.subplot(1, 1, 1)
                axes.tick_params(axis='x', labelrotation=35)
                plt.bar(range(len(d)), values, color='purple',
                        tick_label=sorted_street)
            if temp == 'barh':
                d = OrderedDict(sorted(list_query, key=lambda x: x[0]))  # столбчатая диаграмма
                values = list(d.values())  # столбчатая диаграмма
                plt.ylabel('Ось Y', labelpad=120)  # Увеличиваем отступ для метки оси Y
                plt.barh(range(len(d)), values, tick_label=sorted_street)  # горизонтальная диаграмма
            if temp == 'ring':
                list_explode = []
                d = OrderedDict(sorted(list_query, key=lambda x: x[0]))  # круговая диаграмма
                values = list(d.values())
                for row in range(len(list_query)):
                    list_explode.append(round(random.random() / 3, 4))  # случайное расстояние между долями
                fig = matplotlib.pyplot.figure()
                plt.pie(values, labels=sorted_street, autopct='%1.1f%%',
                        explode=list_explode, rotatelabels=False)
            if temp == 'pie':
                list_explode = []
                d = OrderedDict(sorted(list_query, key=lambda x: x[0]))  # кольцевая диаграмма
                values = list(d.values())
                for row in range(len(list_query)):
                    list_explode.append(round(random.random() / 3, 4))  # случайное расстояние между долями
                fig = matplotlib.pyplot.figure()
                plt.pie(values, labels=sorted_street, autopct='%1.1f%%',
                        explode=list_explode, rotatelabels=False, shadow=False, wedgeprops=dict(width=0.5))
            if temp == 'line':
                self.create_csv()
                df_clicks = pd.read_csv(year + '.csv', index_col=0)
                street = street_all.split(', ')
                fig = matplotlib.pyplot.figure()
                for row in street:
                    if row in df_clicks:
                        random_color = ['magenta', 'red', 'yellow', 'black', 'green', 'blue',
                                        'orange', 'blue', 'purple', 'brown']
                        random_marker = ['o', 'D', 's', 'd', '+', '*', 'p', '4', '3', '2', '1', '^', 'v']
                        random_linestyle = ['-', '--', '-.', ':', 'solid', 'dashed', 'dashdot', 'dotted']
                        df_clicks[row].plot(rot=0, figsize=(14, 10), grid=True, marker=random.choice(random_marker),
                                            color=random.choice(random_color),
                                            linestyle=random.choice(random_linestyle), label=row)
                plt.ylabel('количество подключений')
                plt.xlabel('даты подключений')
                plt.legend()

            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.get_tk_widget().pack(fill='both', expand=True)
            canvas.draw()
            toolbarframe = Frame(master=self)
            toolbar = NavigationToolbar2Tk(canvas, toolbarframe)
            toolbarframe.pack()


    def exit_all(self):
        self.quit()
        self.destroy()


if __name__ == "__main__":
    testObj = Win()
    testObj.mainloop()