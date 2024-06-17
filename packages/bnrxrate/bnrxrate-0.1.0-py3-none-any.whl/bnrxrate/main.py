import datetime
import pytz
from urllib import request
import xml.etree.ElementTree as ET

from .holidays import romania_holidays
from .exceptions import DateRangeError, SymbolError, DateError


non_banking_days = []
for year in romania_holidays.keys():
    for month in romania_holidays[year].keys():
        for day in romania_holidays[year][month]:
            non_banking_days.append(datetime.date(year, month, day))


class Xrates():

    def __init__(self):
        self.year_base_url = 'https://bnr.ro/files/xml/years/nbrfxrates-year-.xml'
        self.today_url = 'https://www.bnr.ro/nbrfxrates.xml'
        self.cached = {}
 
    
    # non-public methods


    def _request_xml(self, url: str) -> str:
        """
        Fetch the xml data at url.
        """
        with request.urlopen(url) as response:
            xml_content = response.read().decode('utf-8')
        return xml_content


    def _get_today(self) -> str:
        """
        Request the data for today.
            Return:
                xml_content (str): content of the accessed online resource
        """
        today_xml = self._request_xml(self.today_url)
        today_dict = self._xml_to_dict(today_xml)
        self.cached.update(today_dict)
        return today_dict


    def _get_year(
            self,
            year: int = datetime.date.today().year) -> str:
        """
        Request the data for a whole year (current year if year parameter
        not provided) and save it as a local XML file.
            Params:
                year (datetime.date.year): the year for which to request 
                    data (default: current year)
            Return:
                xml_content (str): content of the accessed online resource
        """
        year_url = self.year_base_url.replace('-year-', str(year))
        year_xml = self._request_xml(year_url)
        year_dict = self._xml_to_dict(year_xml)
        self.cached.update(year_dict)
        return year_dict


    def _xml_to_dict(self, xml_data: str) -> dict:
        """
        Parse the xml retrieved from the website and convert it to dict.
            Params:
                xml_data (str): the xml data as string
            Return:
                dict_year (dict): the xml data converted to dict
        """
        root = ET.fromstring(xml_data)
        namespaces = {'ns': 'http://www.bnr.ro/xsd'}
        body = root.find('ns:Body', namespaces)
        cubes = body.findall('ns:Cube', namespaces)
        dict_year = {}
        for cube in cubes:
            date = cube.attrib['date']
            dict_year[date] = {}
            rates = cube.findall('ns:Rate', namespaces)
            for rate in rates:
                currency = rate.attrib['currency']
                multiplier = float(rate.attrib.get('multiplier', '1'))
                try:
                    value = float(rate.text)
                    value = value / multiplier
                except:
                    value = None
                dict_year[date][currency] = value
        return dict_year
    

    def _get_previous_banking_day(
            self,
            date: datetime.date = datetime.date.today()) -> datetime.date:
        """
        Get the previous date that was a banking day.
            Params:
                date (datetime.date): object representing the initial date
            Return:
                date (datetime.date): object representing previous banking day
        """
        if str(date) < "2008-01-03":
            raise(DateError("No data before 2008-01-03.", date))
        previous_day = date - datetime.timedelta(1)
        if self.is_banking_day(previous_day):
            return previous_day
        else:
            return self._get_previous_banking_day(previous_day)
        
    
    def _today_not_updated(self):
        today = datetime.date.today()
        if self.is_banking_day(today):
            if str(today) not in self.cached:
                return True
        return False


    def _get_date_xrate(self, date: datetime.date) -> dict:
        """
        Get the xrates for a specific date OR for the previous banking
        day if the date is not a banking day or the time is before the
        update time.
        """
        if str(date) < "2008-01-03":
            raise(DateError("No data before 2008-01-03.", date))
        if not self.is_banking_day(date):
            date = self._get_previous_banking_day(date)
        else:
            if date == datetime.date.today():
                if self._today_not_updated():
                    if self.after_update_time():
                        self._get_today()
                    else:
                        date = self._get_previous_banking_day(date)
        if str(date) not in self.cached.keys():
            self._get_year(date.year)
        return self.cached[str(date)]


    def _get_period_xrate(
            self,
            start_date: datetime.date,
            end_date: datetime.date
            ) -> dict:
        """
        Get the xrates for a specific period.
        """
        if str(start_date) < "2008-01-03":
            raise(DateError("No data before 2008-01-03.", start_date))
        if str(start_date) > str(datetime.date.today()):
            raise(DateError("Start date is in the future.", start_date))
        if str(end_date) > str(datetime.date.today()):
            raise(DateError("End date is in the future.", end_date))
        if end_date < start_date:
            raise DateRangeError('End date should be after start date.', start_date, end_date)
        if end_date == datetime.date.today() and self._today_not_updated():
            if self.after_update_time():
                self._get_today(end_date.year)
            else:
                end_date = self._get_previous_banking_day()
        data = {}
        date_iterator = start_date
        while str(date_iterator) <= str(end_date):
            if self.is_banking_day(date_iterator):
                if not str(date_iterator) in self.cached.keys():
                    self._get_year(date_iterator.year)    
                data[str(date_iterator)] = self.cached[str(date_iterator)]
            date_iterator += datetime.timedelta(1)
        return data


    def _filter_date_symbols(self, symbols: list, data: dict, date: datetime.date):
        """
        Filter the dictionary to keep only the symbols in the list for 
        a date.
        """
        if not symbols:
            return data
        filtered = {}
        for symbol in symbols:
                if symbol not in data.keys():
                    raise SymbolError('Invalid symbol', symbol, date)
        for symbol, value in data.items():
            if symbol in symbols:
                filtered[symbol] = value
        return filtered


    def _filter_period_symbols(self, symbols: list, data: dict):
        """
        Filter the dictionary to keep only the symbols in the list for 
        a period.
        """
        if not symbols:
            return data
        filtered = {}
        for date, values in data.items():
            for symbol in symbols:
                if symbol not in values.keys():
                    raise SymbolError('Invalid symbol', symbol, date)
            filtered[date] = {}
            for symbol, value in values.items():
                if symbol in symbols:
                    filtered[date][symbol] = value
        return filtered


    # public methods


    def is_banking_day(
            self,
            date: datetime.date = datetime.date.today()
            ) -> bool:
        """
        Check if a given date is a banking day or not.
            Params:
                date (datetime.date): object representing the date
            Return:
                bool
        """
        return not (date.weekday() in [5, 6] or \
            date in non_banking_days)
    

    def after_update_time(self):
        """
        Check if the current time is before the time at which the
        data is updated on the website.
            Return:
                bool
        """
        bucharest_tz = pytz.timezone('Europe/Bucharest')
        bucharest_time = datetime.datetime.now(bucharest_tz).time()
        return datetime.time(13, 2) < bucharest_time
    

    def get_xrate(self,
                  symbols_filter: list = None,
                  start_date: datetime.date = datetime.date.today(),
                  end_date: datetime.date = None) -> dict:
        """
        Get the xrate for a list of symbols for a given date or period.
            Params:
                symbols_filter (list): list of symbols (can be lowercase too)
                        should be an emptylist  or None to get all symbols
                start_date (datetime.date): the (starting) date
                end_date (datetime.date): the (optional) end date. If end_date
                        is not provided, data for start_date is returned
            Return:
                dict
        """
        if symbols_filter:
            symbols_filter = [symbol.upper() for symbol in symbols_filter]
        if end_date:
            if end_date < start_date:
                raise DateRangeError('End date sould be after start date.', start_date, end_date)
            all_xrates = self._get_period_xrate(start_date, end_date)
            xrates = self._filter_period_symbols(symbols_filter, all_xrates)
        else:
            all_xrates = self._get_date_xrate(start_date)
            xrates = self._filter_date_symbols(symbols_filter, all_xrates, start_date)
        return xrates
    

    def get_today_update(
            self,
            symbols_filter: list = None) -> dict:
        """
        Get the xrates for a list of symbols but only if it was updated
        today. Else return None.
            Params:
                symbols_filter (list): list of symbols
            Return:
                dict
        """
        # if symbols_filter is None (or empty), get the rates for all symbols
        today = datetime.date.today()
        if not self.after_update_time() or not self.is_banking_day(today):
            return None
        all_xrates = self._get_date_xrate(today)
        xrates = self._filter_date_symbols(symbols_filter, all_xrates, today)
        return xrates


    def list_symbols(
            self,
            date: datetime.date = datetime.date.today()) -> list:
        """
        Get the available symbols for specific date.
            Params:
                date (datetime.date): the date
            Return:
                list: the list of symbols
        """
        date_data = self._get_date_xrate(date)
        return list(date_data.keys())

    
if __name__ == "__main__":
    bnr = Xrates()

    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 6, 15)
    data = bnr.get_xrate(['EUR'], start_date, end_date)
    print(data)

    print(f'\ntoday update: {bnr.get_today_update()}')
