import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Mom's New Healty Dinner")

streamlit.header('Breakfast Menu')
streamlit.text ('🥣  Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗   Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔   Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toad')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected= streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# New section to display fruitvice api  response
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
    else:
      back_from_function= get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
      #ruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      #ruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      #reamlit.dataframe(fruityvice_normalized)
        

except URLError as e:
  streamlit.error()
      
#streamlit.write('The user entered ', fruit_choice)

#import requests

# streamlit.text(fruityvice_response)

# dont' run anytig past here while we troubleshoot 
streamlit.stop()
#import snowflake.connector
streamlit.header("The fruit load list contains:")
#snowflake realted functions
def get fruit_load_list():
    with  my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
# add bution to load the list
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = fruit_load_list()
    streamlit.datafame(my_data_rows)
    
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("SELECT * from fruit_load_list")

#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text("The fruit load list contains:")

#streamlit.text(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
