import streamlit as st


pages = [
    st.Page("views/intro.py", title="Home", icon=":material/home:", default=True),
    st.Page("views/fileUploader.py", title="Upload File", icon=":material/travel_explore:"),
    st.Page("views/explorer.py", title="Search & Filter", icon=":material/search:"),
    st.Page("views/sorting.py", title="Sorting Lab", icon=":material/sort:"),
    st.Page("views/benchmark.py", title="Benchmark", icon=":material/speed:"),
]
st.navigation(pages).run()