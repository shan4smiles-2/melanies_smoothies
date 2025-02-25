# Import python packages
import streamlit as st
import requests
# Write directly to the app
st.title("Customize your Smoothie")
st.write(
    """
    Choose Fruits you want in your custom smoothie
    """
)

# Using text input
name_on_order = st.text_input("Name on your Cup?")
st.write("We wll call out: ", name_on_order)

# Using a select box
option = st.selectbox(
    "What is your fav fruit?",
    ("banana", "strawberry", "peaches"),
)
st.write("You selected fruit:", option)

# using session
cnx = st.connection('snowflake')
session = cnx.session()

# Selecting table
my_dataframe = session.table("smoothies.public.fruit_options")
st.dataframe(data=my_dataframe, use_container_width=True)

# Selecting cols
st.subheader('Snowflake dataframe')
from snowflake.snowpark.functions import col
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('search_on'))
st.dataframe(data=my_dataframe, use_container_width=True)

# Convert to a pandas dataframe
st.subheader('Pandas dataframe')
pd_df = my_dataframe.to_pandas()
st.dataframe(data=pd_df)

# Stop
# st.stop()

# Using a multi select box
ingredients_list = st.multiselect(
    "What are your favorite fruits",
    my_dataframe,
    max_selections=5
    # an additional list to set  default for options
)
# Note: 
# """
# ingredients_list variable is an object or data type called a LIST.
# LIST by meaning can mean a list or a data type or object (shown below), not a dataframe or not a string
# """
# st.write("You selected:", ingredients_list)
# st.text(ingredients_list)

# Using to insert
if ingredients_list: # to show [] only when we select

    ingredients_string = ''
    
    for ingredient in ingredients_list:
        ingredients_string += ingredient + ' '

        # the search_on for the 
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == ingredient, 'SEARCH_ON'].iloc[0] # the iloc[0] if we have multiple rows for a given ingredient
        st.write('The search value for ', ingredient,' is ', search_on, '.')
        
        # The nutrient plan
        st.subheader(ingredient + ' Nutrient Info')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        st_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
    
    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
            values ('""" + name_on_order + """','""" + ingredients_string + """')"""
    # st.write(my_insert_stmt)

    time_to_insert = st.button("Submit")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


# Adding a RESTful API connection - SMOOTHIE nutrition information
# import requests
# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response) # simple: "Response <200>"
# st.text(smoothiefroot_response.json()) # modify the format: "json object"
# st_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
