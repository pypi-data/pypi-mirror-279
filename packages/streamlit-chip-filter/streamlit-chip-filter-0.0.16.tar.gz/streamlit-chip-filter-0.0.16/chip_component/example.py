import streamlit as st
# from __init__ import chip_filter
from chip_component import chip_filter

st.set_page_config(layout="wide")

# data = [
#     { "index": 0, "label": "Marksman", "clicked": True },
#     { "index": 1, "label": "Tank", "clicked": False },
#     { "index": 2, "label": "Mage", "clicked": False },
#     { "index": 3, "label": "Fghter", "clicked": False },
#     { "index": 4, "label": "Support", "clicked": False },
#     { "index": 5, "label": "Assassin", "clicked": False },
#     { "index": 6, "label": "Assassin", "clicked": False },
#   ]

# if "test" not in st.session_state:
#     st.session_state["test"] = None 

# def onChange():
    
#     st.session_state["test"] = st.session_state["hiiiii"]



# test = chip_filter(chipData=data, on_change=onChange, key="hiiiii") 
# st.session_state["test"] = test

# st.write(st.session_state["test"])

if "test_text" not in st.session_state:
    st.session_state["test_text"] = None 

def onChangeTest():

    st.session_state["test_text"] = st.session_state["selection_options_test_"] 
    


roles_ = [{'index': 0, 'label': 'Assassin', 'clicked': False, 'disabled': False}, {'index': 1, 'label': 'Tank', 'clicked': False, 'disabled': False}, {'index': 2, 'label': 'Marksman', 'clicked': True, 'disabled': False}, {'index': 3, 'label': 'Mage', 'clicked': False, 'disabled': False}]
chip_filter(chipData=roles_, disabledOptions=True, on_change=onChangeTest, key="selection_options_test_")


st.write(st.session_state["test_text"])

