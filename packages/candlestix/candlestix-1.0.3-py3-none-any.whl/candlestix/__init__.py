import os
import sys
import tempfile
import csv
import logging
import os
import re
import tempfile
from datetime import datetime, timedelta
from gzip import GzipFile
from logging import Logger
from pathlib import Path
from urllib.request import urlopen

import candlestix
from candlestix.candleconf import Exchange
from candlestix.instrument import Instrument

candlestix_conf = {}
initialised = False
nse_lookup = {}
bse_lookup = {}
logger = logging.getLogger('candlestix')

def init_download_dir():
    history_download_dir = os.path.join(tempfile.gettempdir(), 'candlestix_cache')
    if not os.path.isdir(history_download_dir):
        try:
            os.makedirs(history_download_dir, exist_ok=True)
        except OSError as e:
            history_download_dir = tempfile.gettempdir()
    candlestix_conf['cache_dir'] = history_download_dir
    # for backward compatibility
    candlestix_conf['historical_data'] = {}
    candlestix_conf['historical_data']['download_dir'] = history_download_dir
    return history_download_dir

def download_and_unzip_gzip_file():
    file_url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
    output_file_path = os.path.join(candlestix_conf['cache_dir'], 'complete_instruments.csv.gz')
    # Download the Gzip file
    with urlopen(file_url) as response:
        with open(output_file_path, 'wb') as output_file:
            output_file.write(response.read())

    downloaded_file = Path(output_file_path)
    instruments_file = Path(output_file_path.replace(".gz", ""))

    # Unzip the downloaded file
    with GzipFile(downloaded_file, 'rb') as gz_file:
        with open(instruments_file, 'wb') as output_file:
            output_file.write(gz_file.read())

    # Delete the downloaded Gzip file
    if downloaded_file.exists():
        downloaded_file.unlink()

    logger.info(f"File downloaded and unzipped successfully: {output_file_path}")

    return instruments_file

def load_instruments_from_csv(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header

        logger.info("Starting load into instruments table ...")
        batch = []
        dup_check = set()
        pattern_decimal_number = r"\d{1,2}\.\d{1,2}"
        for row in csv_reader:

            instrument_key = row[0]
            symbol = row[2]
            name = row[3]
            instrument_type = row[9]
            exchange_str = row[11]

            if ('%' in name or  # name contains '%'
                    bool(re.search(pattern_decimal_number, name)) or  # name contains a decimal number - 7.50
                    instrument_key in dup_check or  # duplicate check for instrument id
                    (instrument_type.lower() != 'equity' and instrument_type.lower() != 'index')):  # type is not equity
                continue

            dup_check.add(instrument_key)

            exchange = Instrument.get_exchange_from_val(exchange_str)
            if instrument_type.lower() == 'index':
                symbol = name.upper().replace(' ', '_')  # Convert 'NIFTY 50' to 'NIFTY_50'
            inst = Instrument(symbol=symbol, instrument_key=instrument_key, name=name, exchange=exchange)
            if exchange == Exchange.NSE or exchange == Exchange.NSE_INDEX:
                nse_lookup[symbol] = inst
            elif exchange == Exchange.BSE or exchange == Exchange.BSE_INDEX:
                bse_lookup[symbol] = inst

    # print(f'nse>> size={round(sys.getsizeof(nse_lookup)/1024,2)} kb, len={len(nse_lookup.keys())}')
    # print(f'bse>> size={round(sys.getsizeof(bse_lookup)/1024,2)} kb, len={len(bse_lookup.keys())}')
    logger.info("Data load COMPLETE for instruments.")


def init():
    if initialised:
        return
    # 1. Create the download / cache dir
    init_download_dir()
    # 2. download and process the instruments file
    f = download_and_unzip_gzip_file()
    load_instruments_from_csv(f)
    candlestix.initialised = True


init()
