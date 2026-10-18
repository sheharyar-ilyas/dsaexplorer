import math
import numbers
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
NUMERIC_ALGORITHMS = {"Counting Sort", "Radix Sort", "Bucket Sort"}
INTEGER_ALGORITHMS = {"Counting Sort", "Radix Sort"}


def missing(value):
    try:
        result = pd.isna(value)
        return bool(result) if not hasattr(result, "__len__") else False
    except (TypeError, ValueError):
        return False


def value_key(value):
    if missing(value):
        return ("MISSING",)
    try:
        hash(value)
        return ("VALUE", value)
    except TypeError:
        return ("VALUE_REPR", repr(value))


def validate_column(values, algorithm_name):
    values = [v for v in values if not missing(v)]

    if algorithm_name in NUMERIC_ALGORITHMS:
        if any(isinstance(v, bool) or not isinstance(v, numbers.Number) for v in values):
            return f"{algorithm_name} is for numeric data, not strings. Select a numeric column or another algorithm."

    if algorithm_name in INTEGER_ALGORITHMS:
        for value in values:
            try:
                if not math.isfinite(float(value)) or not float(value).is_integer():
                    return f"{algorithm_name} requires integer numeric values. Select another algorithm for decimal values."
            except (TypeError, ValueError, OverflowError):
                return f"{algorithm_name} requires integer numeric values. Select another algorithm."

    if algorithm_name == "Bucket Sort":
        for value in values:
            try:
                if not math.isfinite(float(value)):
                    return "Bucket Sort requires finite numeric values. Select another algorithm."
            except (TypeError, ValueError, OverflowError):
                return "Bucket Sort requires numeric values. Select another algorithm."

    if algorithm_name not in NUMERIC_ALGORITHMS and values:
        try:
            sorted(values)
        except (TypeError, ValueError):
            return "Values in this column cannot be compared with each other. Select another algorithm or column."

    return None


def multi_sort_positions(df, levels):
    comparisons = 0
    moves = 0

    def sort_group(positions, level_index):
        nonlocal comparisons, moves

        if level_index >= len(levels) or len(positions) <= 1:
            return positions

        column, algorithm_name, direction = levels[level_index]
        algorithm = ALGORITHMS[algorithm_name]

        # Keep rows with equal values together.
        groups = {}
        values_by_key = {}
        missing_positions = []

        for position in positions:
            value = df.iloc[position][column]
            if missing(value):
                missing_positions.append(position)
                continue

            key = value_key(value)
            if key not in groups:
                groups[key] = []
                values_by_key[key] = value
            groups[key].append(position)

        keys = list(groups)
        distinct_values = [values_by_key[key] for key in keys]

        if len(distinct_values) > 1:
            sorted_values, compared, moved = algorithm(
                distinct_values[:], reverse=(direction == "Descending")
            )
            comparisons += compared
            moves += moved

            # Match each sorted value to its original group.
            remaining_keys = keys[:]
            ordered_keys = []
            for sorted_value in sorted_values:
                found = None
                for i, key in enumerate(remaining_keys):
                    try:
                        same = bool(values_by_key[key] == sorted_value)
                    except (TypeError, ValueError):
                        same = False
                    if same:
                        found = i
                        break
                if found is None:
                    raise ValueError("Could not match a sorted value to its original rows.")
                ordered_keys.append(remaining_keys.pop(found))
            keys = ordered_keys

        result = []
        for key in keys:
            # The next sorting level only sorts rows tied on this column.
            result.extend(sort_group(groups[key], level_index + 1))

        # Missing values are placed last; lower levels can order them too.
        if missing_positions:
            result.extend(sort_group(missing_positions, level_index + 1))

        return result

    return sort_group(list(range(len(df))), 0), comparisons, moves


st.title("Multi-Level Sorting")
st.caption("Choose a column, algorithm, and order for each sorting level. All columns stay attached to their original rows.")

try:
    df = get_data()
    if df is None or df.empty:
        st.warning("No dataset is available. Load a dataset first.")
        st.stop()

    columns = list(df.columns)
    if "multi_sort_level_count" not in st.session_state:
        st.session_state.multi_sort_level_count = 2

    add, remove = st.columns(2)
    with add:
        if st.button("➕ Add sorting level", use_container_width=True):
            st.session_state.multi_sort_level_count += 1
            st.rerun()
    with remove:
        if st.button(
            "➖ Remove sorting level",
            use_container_width=True,
            disabled=st.session_state.multi_sort_level_count <= 1,
        ):
            st.session_state.multi_sort_level_count -= 1
            st.rerun()

    st.write("Level 1 has the highest priority. Later levels sort rows tied at earlier levels.")
    levels = []

    for i in range(st.session_state.multi_sort_level_count):
        st.subheader(f"Sorting level {i + 1}")
        c1, c2, c3 = st.columns([1.3, 1.5, 1])
        with c1:
            column = st.selectbox("Column", columns, key=f"multi_column_{i}")
        with c2:
            algorithm_name = st.selectbox("Algorithm", list(ALGORITHMS), key=f"multi_algorithm_{i}")
        with c3:
            direction = st.selectbox("Order", ["Ascending", "Descending"], key=f"multi_direction_{i}")

        if algorithm_name in INTEGER_ALGORITHMS:
            st.info(f"{algorithm_name} is for integer numeric data, not strings or decimal values.")
        elif algorithm_name == "Bucket Sort":
            st.info("Bucket Sort is for numeric data, not strings.")

        levels.append((column, algorithm_name, direction))

    if st.button("Apply Multi-Level Sorting", type="primary", use_container_width=True):
        error_message = None
        for column, algorithm_name, direction in levels:
            error_message = validate_column(df[column].tolist(), algorithm_name)
            if error_message:
                st.error(f"Column '{column}': {error_message}")
                break

        if not error_message:
            try:
                start = time.perf_counter()
                positions, comparisons, moves = multi_sort_positions(df, levels)
                elapsed_ms = (time.perf_counter() - start) * 1000
                sorted_df = df.iloc[positions].reset_index(drop=True)

                st.session_state["multi_sort_result"] = sorted_df
                st.session_state["multi_sort_stats"] = (elapsed_ms, comparisons, moves)
            except Exception as error:
                st.error(f"Sorting failed: {error}")

    if "multi_sort_result" in st.session_state:
        result = st.session_state["multi_sort_result"]
        elapsed_ms, comparisons, moves = st.session_state["multi_sort_stats"]
        st.divider()
        st.subheader("Sorted Dataset")
        a, b, c = st.columns(3)
        a.metric("Rows", f"{len(result):,}")
        b.metric("Time", f"{elapsed_ms:.3f} ms")
        c.metric("Algorithm comparisons", f"{comparisons:,}")
        st.caption(f"Moves reported by the custom algorithms: {moves:,}. The counts cover sorting distinct values within groups.")
        st.dataframe(result, use_container_width=True, height=450)
        st.download_button(
            "Download sorted CSV",
            data=result.to_csv(index=False).encode("utf-8"),
            file_name="multi_sorted_data.csv",
            mime="text/csv",
            use_container_width=True,
        )

except Exception as error:
    st.error(f"Unable to load dataset: {error}")
