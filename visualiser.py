import matplotlib.pyplot as plt
import numpy as np

from utils.enums import Exchange
from utils.requests import request_dividends

if __name__ == '__main__':
    data = request_dividends(Exchange.TSX, 'CDZ')

    dates = [payment[0] for payment in data]
    amounts = [payment[1] for payment in data]

    print(f'${(amounts[0] - amounts[-1]) / len(amounts)}')

    plt.plot_date(dates, amounts, xdate=True, linestyle='solid', marker='None')
    plt.show()