
import time
import math
import numbers

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
# 1. Register all eight algorithms
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
# 2. Page heading
# ---------------------------------------------------------

st.title("Sorting Algorithm Benchmark")

st.write(
    "Compare the performance of sorting algorithms "
    "using the complete dataset."
)

st.info(
    "In Benchmarking we see running of all the sorting algorithms on the complete dataset. This is the complete overview of all sorting algorithms performance"
)


# ---------------------------------------------------------
# 3. Load the complete dataset
# ---------------------------------------------------------

try:
    df = get_data()

except (FileNotFoundError, pd.errors.EmptyDataError) as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()

if df.empty:
    st.warning("The dataset is empty.")
    st.stop()

st.metric("Total Dataset Rows", f"{len(df):,}")
st.metric("Total Dataset Columns", f"{len(df.columns):,}")


# ---------------------------------------------------------
# 4. Select the column and sorting direction
# ---------------------------------------------------------

column = st.selectbox(
    "Select the column to benchmark",
    options=list(df.columns),
)

direction = st.radio(
    "Sorting order",
    ["Ascending", "Descending"],
    horizontal=True,
)

reverse = direction == "Descending"

st.write("**Algorithms included:**")

st.write(", ".join(ALGORITHMS.keys()))

st.warning(
    "Bubble Sort, Selection Sort, and Insertion Sort can be "
    "very slow on large datasets. All algorithms will process "
    "the complete selected column, without a row limit."
)


# ---------------------------------------------------------
# 5. Run the benchmark
# ---------------------------------------------------------

if st.button(
    "Run Benchmark on Complete Dataset",
    type="primary",
    use_container_width=True,
):

    # Take every non-missing value from the selected column.
    # No filtered DataFrame and no head() limit are used.
    values = df[column].tolist()

    missing_count = sum(
        1 for value in values if pd.isna(value)
    )

    data = [
        value for value in values
        if not pd.isna(value)
    ]

    if not data:
        st.error("The selected column has no non-missing values.")
        st.stop()

    results = []
    skipped = []

    st.write(f"**Selected column:** {column}")
    st.write(f"**Total dataset rows:** {len(df):,}")
    st.write(f"**Non-missing values benchmarked:** {len(data):,}")
    st.write(f"**Missing values kept aside:** {missing_count:,}")

    # Convert whole-number floats to integers for integer-only
    # algorithms, but only when every value is a whole number.
    integer_data = all(
        isinstance(value, numbers.Integral)
        and not isinstance(value, bool)
        for value in data
    )

    if not integer_data:
        integer_data = all(
            isinstance(value, numbers.Real)
            and not isinstance(value, bool)
            and math.isfinite(value)
            and float(value).is_integer()
            for value in data
        )

    # -----------------------------------------------------
    # Run every algorithm on the same complete value list
    # -----------------------------------------------------

    progress = st.progress(0)
    status = st.empty()

    total_algorithms = len(ALGORITHMS)

    for position, (name, algorithm) in enumerate(
        ALGORITHMS.items(), start=1
    ):
        status.write(f"Running {name} ({position}/{total_algorithms})...")

        try:
            # Check algorithm requirements before running.
            if name in INTEGER_ONLY and not integer_data:
                skipped.append({
                    "Algorithm": name,
                    "Reason": "Requires integer values.",
                })

                progress.progress(
                    position / total_algorithms
                )
                continue

            if name == "Bucket Sort":
                if not all(
                    isinstance(value, numbers.Real)
                    and not isinstance(value, bool)
                    and math.isfinite(value)
                    for value in data
                ):
                    skipped.append({
                        "Algorithm": name,
                        "Reason": "Requires finite numeric values.",
                    })

                    progress.progress(
                        position / total_algorithms
                    )
                    continue

            # Give each algorithm its own copy of the same data.
            # Convert integer-only inputs when necessary.
            if name in INTEGER_ONLY:
                input_data = [int(value) for value in data]
            else:
                input_data = list(data)

            start_time = time.perf_counter()

            sorted_values, comparisons, moves = algorithm(
                input_data,
                reverse=reverse,
            )

            elapsed_ms = (
                time.perf_counter() - start_time
            ) * 1000

            results.append({
                "Algorithm": name,
                "Execution Time (ms)": round(elapsed_ms, 3),
                "Comparisons": comparisons,
                "Moves / Swaps": moves,
                "Time Complexity": ALGORITHM_INFO[name]["complexity"],
                "Stable": ALGORITHM_INFO[name]["stable"],
                "Rows Sorted": len(sorted_values),
                "_elapsed": elapsed_ms,
            })

        except (
            ValueError,
            TypeError,
            RecursionError,
            OverflowError,
        ) as error:
            skipped.append({
                "Algorithm": name,
                "Reason": str(error),
            })

        progress.progress(position / total_algorithms)

    progress.empty()
    status.empty()

    # -----------------------------------------------------
    # Save and display results
    # -----------------------------------------------------

    if results:
        # Rank only algorithms that completed successfully.
        results.sort(key=lambda item: item["_elapsed"])

        for rank, result in enumerate(results, start=1):
            result["Rank"] = rank
            result.pop("_elapsed")

        results_df = pd.DataFrame(results)

        st.session_state["benchmark_results"] = results_df
        st.session_state["benchmark_column"] = column
        st.session_state["benchmark_order"] = direction
        st.session_state["benchmark_rows"] = len(df)
        st.session_state["benchmark_values"] = len(data)

        st.success(
            f"Benchmark completed for {len(data):,} non-missing "
            f"values from the complete dataset."
        )

    else:
        st.error(
            "No algorithm completed successfully. "
            "Check the selected column's data type."
        )

    if skipped:
        st.subheader("Algorithms Not Run Successfully")
        st.dataframe(
            pd.DataFrame(skipped),
            use_container_width=True,
        )


# ---------------------------------------------------------
# 6. Display saved benchmark results
# ---------------------------------------------------------

if "benchmark_results" in st.session_state:
    results_df = st.session_state["benchmark_results"]

    st.divider()
    st.subheader("Benchmark Comparison")

    st.write(
        f"**Column:** {st.session_state['benchmark_column']}"
    )
    st.write(
        f"**Order:** {st.session_state['benchmark_order']}"
    )
    st.write(
        f"**Total dataset rows:** "
        f"{st.session_state['benchmark_rows']:,}"
    )
    st.write(
        f"**Non-missing values tested:** "
        f"{st.session_state['benchmark_values']:,}"
    )

    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True,
    )

    fastest = results_df.iloc[0]

    st.subheader("Fastest Measured Algorithm")

    st.metric(
        "Algorithm",
        fastest["Algorithm"],
    )

    st.metric(
        "Execution Time",
        f"{fastest['Execution Time (ms)']:.3f} ms",
    )

    st.caption(
        "The fastest result is based on this particular run, "
        "dataset, column, and sorting direction. It is not a "
        "guarantee that the algorithm is always the fastest."
    )

    csv_data = results_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Benchmark Results",
        data=csv_data,
        file_name="benchmark_results.csv",
        mime="text/csv",
        use_container_width=True
    )

