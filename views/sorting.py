import time
import pandas as pd
import streamlit as st

from data_manager import get_data

from Sortingalgorithms.bubbleSort import BubbleSort
from Sortingalgorithms.SelectionSort import SelectionSort
from Sortingalgorithms.InsertionSort import InsertionSort
from Sortingalgorithms.MergeSort import MergeSort
from Sortingalgorithms.QuickSort import QuickSort
from Sortingalgorithms.CountingSort import CountingSort
from Sortingalgorithms.RadixSort import RadixSort
from Sortingalgorithms.bucketSort import BucketSort

from Sortingalgorithms.algorithmsInfo import ALGORITHM_INFO


# ---------------------------------------------------------
# 1. Register all sorting algorithms
# ---------------------------------------------------------

ALGORITHMS = {
    "Bubble Sort": BubbleSort,
    "Selection Sort": SelectionSort,
    "Insertion Sort": InsertionSort,
    "Merge Sort": MergeSort,
    "Quick Sort": QuickSort,
    "Counting Sort": CountingSort,
    "Radix Sort": RadixSort,
    "Bucket Sort": BucketSort,
}

INTEGER_ONLY = {
    "Counting Sort",
    "Radix Sort",
}

SLOW_ALGORITHMS = {
    "Bubble Sort",
    "Selection Sort",
    "Insertion Sort",
}


# ---------------------------------------------------------
# 2. Load the complete dataset
# ---------------------------------------------------------

st.title("Sorting Lab")
st.caption(
    "Sort your complete dataset using different algorithms "
)

try:
    df = get_data()

except (FileNotFoundError, pd.errors.EmptyDataError) as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()

if df.empty:
    st.warning("The dataset is empty.")
    st.stop()

st.write(f"**Total rows:** {len(df):,}")
st.write(f"**Total columns:** {len(df.columns):,}")

st.dataframe(df, use_container_width=True, height=250)


# ---------------------------------------------------------
# 3. Single-column sorting
# ---------------------------------------------------------

st.divider()
st.header("Single-Column Sorting")

sort_column = st.selectbox(
    "Select the column to sort",
    options=list(df.columns),
)

algorithm_name = st.selectbox(
    "Select sorting algorithm",
    options=list(ALGORITHMS.keys()),
)

order = st.radio(
    "Sorting order",
    ["Ascending", "Descending"],
    horizontal=True,
)

info = ALGORITHM_INFO[algorithm_name]

info_col1, info_col2 = st.columns(2)

info_col1.metric(
    "Time Complexity",
    info["complexity"],
)

info_col2.metric(
    "Stable",
    info["stable"],
)

if algorithm_name in SLOW_ALGORITHMS:
    st.warning(
        "This algorithm has O(n²) worst-case time complexity. "
        "It will process the entire dataset, so large datasets "
        "may take a long time."
    )


# ---------------------------------------------------------
# 4. Sort all rows while keeping every column
# ---------------------------------------------------------

if st.button(
    "Sort Complete Dataset",
    type="primary",
    use_container_width=True,
):
    st.session_state.pop("last_sort_metrics", None)
    st.session_state.pop("last_sort_result", None)

    try:
        # Separate missing and non-missing values.
        column_values = df[sort_column].tolist()

        missing_indices = []
        valid_values = []
        valid_indices = []

        for index, value in enumerate(column_values):
            if pd.isna(value):
                missing_indices.append(index)
            else:
                valid_values.append(value)
                valid_indices.append(index)

        if algorithm_name in INTEGER_ONLY:
            if any(
                not isinstance(value, int)
                or isinstance(value, bool)
                for value in valid_values
            ):
                st.error(
                    f"{algorithm_name} requires integer values. "
                    "Choose an integer column or use another algorithm."
                )
                st.stop()

        # Get the selected column's values
        column_values = df[sort_column].tolist()

        # Keep the original row indices
        row_indices = list(range(len(df)))

        # Sort the values using the selected algorithm
        reverse = order == "Descending"
        algorithm = ALGORITHMS[algorithm_name]

        start_time = time.perf_counter()

        sorted_values, comparisons, moves = algorithm(
            column_values,
            reverse=reverse,
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        # Match each sorted value to its original row index.
        # This version handles duplicate values too.
        unused_indices = list(row_indices)
        sorted_indices = []

        for value in sorted_values:
            for position in range(len(unused_indices)):
                original_index = unused_indices[position]

                if column_values[original_index] == value:
                    sorted_indices.append(original_index)
                    unused_indices.pop(position)
                    break

        # Rearrange the complete rows, keeping all columns
        sorted_df = df.iloc[sorted_indices].reset_index(drop=True)

        st.session_state["last_sort_result"] = sorted_df

        st.session_state["last_sort_metrics"] = {
            "algorithm": algorithm_name,
            "column": sort_column,
            "order": order,
            "time": elapsed_ms,
            "comparisons": comparisons,
            "moves": moves,
            "rows": len(df),
        }

    except (ValueError, TypeError, RecursionError, OverflowError) as error:
        st.error(f"Sorting failed: {error}")


# ---------------------------------------------------------
# 5. Show metrics and the complete sorted dataset
# ---------------------------------------------------------

if "last_sort_metrics" in st.session_state:
    metrics = st.session_state["last_sort_metrics"]

    st.divider()
    st.subheader("Sorting Performance")

    st.write(f"**Algorithm:** {metrics['algorithm']}")
    st.write(f"**Column:** {metrics['column']}")
    st.write(f"**Order:** {metrics['order']}")
    st.write(f"**Rows processed:** {metrics['rows']:,}")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Execution Time",
        f"{metrics['time']:.3f} ms",
    )

    col2.metric(
        "Comparisons",
        f"{metrics['comparisons']:,}",
    )

    col3.metric(
        "Swaps / Moves",
        f"{metrics['moves']:,}",
    )

    st.caption(
        "Execution time measures the selected algorithm call. "
        "Move counts depend on the algorithm's implementation."
    )

    st.subheader("Complete Sorted Dataset")

    st.dataframe(
        st.session_state["last_sort_result"],
        use_container_width=True,
        height=450,
    )

    csv_data = st.session_state["last_sort_result"].to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Sorted Dataset as CSV",
        data=csv_data,
        file_name="sorted_dataset.csv",
        mime="text/csv",
        use_container_width=True,
    )
