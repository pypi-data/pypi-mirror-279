import streamlit as st
from __init__ import chip_filter
import streamlit_antd_components as sac
# from chip_component import chip_filter

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

# st.html(
#     """
#         <style>
#             iframe{
#                 height: 100px;
#             }
#         </style>
#     """
# )

if "test_text" not in st.session_state:
    st.session_state["test_text"] = None 

if "input_list_" not in st.session_state:
    st.session_state["input_list_"] = [{"label":"apple", "disabled":False }, {"label":"google", "disabled":False}, {"label":"github", "disabled":False} ]

if "test_list_" not in st.session_state:
    # list_ = [{"label":"apple", "disabled":False }, {"label":"google", "disabled":False}, {"label":"github", "disabled":False} ]

    list_res_ = []
    for l in st.session_state["input_list_"]:
        list_res_.append(
            sac.ChipItem(label=l["label"], disabled=l["disabled"])
        )
        
    st.session_state["test_list_"] = list_res_
    
# st.write(
#     [i for i, s in enumerate(st.session_state["test_list_"]) if 'apple' in s]
# )

def onChangeTest():

    # print(st.session_state["testing_list"])
    # for dict_, i in zip(st.session_state["input_list_"], range(len(st.session_state["input_list_"]))):
    #     # print(dict_, st.session_state["testing_list"])
    #     if dict_["label"] != st.session_state["testing_list"]:
    #         st.session_state["input_list_"][i]["disabled"] = True
    #     else:
    #         st.session_state["input_list_"][i]["disabled"] = False
    
    # st.session_state["test_list_"] = st.session_state["input_list_"] 


    # expectedResult = [d for d in st.session_state["input_list_"] if d['label'] in st.session_state["testing_list"]] 

    st.session_state["test_text"] = st.session_state["selection_options_test_"] 

@st.experimental_dialog(title="Test Dialog", width="large")
def test_dialog():
    # sac.chip(
    #     items=st.session_state["test_list_"], label='', index=0, align='center', size="xs", radius='sm', variant="outline", color="black", multiple=False, on_change=onChangeTest, key="testing_list"
    # )

    roles_ = [{'index': 0, 'label': 'Assassin', 'clicked': False, 'disabled': False}, {'index': 1, 'label': 'Tank', 'clicked': False, 'disabled': False}, {'index': 2, 'label': 'Marksman', 'clicked': True, 'disabled': False}, {'index': 3, 'label': 'Mage', 'clicked': False, 'disabled': False}]
    chip_filter(chipData=roles_, disabledOptions=True, on_change=onChangeTest, key="selection_options_test_")
    st.write(st.session_state["test_text"])

test_dialog()

# st.write(st.session_state["test_text"])

