import time
import mysql.connector
import datetime
from . import dates
import multiprocessing
import sqlite3


modes = ['mysql', 'sqlite']

class SQL_Class:

    def __init__(self, mode='mysql'):
        self.mode = mode
        self.db = None
        self.cursor = None
        self.tabels = []
        self.database = ''
        self.host = 'localhost'
        self.user = ''
        self.password = ''

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def login(self, user:str='', password:str='', database:str='', tables:list='', host_name:str = 'localhost'):
        self.host = host_name
        self.password = password
        self.user = user
        self.database = database
        self.tabels = tables
        if self.mode == modes[0]:
            self.connect_mysql()
        if self.mode == modes[1]:
            self.connect_sqlite()

    def connect_mysql(self):
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.db.cursor()

    def connect_sqlite(self):
        self.db = sqlite3.connect(self.database)
        self.cursor = self.db.cursor()

    def ifconnected(self):
        if self.cursor == '':
            return False
        else:
            return True

    def reset_auto_increment(self):
        self.Execute_SQL_Command(f'ALTER TABLE `{self.database}`.`{self.tabels[0]}`  AUTO_INCREMENT = 1')
        self.db.commit()

    def clear_table(self):
        self.Execute_SQL_Command(f'DELETE FROM `{self.database}`.`{self.tabels[0]}`')
        self.db.commit()

    def basic_read(self, tabels=None, *args, **kwargs):
        if not self.ifconnected():
            raise NotConnected
        if tabels is None:
            tabels = [x for x in self.tabels]
        for x in range(len(tabels)):
            tabels[x] = f'{self.database}.{tabels[x]}'
        tabels_str = ', '.join(tabels)
        if len(args) == 0:
            select = '*'
        else:
            select = ', '.join(args)
        elements = []
        for x in kwargs:
            elements.append(f"{x} = '{kwargs[x]}'")
        elements = ' and '.join(elements)
        if elements == '':
            Abfrage = f'SELECT {select} FROM {tabels_str}'
        else:
            Abfrage = f'SELECT {select} FROM {tabels_str} WHERE {elements}'
        Return = self.Execute_SQL_Command(Abfrage)
        return Return


    def basic_write(self, tabels=None, **kwargs):
        if not self.ifconnected():
            raise NotConnected
        if tabels is None:
            tabels = [x for x in self.tabels]
        for x in range(len(tabels)):
            tabels[x] = f'{self.database}.{tabels[x]}'
        tabels_str = tabels[0]
        colums = []
        for x in kwargs:
            colums.append(x)
        values = []
        for x in kwargs:
            values.append(kwargs[x])
        for x in range(len(values)):
            values[x] = f"'{values[x]}'"
        colums = ', '.join(colums)
        values = ', '.join(values)
        Abfrage = f'INSERT INTO {tabels_str} ({colums}) VALUES ({values})'
        self.Execute_SQL_Command(Abfrage)
        self.db.commit()

    def basic_delete(self, tabels=None, **kwargs):
        if tabels is None:
            tabels = [x for x in self.tabels]
        for x in range(len(tabels)):
            tabels[x] = f'{self.database}.{tabels[x]}'
        print(tabels)
        tabels_str = tabels[0]
        elements = list()
        for x in kwargs:
            elements.append(f"{x} = '{kwargs[x]}'")
        elements = ' and '.join(elements)
        Abfrage = f'DELETE FROM {tabels_str} WHERE {elements}'
        self.Execute_SQL_Command(Abfrage)
        self.db.commit()

    def Execute_SQL_Command(self, command:str):
        print(command)
        self.cursor.execute(command)
        return self.cursor.fetchall()


class NotConnected(Exception):

    pass
class auto_delete():

    def __init__(self, tabel:str, colum:str, Buffertime:list, SQL:SQL_Class = None): # Buffertime: [name:(days, months, years, minutes, seconds, hours), time:int]
        self.SQL = SQL
        self.tabel = tabel
        self.colum = colum
        self.Buffertime = Buffertime
        self.Process = None
        self.setup()

    def setup(self):
        self.SQL.tabels = [self.tabel]
        self.Process = multiprocessing.Process(target=self.exe)

    def delete_if_too_old_date(self):
        dates_list = self.SQL.basic_read(None, self.colum)
        dates_list = [dates.format(x[0]) for x in dates_list]
        dates_delete = []
        for x in dates_list:
            if 'months' == self.Buffertime[0]:
                if dates.add(x, months=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
            if 'days' == self.Buffertime[0]:
                if dates.add(x, days=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
            if 'years' == self.Buffertime[0]:
                if dates.add(x, years=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
            if 'minutes' == self.Buffertime[0]:
                if dates.add(x, minutes=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
            if 'seconds' == self.Buffertime[0]:
                if dates.add(x, seconds=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
            if 'hours' == self.Buffertime[0]:
                if dates.add(x, hours=self.Buffertime[1]) < dates.current():
                    dates_delete.append(x)
        print(dates_delete)
        for x in dates_delete:
            self.SQL.Execute_SQL_Command(f"DELETE FROM `{self.SQL.database}`.`{self.tabel}` WHERE (`{self.colum}` = '{x}')")
        self.SQL.db.commit()

    def exe(self):
        while True:
            try:
                self.delete_if_too_old_date()
            except Exception:
                print(Exception)

    def run(self):
        multiprocessing.freeze_support()
        self.Process.start()

    def stop(self):
        self.Process.terminate()