import os
import datetime
from typing import Dict
import requests
from bs4 import BeautifulSoup
import pandas as pd


class ParserCBRF:
    """
    Класс для парсинга данных о ключевой ставке ЦБ РФ.
    Поддерживает сбор с URL или парсинг файлов (.xlsx, .xls, .csv).
    Возвращает dict[date, rate].
    """

    def __init__(self):
        pass

    def start(self, source: str) -> Dict[datetime.date, float]:
        """
        Публичный метод для запуска парсинга.
        
        :param source: URL страницы или путь к файлу.
        :return: dict с датами (date) как ключами и ставками (float) как значениями.
        """
        if source.startswith('http'):
            return self._scrape_url(source)
        else:
            return self._parse_file(source)

    def _scrape_url(self, url: str) -> Dict[datetime.date, float]:
        """
        Приватный метод для парсинга HTML-таблицы с URL.
        """
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if not table:
            raise ValueError("Таблица не найдена на странице.")
        
        data = {}
        rows = table.find_all('tr')[1:]  # Пропускаем заголовок
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 2:
                continue
            date_str = cols[0].text.strip()
            rate_str = cols[1].text.strip().replace(',', '.')
            try:
                date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
                rate = float(rate_str)
                data[date] = rate
            except ValueError as e:
                print(f"Ошибка парсинга строки {date_str}: {e}")
                continue
        return data

    def _parse_file(self, file_path: str) -> Dict[datetime.date, float]:
        """
        Приватный метод для парсинга файла по расширению.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.xlsx', '.xls']:
            return self._parse_excel(file_path)
        elif ext == '.csv':
            return self._parse_csv(file_path)
        elif ext == '.pdf':
            raise NotImplementedError("Парсинг PDF не поддерживается (требует tabula-py или pdfplumber).")
        else:
            raise ValueError(f"Неизвестное расширение файла: {ext}")

    def _parse_excel(self, file_path: str) -> Dict[datetime.date, float]:
        """
        Приватный метод для парсинга Excel-файлов.
        Предполагаем колонки 'Дата' и 'Ставка'.
        """
        df = pd.read_excel(file_path)
        if 'Дата' not in df.columns or 'Ставка' not in df.columns:
            raise ValueError("В файле отсутствуют колонки 'Дата' или 'Ставка'.")
        
        data = {}
        for _, row in df.iterrows():
            try:
                date = pd.to_datetime(row['Дата'], format='%d.%m.%Y').date()
                rate_str = str(row['Ставка']).replace(',', '.')
                rate = float(rate_str)
                data[date] = rate
            except ValueError as e:
                print(f"Ошибка парсинга строки {row['Дата']}: {e}")
                continue
        return data

    def _parse_csv(self, file_path: str) -> Dict[datetime.date, float]:
        """
        Приватный метод для парсинга CSV-файлов.
        Предполагаем колонки 'Дата' и 'Ставка', разделитель ';'.
        """
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')  # ЦБ часто использует ';'
        if 'Дата' not in df.columns or 'Ставка' not in df.columns:
            raise ValueError("В файле отсутствуют колонки 'Дата' или 'Ставка'.")
        
        data = {}
        for _, row in df.iterrows():
            try:
                date = pd.to_datetime(row['Дата'], format='%d.%m.%Y').date()
                rate_str = str(row['Ставка']).replace(',', '.')
                rate = float(rate_str)
                data[date] = rate
            except ValueError as e:
                print(f"Ошибка парсинга строки {row['Дата']}: {e}")
                continue
        return data

if __name__ == "__main__":
    parser = ParserCBRF()
    
    # Пример для URL (собирает данные с сайта ЦБ РФ)
    try:
        data_url = parser.start('https://www.cbr.ru/hd_base/KeyRate/')
        print("Данные с URL:")
        for date, rate in sorted(data_url.items()):
            print(f"{date}: {rate}%")
    except Exception as e:
        print(f"Ошибка при парсинге URL: {e}")

