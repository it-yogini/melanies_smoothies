
# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import Pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    "Choose the fruits you want in your custom Smoothie!"

)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()

name_on_order= st.text_input('Name on Smoothie: ')

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'), col('Search_on'))
st.dataframe(data=my_dataframe, use_container_width=True)

#convert SN DF to PD DF
pd_df - my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:'
        ,my_dataframe
)
ingredients_string = ''
if ingredients_list:
   # st.write(ingredients_list)
   # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    #st.write(ingredients_string)


my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

#st.write(my_insert_stmt)

time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    
    st.success('Your Smoothie is ordered!', icon="✅")



