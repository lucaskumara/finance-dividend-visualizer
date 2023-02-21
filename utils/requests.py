import requests

from bs4 import BeautifulSoup
from datetime import datetime
from utils.enums import Exchange

def request_dividends(exchange, ticker):
    match exchange:
        case Exchange.NYSE | Exchange.NASDAQ:
            return extract_dividends(f'https://dividendhistory.org/payout/{ticker}')
        case Exchange.TSX:
            return extract_dividends(f'https://dividendhistory.org/payout/tsx/{ticker}')
        case Exchange.LSE:
            return extract_dividends(f'https://dividendhistory.org/payout/uk/{ticker}')
        case Exchange.ASX:
            return extract_dividends(f'https://dividendhistory.org/payout/asx/{ticker}')

def extract_dividends(url):
    dividends = []
    page = BeautifulSoup(requests.get(url).content, 'html.parser')

    table = page.find(id='dividend_table')
    table_body = table.find('tbody')
    table_rows = table_body.find_all('tr')

    for row in table_rows:
        columns = row.find_all('td')

        if columns[3].text == 'unconfirmed/estimated':
            continue

        dividend_date_string = columns[1].text
        dividend_amount_string = columns[2].text

        dividend_date = parse_date(dividend_date_string)
        dividend_amount = parse_amount(dividend_amount_string)

        dividends.append((dividend_date, dividend_amount))

    return dividends

def parse_date(dividend_date_string):
    return datetime.strptime(dividend_date_string, '%Y-%m-%d')

def parse_amount(dividend_amount_string):
    return float(dividend_amount_string.replace('$', '').replace('*', ''))