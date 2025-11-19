import os
import random
from collections import OrderedDict
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd

import tkinter as tk
from tkinter import *
from tkinter import messagebox

from dotenv import load_dotenv
from mysql.connector import connect

load_dotenv()


class DatabaseConfig:
    """Database configuration with environment variables fallback."""

    def __init__(self):
        self.host = os.getenv('DB_HOST', 'HOST')
        self.port = int(os.getenv('DB_PORT', '3306'))
        self.user = os.getenv('DB_USER', 'USER')
        self.password = os.getenv('DB_PASSWORD', 'PASSWORD')
        self.database = os.getenv('DB_NAME', 'DATABASE')

    @property
    def connection_dict(self):
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database,
        }

DB_CONFIG = DatabaseConfig()


class Win(tk.Tk):
    """Main application window for FTTX data analysis.

    Provides GUI for viewing and analyzing FTTX-related data with date range
    selection and street filtering capabilities.
    """
    def __init__(self, *args, **kwargs):
        """Initialize the main application window.

        Sets up window properties, initializes variables, and starts the UI.
        """
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('FTTX data')
        self.geometry('1200x700')
        self.date_start = tk.StringVar()
        self.date_end = tk.StringVar()
        self.street_all = tk.StringVar()
        self.temp = None
        self.start_analutic()


    def start_analutic(self):
        """Start window"""

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


    def select_plt_bar(self):
        """Vertical graph."""

        temp = 'bar'
        street_all = None
        date_start = self.date_start.get()
        date_end = self.date_end.get()
        self.result(temp, date_start, date_end,  street_all)


    def select_plt_barh(self):
        """Horizontal graph"""

        temp = 'barh'
        street_all = None
        date_start = self.date_start.get()
        date_end = self.date_end.get()
        self.result(temp, date_start, date_end, street_all)


    def select_plt_ring(self):
        """Ring graph with percent."""

        temp = 'ring'
        street_all = None
        date_start = self.date_start.get()
        date_end = self.date_end.get()
        self.result(temp, date_start, date_end, street_all)


    def select_plt_pie(self):
        """Pie graph with percent"""

        temp = 'pie'
        street_all = None
        date_start = self.date_start.get()
        date_end = self.date_end.get()
        self.result(temp, date_start, date_end, street_all)


    def select_plt_line(self):
        """Detailed street infographics, taken from .csv"""

        temp = 'line'
        street_all = self.street_all.get()
        date_start = self.date_start.get()
        date_end = self.date_end.get()
        self.result(temp, date_start, date_end, street_all)


    @staticmethod
    def validate_date(date_text):
        """Date validation."""

        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False


    def create_csv(self):
        """Create CSV file with street data aggregated by month."""

        date_start = self.date_start.get()
        date_end = self.date_end.get()
        current_year = date_end[:4]

        query = """
            SELECT 
                DATE_FORMAT(date, '%Y-%m') AS month,
                TRIM(street) AS street,
                COUNT(*) as count
            FROM info 
            WHERE date BETWEEN %s AND %s
            GROUP BY month, street
            ORDER BY month, street
        """

        try:
            with connect(**DB_CONFIG.connection_dict) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (date_start, date_end))
                    results = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]

            df = pd.DataFrame(results, columns=columns)

            count_df = df.pivot_table(
                index='month',
                columns='street',
                values='count',
                fill_value=0
            )

            filename = f'{current_year}.csv'
            count_df.to_csv(filename)
            return filename

        except Exception as e:
            print(f"Error creating CSV: {e}")
            return None


    def result(self, temp, date_start, date_end, street_all):
        """Process data and generate visualization based on selected chart type."""

        if not date_start or not date_end:
            self.start_analutic()
            return

        if not self.validate_date(date_start) or not self.validate_date(date_end):
            messagebox.showinfo("Ошибка", "Неверный формат даты! Используйте YYYY-MM-DD.")
            return

        try:
            with connect(**DB_CONFIG.connection_dict) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT street, COUNT(*) as count FROM info WHERE "
                        "date BETWEEN %s AND %s GROUP BY street",
                        (date_start, date_end)
                    )
                    results = cursor.fetchall()

            list_query = [[row[0].strip(), row[1]] for row in results]
            sorted_street = sorted([row[0] for row in results])

        except Exception as err:
            messagebox.showerror("Ошибка", f"Database error: {err}")
            return

        for widget in self.winfo_children():
            widget.destroy()

        button_resend_date = tk.Button(self, text='Вернутся к вводу данных', command=self.start_analutic)
        button_resend_date.pack()

        matplotlib.style.use('ggplot')
        plt.minorticks_on()
        plt.grid(which='major')
        plt.grid(which='minor', linestyle='-.')
        plt.tight_layout()

        fig = plt.figure()

        if temp in ['bar', 'barh']:
            d = OrderedDict(sorted(list_query, key=lambda x: x[0]))
            values = list(d.values())

            if temp == 'bar':
                plt.bar(range(len(d)), values, color='purple', tick_label=sorted_street)
                plt.xlabel('Ось X', labelpad=120)
                plt.xticks(rotation=35)

            else:
                plt.barh(range(len(d)), values, tick_label=sorted_street)
                plt.ylabel('Ось Y', labelpad=120)

        elif temp in ['pie', 'ring']:
            d = OrderedDict(sorted(list_query, key=lambda x: x[0]))
            values = list(d.values())
            list_explode = [round(random.random() / 3, 4) for _ in range(len(list_query))]

            if temp == 'ring':
                plt.pie(values, labels=sorted_street, autopct='%1.1f%%', explode=list_explode)
            else:
                plt.pie(values, labels=sorted_street, autopct='%1.1f%%',
                        explode=list_explode, wedgeprops=dict(width=0.5))

        elif temp == 'line':
            self.create_csv()
            year = date_end[:4]
            df_clicks = pd.read_csv(f'{year}.csv', index_col=0)
            street = street_all.split(', ')

            colors = ['magenta', 'red', 'yellow', 'black', 'green', 'blue', 'orange', 'purple', 'brown']
            markers = ['o', 'D', 's', 'd', '+', '*', 'p', '^', 'v']
            linestyles = ['-', '--', '-.', ':']

            for row in street:
                if row in df_clicks:
                    df_clicks[row].plot(rot=0, figsize=(14, 10), grid=True,
                                        marker=random.choice(markers),
                                        color=random.choice(colors),
                                        linestyle=random.choice(linestyles),
                                        label=row)

            plt.ylabel('количество подключений')
            plt.xlabel('даты подключений')

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.draw()

        toolbarframe = Frame(master=self)
        NavigationToolbar2Tk(canvas, toolbarframe)
        toolbarframe.pack()

    def exit_all(self):
        self.quit()
        self.destroy()


if __name__ == "__main__":
    testObj = Win()
    testObj.mainloop()
