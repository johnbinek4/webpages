# Streamlit Tutorial 24OCT24

import streamlit as sl

sl.title('Hi, I am a bitch')
sl.subheader('subheader')
sl.header('header')
sl.text('paragraghs')
sl.markdown("**Hello** *World*")

# JSON Functions

# Imbed Videos

#sl.image("Image.jpg")

# widgets

def change():
    print("Changed")
sl.checkbox("Checkbox", on_change=change)

