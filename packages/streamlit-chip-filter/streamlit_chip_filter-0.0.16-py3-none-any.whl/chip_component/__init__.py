import os
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True  

if not _RELEASE:
    _chip_filter= components.declare_component(
        
        "chip_filter",

        url="http://localhost:3001",
    )
else:

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _chip_filter = components.declare_component("chip_filter", path=build_dir)

def chip_filter(chipData=None, disabledOptions=False, styles=None, on_change=None, key=None, default=None):
    
    component_value = _chip_filter(chipData=chipData, disabledOptions=disabledOptions, on_change_handler=on_change, styles=styles, key=key, default=default)

    return component_value
