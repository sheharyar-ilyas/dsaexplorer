import streamlit as st


# set the page configuration

st.set_page_config(layout="wide", page_title="DSA Explorer",page_icon="icon.png")

st.logo(
    "logo_complete.png",        
    size="large",                  
    # link="https://dsaexplorer.streamlit.app",    
    icon_image="icon.png",  
)


pages = [
    st.Page("views/intro.py", title="Home", icon=":material/home:", default=True),
    st.Page("views/explorer.py", title="Search & Filter", icon=":material/search:"),
    st.Page("views/sorting.py", title="Sorting Lab", icon=":material/sort:"),
    st.Page("views/benchmark.py", title="Benchmark", icon=":material/speed:"),
]
st.navigation(pages).run()