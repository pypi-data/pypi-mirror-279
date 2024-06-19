from .. import data
from .. import dates

class process_data:

    def __init__(self, config:dict, **kwargs):
        self.data:dict = self.clean_data(kwargs)
        self.num_data:int = 0
        self.config(config)
        self.data, self.labels = self.process()

    def get(self):
        return self.labels, self.data

    def config(self, config:dict):
        keys = config.keys()
        if 'time' in keys:
            self.time = config['time']

    def clean_data(self, data:dict):
        for x in [x for x in data.keys()]:
            data[x] = sorted(data[x], key=lambda x: x[-1])
        return data

    def process_dates(self):
        min_data, max_data = self.seperate_dates()
        dates = [min_data]
        while dates[-1] < max_data:
            dates.append(self.time+dates[-1])
        return dates

    def process(self):
        _data = dict()
        dates = self.process_dates()
        print(dates)
        for x in self.data.keys():
            _data[x] = self._process(self.data[x], dates)
        for x in _data.keys():
            _data[x] = self.do_data(_data[x])
            print(_data[x])
        del dates[-1]
        return _data, self.cov_dates_to_str(dates)


    def do_data(self, data):
        values = list()
        for x in data:
            values.append(self._do_data(x))
        return values

    def _do_data(self, data):
        values = list()
        func = data[0][0][-1]
        for x in data:
            _values = list()
            for xx in x:
                _values.append(xx[0])
            values.append(func(_values))
        return func(values)

    def _process(self, data:list, dates_list):
        _data = [x for x in data]
        finished_data = []
        for num in range(len(dates_list)):
            if num != (len(dates_list) - 1):
                date = dates_list[num + 1]
                _finished_data = []
                for x in _data:
                    if x[-1] < date:
                        _finished_data.append(x[0:-1])
                if len(_finished_data) != 0:
                    for x in range(len(_finished_data)):
                        del _data[0]
                finished_data.append(_finished_data)
        return finished_data

    def seperate_dates(self):
        data = self.data
        values = sorted([item[-1] for sublist in data.values() for item in sublist])
        return values[0], values[-1]

    def cov_dates_to_str(self, date_list:list):
        for x in range(len(date_list)):
            date_list[x] = dates.datetime_to_String(date_list[x])
        return date_list

