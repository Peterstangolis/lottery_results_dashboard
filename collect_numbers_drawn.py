import numpy as np

from variables import lottery_guru_url, lottery_names, lottery_with_bonus


## Import the required packages
import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import datetime as dt
from datetime import time
import pytz
import lxml
import pickle


def list_conversion(l):
    if isinstance(l, int):
        return l
    else:
        new_list = []
        l2 = l.split(',')
        for item in l2:
            i = item.replace('[','').replace(']','').strip()
            if not i:
                i = i
            else:
                try:
                    i = int(i)
                except:
                    i = float(i)
            new_list.append(i)
        return new_list

## Get the lottery cards from the website
def scrape_lottery_cards(url):
    lottery_guru = requests.get(url)

    if lottery_guru.status_code == 200:
        print(f"SCRAPE SUCCESSFUL {lottery_guru.status_code}")

        soup_guru = BS(lottery_guru.text, "lxml")

        ## Retrieve all the cards from the site
        lottery_cards = soup_guru.find_all('div', class_ = 'lg-card lg-link')

    else:
        print(lottery_guru.status_code)

    return lottery_cards

def lottery_variables():

    lottery_cards = scrape_lottery_cards(lottery_guru_url)

    results = dict()
    for n in range(len(lottery_cards)):

        lottery_card = lottery_cards[n]

        lotto_name = lottery_card.find("div", class_="column is-10 lg-name")
        lotto_name = lotto_name.text
        numbers = lottery_card.find_all("ul", class_ = "lg-numbers")
        if lotto_name == 'Mega Dice':
            break


        for name in lottery_names:
            if name == lotto_name:
                lottery_numbers = list()
                for num in numbers[0].find_all("li"):
                    lottery_numbers.append(int(num.text))
                    draw_dates = lottery_card.find_all("div", class_="lg-time")
                    last_result_date = draw_dates[0].text.strip()
                    last_result_date = last_result_date.split("\n")
                    next_result_date = draw_dates[1].text.strip()
                    next_result_date = next_result_date.split("\n")
                results[lotto_name] = [lottery_numbers, last_result_date, next_result_date]

    return results

def load_df(filename):
    import pandas as pd
    df = pd.read_csv(filename)
    return df

def new_row():
    lot_results = lottery_variables()
    df = load_df(filename='data/lotto_results.csv')
    df_pickle = pd.read_pickle(filepath_or_buffer='data/lotto_results.pkl')
    for key, value in lot_results.items():

        if len(value[-1]) == 2:
            last_draw_time = time(hour=22, minute=30, second=00)
            last_draw_date = value[-2][-1]
            next_draw_time = time(hour=22, minute=30, second=00)
            next_draw_date = value[-1][-1]
        elif len(value[-1]) == 3:
            last_draw_time = value[-2][-1]
            last_draw_date = value[-2][-2]
            next_draw_time = value[-1][-1]
            next_draw_date = value[-1][-2]

        if key not in lottery_with_bonus:
            bonus_number = None
        else:
            bonus_number = value[0][-1]

        add_new_row = {
            df_pickle.columns[0] : key,
            df_pickle.columns[1] : last_draw_date,
            df_pickle.columns[2] : last_draw_time,
            df_pickle.columns[3] : next_draw_date,
            df_pickle.columns[4] : next_draw_time,
            df_pickle.columns[5] : value[0],
            df_pickle.columns[6] : bonus_number
        }

        df_length = len(df_pickle)
        if df_length < 8:
            print("Correct")
            new_row_series = pd.Series(add_new_row)
            df_pickle = pd.concat([df_pickle, new_row_series.to_frame().T], ignore_index=True)

        else:
            df_tail = df_pickle.tail(8)
            last_nums = df_pickle["Lottery Name"] == key
            last_nums = df_pickle[last_nums]
            last_nums = last_nums["Numbers Drawn"]
            last_nums_int = last_nums.values.tolist()[-1]
            try:
                last_nums_int = list_conversion(last_nums.values.tolist()[-1])
            except:
                last_nums_int

            if last_nums_int == value[0]:
                print("Numbers Match")
                continue
            else:
                print("Adding new row")
                new_row_series = pd.Series(add_new_row)
                df_pickle = pd.concat([df_pickle, new_row_series.to_frame().T], ignore_index=True)



    df_pickle.to_csv("data\lotto_results.csv",
               lineterminator='\n',
               index=False)

    df_pickle.to_pickle("data\lotto_results.pkl")







