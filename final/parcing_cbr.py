import requests
import json
from datetime import datetime, timedelta
import os
from decimal import Decimal
from bs4 import BeautifulSoup

import xml.etree.ElementTree as ET

class ParserCBRF:
    def __init__(self):
        self.base_url = "http://www.cbr.ru/scripts/XML_daily.asp"
        self.data = {}
        self.parsed_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parsed_data')
        self.json_file = os.path.join(self.parsed_data_dir, 'currency_rates.json')

    def _create_data_directory(self):
        if not os.path.exists(self.parsed_data_dir):
            os.makedirs(self.parsed_data_dir)

    def _fetch_data(self, date):
        params = {'date_req': date.strftime('%d/%m/%Y')}
        response = requests.get(self.base_url, params=params)
        return response.content

    def _parse_xml(self, xml_content):
        root = ET.fromstring(xml_content)
        rates = {}
        for valute in root.findall('Valute'):
            code = valute.find('CharCode').text
            value = valute.find('Value').text.replace(',', '.')
            rates[code] = value
        return rates

    def start(self, days=30):
        self._create_data_directory()
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        current_date = start_date

        while current_date <= end_date:
            try:
                xml_content = self._fetch_data(current_date)
                daily_rates = self._parse_xml(xml_content)
                self.data[current_date.strftime('%Y-%m-%d')] = daily_rates
            except Exception as e:
                print(f"Error fetching data for {current_date}: {e}")
            
            current_date += timedelta(days=1)

        self._serialize_data()

    def _serialize_data(self):
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

class CurrencyRatesCBRF:
    def __init__(self):
        self.parser = ParserCBRF()
        self.json_file = self.parser.json_file
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def rate_by_date(self, date, currency_code):
        """Returns exchange rate for specific currency on a given date"""
        if isinstance(date, datetime):
            date = date.strftime('%Y-%m-%d')
        
        if date in self.data and currency_code in self.data[date]:
            return self.data[date][currency_code]
        return None

    def rate_last(self, currency_code):
        """Returns the latest available exchange rate for specific currency"""
        last_date = max(self.data.keys())
        return self.data[last_date].get(currency_code)

    def rate_range_dates(self, from_date, to_date, currency_code):
        """Returns sorted list of (date, rate) pairs for specific currency in date range"""
        if isinstance(from_date, datetime):
            from_date = from_date.strftime('%Y-%m-%d')
        if isinstance(to_date, datetime):
            to_date = to_date.strftime('%Y-%m-%d')

        result = [
            (date, rates[currency_code])
            for date, rates in self.data.items()
            if from_date <= date <= to_date and currency_code in rates
        ]
        return sorted(result)

def main():
    # Initialize and run parser
    parser = ParserCBRF()
    parser.start()

    # Example usage of CurrencyRatesCBRF
    currency_rates = CurrencyRatesCBRF()
    
    # Get USD rate for specific date
    print("USD rate for 2023-11-01:", currency_rates.rate_by_date("2023-11-01", "USD"))
    
    # Get latest USD rate
    print("Latest USD rate:", currency_rates.rate_last("USD"))
    
    # Get USD rates for date range
    rates = currency_rates.rate_range_dates("2023-11-01", "2023-11-05", "USD")
    print("USD rates for range:", rates)

if __name__ == "__main__":
    main()