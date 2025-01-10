# Import python packages
import streamlit as st
import requests
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie!! :cup_with_straw:")
st.write(
    """Choose the Fruit to customize the Smothie!
    """)

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# ##conver snowpark dataframe to pandas dataframe below
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# stop()

name_on_order = st.text_input("Name on Smoothie:",)
st.write("The name on Smoothie will be:", name_on_order)

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

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')

    # st.write(my_insert_stmt)
    if time_to_insert:
    # if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

my_dataframe2 = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
editable_df = st.data_editor(my_dataframe2)
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

submitted = st.button('Submit')
if submitted:
    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)
    try:
        og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
        st.success('Someone clicked the button', icon = '👍')   
    except:
        st.write('Something went wrong')
        
else:
    st.success('There is no pending order right now', icon = '👍')  
    


