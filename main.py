
from collect_numbers_drawn import new_row, list_conversion
from variables import lottery_facts, number_keys, lottery_with_bonus, lottery_order_matters, lottery_names


import pandas as pd
from datetime import datetime
import datetime as dt
import pytz

import streamlit as st

st.set_page_config(
    page_title="Lottery Result Check",
    page_icon='🎲',
    layout="centered"
)

## Set sessions states
for e, n in enumerate(number_keys):
    if f'number_{e+1}' not in st.session_state:
        st.session_state[f'number_{e+1}'] = 0

if "lottery_option" not in st.session_state:
    st.session_state["lottery_option"] = "Lotto 6/49"


df_pickle = pd.read_pickle(filepath_or_buffer="data/lotto_results.pkl")

lotteries = lottery_names

color_main = lottery_facts[st.session_state.lottery_option]["colors"][1]
color_white = lottery_facts[st.session_state.lottery_option]["colors"][0]
color_grey = lottery_facts[st.session_state.lottery_option]["colors"][-1]

st.markdown(
    f"<H5 style='color:#F2F2F2; font-size:35px;'> LOTTERY RESULT CHECK - <mark style = 'font-family:liberation serif; font-size:44px; color:{color_main}; background-color:transparent;'>{st.session_state.lottery_option}</mark></H5>",
    unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

with st.sidebar:
    st.write(
        f"<H5 style='color:{color_main}; font-size:16px;'> {dt.datetime.now(tz=pytz.timezone('EST')).strftime('%A %B %#d, %Y %I:%M%p %Z')} </h5>",
        unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.image(f"images/{lottery_facts[st.session_state.lottery_option]['image_file']}", width=154)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<hr style = 'height:1px; border-width:0; color:{color_main}; background-color:{color_main}'> ",
                    unsafe_allow_html=True)
    st.selectbox(label='Select Lottery',
                 options=lotteries,
                 index = 0,
                 key = 'lottery_option'
    )

    numbers_selected = lottery_facts[st.session_state.lottery_option]["numbers_drawn"]
    numbers_range = lottery_facts[st.session_state.lottery_option]["value_range"]
    numbers_range = range(numbers_range[0], numbers_range[1] + 1)

    if st.session_state.lottery_option == 'Keno':
        st.selectbox(label="How many numbers?", options=range(2, 10), key="keno_slider",
                     index=0)

        with st.form(key="submit_selection"):

            with st.expander(label="Expand to view number selection", expanded=False):
                for num in range(st.session_state.keno_slider):
                    st.select_slider(label="", options=numbers_range, key=f"number_{num+1}")

            submitted = st.form_submit_button(label="Submit")

    else:
        with st.form(key="submit_selection"):


            with st.expander(label="Expand to view number selection", expanded=False):
                for num in range(numbers_selected):
                    st.select_slider(label="", options=numbers_range, key=f"number_{num+1}")

            submitted = st.form_submit_button(label="Submit")


## Main Page
df_filtered = df_pickle[df_pickle["Lottery Name"] == st.session_state.lottery_option]
st.markdown(f"<p style = 'font-size:20px;color:{color_main};   '>LAST DRAWN NUMBERS </p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
last_numbers = df_filtered.tail(1)["Numbers Drawn"].values.tolist()[0]
last_draw_date = df_filtered.tail(1)["Draw Date"].values.tolist()[0]
last_draw_time = df_filtered.tail(1)["Draw Time"].values.tolist()[0]

try:
    last_draw_date = datetime.strptime(last_draw_date, "%d %b %Y")
except:
    last_draw_date = datetime.strptime(last_draw_date, "%d-%b-%y")
try:
    last_numbers2 = list_conversion(last_numbers)
except:
    last_numbers2 = last_numbers

numbers_selected_keys = number_keys[0:numbers_selected]


cols = []
for c in range(numbers_selected):
    col_name = f"col_{c}"
    cols.append(col_name)
cols = st.columns(len(cols))
for e,c in enumerate(cols):
    with c:
        st.write(
            f"<p style = 'border-radius: 50%; width:52px; height:52px; padding:10px; background:#fff; box-shadow: 3px 3px 5px {color_main}; border:3px solid {color_main}; color:{color_main}; text-align:center; font:bold 20px Arial, sans-serif;'> {last_numbers2[e]} </p>",
            unsafe_allow_html=True)
if st.session_state.lottery_option in lottery_with_bonus:
    bonus_number = int(df_filtered.tail(1)["Bonus Number"].values.tolist()[0])
    st.markdown(f"<p style = 'font-size:20px;color:{color_white};   '>BONUS NUMBER </p>", unsafe_allow_html=True)
    st.write(
        f"<p style = 'border-radius: 50%; width:52px; height:52px; padding:10px; background:{color_main}; border:3px solid #fff; color:#fff; text-align:center; font:bold 20px Arial, sans-serif;'> {bonus_number} </p>",
        unsafe_allow_html=True)
else:
    bonus_number = 0

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<p style = 'font-size:14px;color:{color_white};'>LAST DRAW DATE | {last_draw_date.strftime('%A %B %#d, %Y')} | {last_draw_time} </p>", unsafe_allow_html=True)

## Writing your picked numbers on main page
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<p style = 'font-size:20px;color:{color_white};   '>MY PICKS </p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
cols_picks = []
for my_pick in range(numbers_selected):
    col_name2 = f"col_pick_{my_pick}"
    cols_picks.append(col_name2)
cols_picks = st.columns(len(cols_picks))

for number_pick, col_pick in enumerate(cols_picks):
    with col_pick:
        picked_number = st.session_state[numbers_selected_keys[number_pick]]
        drawn_number = last_numbers2[number_pick]
        if st.session_state.lottery_option in lottery_order_matters:
            st.write(
                f"<p style = 'border-radius: 50%; width:52px; height:52px; padding:10px; background:#fff; border:3px solid {color_main if picked_number == drawn_number else (color_main if picked_number == bonus_number else color_grey)}; color:{color_main if picked_number == drawn_number else (color_grey if picked_number == bonus_number else color_grey)}; text-align:center; font:bold 20px Arial, sans-serif;'> {picked_number} </p>",
                unsafe_allow_html=True)
        else:
            st.write(
                f"<p style = 'border-radius: 50%; width:52px; height:52px; padding:10px; background:#fff; border:3px solid {color_main if picked_number in last_numbers2 else(color_main if picked_number == bonus_number else color_grey)}; color:{color_main if picked_number in last_numbers2 else color_grey}; text-align:center; font:bold 20px Arial, sans-serif;'> {picked_number} </p>",
                unsafe_allow_html=True)

if st.session_state.lottery_option in lottery_order_matters:
    st.write(f"<p style='font-size:13px;color:{color_white};font-style:italic;'>The order of your number picks factors into prize winnings </p>", unsafe_allow_html=True)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Program Running...")
    #new_row()


