# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smothie!! :cup_with_straw:")
st.write(
    """Choose the Fruit to customize the Smothie!
    """)

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose your 5 ingredients:"
    , my_dataframe
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '
    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

    time_to_insert = st.button('Submit Order')

    # st.write(my_insert_stmt)
    if time_to_insert:
    # if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width=true)
