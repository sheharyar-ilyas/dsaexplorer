import streamlit as st
import pandas as pd
import time

st.logo(
    "logo_complete.png",        
    size="large",                  
    # link="https://dsaexplorer.streamlit.app",    
    icon_image="icon.png",  
)

# Set page configurations
st.set_page_config(layout="wide", page_title="DSA Explorer",page_icon="icon.png")

# ⚙️ Configuration
CHUNK_SIZE = 1000  

# 🔒 1. Safe Cache Loader (Survives browser refreshes!)
@st.cache_data(show_spinner="Recovering file from cache...")
def load_and_cache_csv(file_bytes):
    # This keeps a master copy safely stored in server memory
    return pd.read_csv(file_bytes)

# 🛠️ 2. Initialize Session State Variables
if "current_row" not in st.session_state:
    st.session_state.current_row = 0
if "status" not in st.session_state:
    st.session_state.status = "stopped"  
if "processed_data" not in st.session_state:
    st.session_state.processed_data = pd.DataFrame()

st.title("🔄 Load the CSV File To sort the data")

# 📂 3. File Uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    # Use cache to load or recover the file securely 
    df = load_and_cache_csv(uploaded_file)
    total_rows = len(df)

    # 🕹️ 4. Control UI Buttons (Horizontal Layout)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("▶️ Start / Resume", disabled=(st.session_state.status == "running" or st.session_state.current_row >= total_rows)):
            st.session_state.status = "running"
            st.rerun()

    with col2:
        if st.button("⏸️ Pause", disabled=(st.session_state.status != "running")):
            st.session_state.status = "paused"
            st.rerun()

    with col3:
        if st.button("⏹️ Stop / Reset"):
            st.session_state.status = "stopped"
            st.session_state.current_row = 0
            st.session_state.processed_data = pd.DataFrame()
            st.rerun()

    with col4:
        st.write(f"**Status:** {st.session_state.status.upper()}")

    # 📊 5. Progress Indicators
    progress_percentage = min(1.0, st.session_state.current_row / total_rows) if total_rows > 0 else 0
    progress_bar = st.progress(progress_percentage)
    status_text = st.empty()
    status_text.text(f"Processed {st.session_state.current_row} of {total_rows} rows ({int(progress_percentage * 100)}%)")

    # 📈 6. Live Data Container
    table_placeholder = st.empty()
    
    # Render what is currently processed so far
    if not st.session_state.processed_data.empty:
        table_placeholder.dataframe(st.session_state.processed_data)

    # 🔄 7. Processing Loop (Runs only when status is 'running')
    if st.session_state.status == "running":
        while st.session_state.current_row < total_rows and st.session_state.status == "running":
            start_idx = st.session_state.current_row
            end_idx = min(start_idx + CHUNK_SIZE, total_rows)
            
            chunk = df.iloc[start_idx:end_idx]
            
            if st.session_state.processed_data.empty:
                st.session_state.processed_data = chunk
            else:
                st.session_state.processed_data = pd.concat([st.session_state.processed_data, chunk], ignore_index=True)
            
            st.session_state.current_row = end_idx
            
            progress_percentage = st.session_state.current_row / total_rows
            progress_bar.progress(progress_percentage)
            status_text.text(f"Processed {st.session_state.current_row} of {total_rows} rows ({int(progress_percentage * 100)}%)")
            
            table_placeholder.dataframe(st.session_state.processed_data)
            time.sleep(0.3) 
            
            if st.session_state.current_row >= total_rows:
                st.session_state.status = "stopped"
                st.success("🎉 CSV Chunk Processing Completed!")
                st.rerun()

else:
    # Reset state if file is removed manually
    st.session_state.current_row = 0
    st.session_state.processed_data = pd.DataFrame()
    st.session_state.status = "stopped"
    st.info("Please upload a CSV file to begin.")
