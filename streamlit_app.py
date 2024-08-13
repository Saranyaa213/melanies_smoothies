pip install snowflake-snowpark-python
# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie.
    """
)

# Initialize Snowflake session
session = get_active_session()

# Retrieve fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name')).to_pandas()
fruit_names = my_dataframe['fruit_name'].tolist()

# Create a multiselect widget for choosing ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names
)

# Enforce maximum selection of 5
if len(ingredients_list) > 5:
    st.warning('You can select up to 5 ingredients only.')
    ingredients_list = ingredients_list[:5]

if ingredients_list:
    # Create a string of selected ingredients
    ingredients_string = ' '.join(ingredients_list)
    st.write("Selected ingredients:", ingredients_string)

    # Prepare SQL insert statement
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, order_filled)
    VALUES ('{ingredients_string}', FALSE);
    """

    # Create a button for submitting the order
    if st.button('Submit Order'):
        # Execute the SQL statement
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

