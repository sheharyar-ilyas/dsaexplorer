import streamlit as st 
from data_manager import get_data, get_dataset_info
from Sortingalgorithms.algorithmsInfo import ALGORITHM_INFO

st.title("DSA Explorer")
st.subheader("Sort, filter, search and benchmark on a real dataset")

st.write(
    "We uses one fixed stored dataset to sort the them "
)

try:
    info = get_dataset_info()
    c1, c2 = st.columns(2)
    c1.metric("Entries", f"{info['rows']:,}")
    c2.metric("Columns", f"{info['columns']:,}")

    st.divider()

    st.markdown("### What you can do")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            **Search & Filter**
            - Search any column
            - Starts with / Ends with / Contains
            - Numeric comparisons
            - AND / OR / NOT composite filters
            """
        )

        st.markdown(
            """
            **Multi-Level Sorting**
            - Sort using multiple columns
            - Choose ascending or descending order
            - Sort the complete dataset or filtered results
            """
        )

    with col2:
        st.markdown(
            """
            **Sorting Lab**
            - 8 sorting algorithms
            - Time in milliseconds
            - Comparisons and swaps
            - Complexity and stability information
            """
        )

        st.markdown(
            """
            **Benchmark**
            - Run all algorithms on one selected column
            - Compare time, comparisons and swaps
            """
        )

    st.divider()
    st.markdown("### Algorithms included")

    algorithm_table = []
    for name, info_item in ALGORITHM_INFO.items():
        algorithm_table.append(
            {
                "Algorithm": name,
                "Time Complexity": info_item["complexity"],
                "Stable": info_item["stable"],
            }
        )

    st.dataframe(algorithm_table, width="stretch", hide_index=True)

    st.markdown("### Dataset Preview")
    st.dataframe(get_data().head(15000), width="stretch")

except Exception as error:
    st.error(str(error))
