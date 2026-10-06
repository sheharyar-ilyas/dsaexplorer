import streamlit as st
import time
import random
import copy
import pandas as pd

st.logo(
    "icon.png",        
    size="large",                  
    link="https://dsaexplorer.streamlit.app",  
    icon_image="icon.png",  
)

# Set page configurations
st.set_page_config(layout="wide", page_title="DSA Explorer",page_icon="icon.png")
st.title("📊 CS200 - Sorting Algorithm Benchmark Dashboard")

# ---------------------------------------------------------
# 1. GENERATE MOCK DATASET (Simulating 15k Scraped Entities)
# ---------------------------------------------------------
@st.cache_data
def load_mock_data():
    """Generates a dataset matching the required 8 attributes."""
    data = []
    categories = ["Computer Science", "Physics", "Mathematics", "Biology", "Chemistry"]
    for i in range(15000):
        data.append({
            "ID": i + 1,
            "Title": f"Academic Research Paper Title Number {i+1}",
            "Primary Author": f"Author_{random.randint(100, 999)}",
            "Co-Authors": random.randint(0, 10),              # Numerical column to sort
            "Year": random.randint(2010, 2026),               # Numerical column to sort
            "Category": random.choice(categories),
            "Abstract Word Count": random.randint(150, 500),  # Numerical column to sort
            "Page Count": random.randint(5, 50)               # Numerical column to sort
        })
    return data

dataset = load_mock_data()

# ---------------------------------------------------------
# 2. CUSTOM SORTING ALGORITHMS WITH COUNTERS
# ---------------------------------------------------------

# --- BUBBLE SORT (Class Studied - Unstable Version/Stable base) ---
def bubble_sort(arr, key):
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            comparisons += 1
            if arr[j][key] > arr[j+1][key]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swaps += 1
    return arr, comparisons, swaps

# --- INSERTION SORT (Class Studied) ---
def insertion_sort(arr, key):
    comparisons = 0
    swaps = 0
    for i in range(1, len(arr)):
        current_val = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j][key] > current_val[key]:
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1
            else:
                break
        arr[j + 1] = current_val
    return arr, comparisons, swaps

# --- MERGE SORT (Additional 1) ---
def merge_sort(arr, key):
    comparisons = 0
    swaps = 0
    
    if len(arr) <= 1:
        return arr, 0, 0
        
    mid = len(arr) // 2
    left, comp_l, swap_l = merge_sort(arr[:mid], key)
    right, comp_r, swap_r = merge_sort(arr[mid:], key)
    
    comparisons += (comp_l + comp_r)
    swaps += (swap_l + swap_r)
    
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i][key] <= right[j][key]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            swaps += 1
            
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, comparisons, swaps

# --- QUICK SORT (Additional 2) ---
def quick_sort(arr, key):
    comp = [0]
    swap = [0]
    
    def _quick_sort(items, low, high):
        if low < high:
            pivot_idx = partition(items, low, high)
            _quick_sort(items, low, pivot_idx - 1)
            _quick_sort(items, pivot_idx + 1, high)

    def partition(items, low, high):
        pivot = items[high][key]
        i = low - 1
        for j in range(low, high):
            comp[0] += 1
            if items[j][key] <= pivot:
                i += 1
                items[i], items[j] = items[j], items[i]
                swap[0] += 1
        items[i + 1], items[high] = items[high], items[i + 1]
        swap[0] += 1
        return i + 1

    _quick_sort(arr, 0, len(arr) - 1)
    return arr, comp[0], swap[0]

# --- HEAP SORT (Additional 3) ---
def heap_sort(arr, key):
    comp = [0]
    swap = [0]
    
    def heapify(items, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        
        if l < n:
            comp[0] += 1
            if items[l][key] > items[largest][key]:
                largest = l
        if r < n:
            comp[0] += 1
            if items[r][key] > items[largest][key]:
                largest = r
                
        if largest != i:
            items[i], items[largest] = items[largest], items[i]
            swap[0] += 1
            heapify(items, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        swap[0] += 1
        heapify(arr, i, 0)
        
    return arr, comp[0], swap[0]

# ---------------------------------------------------------
# 3. INTERACTIVE CONTROL UI
# ---------------------------------------------------------
st.sidebar.header("🎛️ Control Panel")

# Columns selection configuration
sort_column = st.sidebar.selectbox(
    "Choose Column to Sort By:",
    ["Co-Authors", "Year", "Abstract Word Count", "Page Count"]
)

# Sorting Scope criteria (Full Dataset vs Filtered Slice)
scope = st.sidebar.radio("Sorting Scope:", ["Full Dataset (15k entries)", "Small Slice (Top 500 items)"])
sample_size = 15000 if scope == "Full Dataset (15k entries)" else 500
active_data = dataset[:sample_size]

run_benchmark = st.sidebar.button("⚡ Run Sorting Benchmark")

# ---------------------------------------------------------
# 4. BENCHMARK EXECUTION LOGIC
# ---------------------------------------------------------
if run_benchmark:
    st.subheader(f"⏱️ Evaluation Results (Sorting by: {sort_column} on {sample_size} records)")
    
    algorithms = {
        "Bubble Sort": {"func": bubble_sort, "complexity": "O(N²)", "stable": "Yes"},
        "Insertion Sort": {"func": insertion_sort, "complexity": "O(N²)", "stable": "Yes"},
        "Merge Sort": {"func": merge_sort, "complexity": "O(N log N)", "stable": "Yes"},
        "Quick Sort": {"func": quick_sort, "complexity": "O(N log N)", "stable": "No"},
        "Heap Sort": {"func": heap_sort, "complexity": "O(N log N)", "stable": "No"}
    }
    
    results = []
    
    # Progress feedback display framework
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, (algo_name, algo_meta) in enumerate(algorithms.items()):
        status_text.text(f"Running {algo_name}...")
        
        # Deepcopy to prevent pre-sorting side-effects across iterations
        data_copy = copy.deepcopy(active_data)
        
        # Execution time measurement tracking
        start_time = time.perf_counter()
        sorted_arr, comparisons, swaps = algo_meta["func"](data_copy, sort_column)
        end_time = time.perf_counter()
        
        elapsed_ms = (end_time - start_time) * 1000
        
        results.append({
            "Algorithm": algo_name,
            "Time (ms)": round(elapsed_ms, 2),
            "Comparisons": comparisons,
            "Swaps / Inversions": swaps,
            "Time Complexity": algo_meta["complexity"],
            "Stable": algo_meta["stable"]
        })
        
        progress_bar.progress((idx + 1) / len(algorithms))
        
    status_text.success("Benchmark Completed Successfully!")
    
    # Render Metrics Matrix Data Frame Table UI Component
    results_df = pd.DataFrame(results)
    st.dataframe(results_df, use_container_width=True)
    
    # Render Comparative Visual Graphics Charts Panel
    st.subheader("📊 Execution Speed Comparison")
    st.bar_chart(data=results_df, x="Algorithm", y="Time (ms)", use_container_width=True)

else:
    st.info("👈 Use the control panel side sidebar to choose your features and hit **Run Sorting Benchmark**.")
    st.subheader("Previewing Original Collected Dataset (Unsorted)")
    st.dataframe(pd.DataFrame(active_data[:100]), use_container_width=True)
