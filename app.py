import streamlit as st

# set the page configuration

st.set_page_config(layout="wide", page_title="DSA Explorer",page_icon="icon.png")

st.logo(
    "logo_complete.png",        
    size="large",                  
    # link="https://dsaexplorer.streamlit.app",    
    icon_image="icon.png",  
)

# Hide ONLY the Edit button at the top and 'Manage app' at the bottom
hide_selective_style = """
    <style>
    /* 1. Hide only the Edit (pencil) button in the top toolbar */
    header [title*="Edit"],
    [data-testid="stToolbar"] a[title*="Edit"],
    [data-testid="stToolbar"] button:has(svg path[d*="M3"]) {
        display: none !important;
    }
    
    /* 2. Hide the 'Manage app' button at the bottom right */
    div[data-testid="stAppDeployButton"], 
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }
    </style>
"""

st.markdown(hide_selective_style, unsafe_allow_html=True)


pages = [
    st.Page("views/intro.py", title="Home", icon=":material/home:", default=True),
    st.Page("views/explorer.py", title="Search & Filter", icon=":material/search:"),
    st.Page("views/sorting.py", title="Sorting Lab", icon=":material/sort:"),
    st.Page("views/multi_sort.py", title="Multisorting Lab", icon=":material/layers:"),
    st.Page("views/benchmark.py", title="Benchmark", icon=":material/speed:"),
]
st.navigation(pages).run()