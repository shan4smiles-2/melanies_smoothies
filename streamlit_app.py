# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Customize your Smoothie")
st.write(
    """
    Choose Fruits you want in your custom smoothie
    """
)

# Using text input
name_on_order = st.text_input("Name on your Cup?").strip()
st.write("We wll call out: ", name_on_order)

# Using a select box
option = st.selectbox(
    "What is your fav fruit?",
    ("banana", "strawberry", "peaches"),
)
st.write("You selected fruit:", option)

# using session
session = get_active_session()

# Selecting table
my_dataframe = session.table("smoothies.public.fruit_options")
st.dataframe(data=my_dataframe, use_container_width=True)

# Selecting cols
from snowflake.snowpark.functions import col
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)

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
    
    ingredients_string = ' '.join(ingredients_list).strip()
    # st.write(ingredients_string)
    
    my_insert_stmt = ("""
        insert into SMOOTHIES.PUBLIC.ORDERS (name_on_order, ingredients)
        values('"""
        + (name_on_order.lstrip()) + "', '" + (ingredients_string) +
        """
        ')
    """)
    # st.write(my_insert_stmt)

    time_to_insert = st.button("Submit")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    



