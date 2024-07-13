# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")

name_on_order = st.text_input('Name on Smoothie:')

st.write("The Name on your Smoothie will be -", name_on_order)

st.write(""" Choose your Fruits to add in your smoothie""")


#Commented out the Selection box
#option = st.selectbox(
#    "Which fruit you like to add in your Smoothie",
#    ("Strawberries", "Banana", "Mango" ,"Pomogranade"))
#
#st.write("You choose:", option)
#session = get_active_session()

cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredints_list = st.multiselect("Choose upto 5 ingredints of your choice",my_dataframe,max_selections=5)

if ingredints_list:
    #st.write("You selected:", ingredints_list)
    #st.text(ingredints_list)

    ingredients_string = ''
    for fruit_chosen in ingredints_list:
        ingredients_string += fruit_chosen + ' '
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success("Your Smoothie is ordered! "+name_on_order,icon="✅")


    
