
import streamlit as st
import pandas as pd
from data_manager import get_data

st.title("Search & Filter")
st.caption("Search individual columns or combine multiple conditions with AND, OR and NOT.")

try:
    df = get_data()

    # ---------------------------------------------------------
    # Single-column search
    # ---------------------------------------------------------
    st.subheader("Search a column")

    col1, col2 = st.columns([1, 2])

    with col1:
        search_column = st.selectbox("Column", list(df.columns), key="single_search_column")

    with col2:
        search_value = st.text_input(
            "Search value",
            placeholder="Enter text or number...",
            key="single_search_value",
        )

    column_series = df[search_column]

    if pd.api.types.is_numeric_dtype(column_series):
        search_operation = st.selectbox(
            "Numeric operation",
            ["Equals", "Not equals", "Greater than", "Greater than or equal",
             "Less than", "Less than or equal"],
            key="numeric_operation",
        )
    else:
        search_operation = st.selectbox(
            "String operation",
            ["Contains", "Starts with", "Ends with", "Equals", "Not equals"],
            key="string_operation",
        )

    if st.button("Search", type="primary", use_container_width=True):
        try:
            if pd.api.types.is_numeric_dtype(column_series):
                number = float(search_value)
                if search_operation == "Equals":
                    mask = column_series == number
                elif search_operation == "Not equals":
                    mask = column_series != number
                elif search_operation == "Greater than":
                    mask = column_series > number
                elif search_operation == "Greater than or equal":
                    mask = column_series >= number
                elif search_operation == "Less than":
                    mask = column_series < number
                else:
                    mask = column_series <= number
            else:
                text = search_value.strip().lower()
                series = column_series.fillna("").astype(str).str.lower()

                if search_operation == "Contains":
                    mask = series.str.contains(text, regex=False)
                elif search_operation == "Starts with":
                    mask = series.str.startswith(text)
                elif search_operation == "Ends with":
                    mask = series.str.endswith(text)
                elif search_operation == "Equals":
                    mask = series == text
                else:
                    mask = series != text

            result = df[mask]
            st.session_state["search_result"] = result

        except ValueError:
            st.error("Please enter a valid value for this column.")

    if "search_result" in st.session_state:
        result = st.session_state["search_result"]
        st.success(f"{len(result):,} matching rows found.")
        st.dataframe(result, use_container_width=True, height=420)

    st.divider()

    # ---------------------------------------------------------
    # Composite search: AND / OR / NOT
    # ---------------------------------------------------------
    st.subheader("Composite Search")
    st.write("Create multiple conditions and combine them using AND, OR and NOT.")

    if "condition_count" not in st.session_state:
        st.session_state.condition_count = 2

    add_col, remove_col = st.columns(2)
    with add_col:
        if st.button("➕ Add condition"):
            st.session_state.condition_count += 1
            st.rerun()

    with remove_col:
        if st.button("➖ Remove condition") and st.session_state.condition_count > 2:
            st.session_state.condition_count -= 1
            st.rerun()

    conditions = []

    for i in range(st.session_state.condition_count):
        st.markdown(f"**Condition {i + 1}**")

        c1, c2, c3, c4 = st.columns([1.2, 1.5, 1.4, 2])

        with c1:
            col = st.selectbox(
                "Column",
                list(df.columns),
                key=f"condition_col_{i}",
            )

        series = df[col]

        with c2:
            if pd.api.types.is_numeric_dtype(series):
                operation = st.selectbox(
                    "Operation",
                    ["Equals", "Not equals", "Greater than", "Greater than or equal",
                     "Less than", "Less than or equal"],
                    key=f"condition_op_{i}",
                )
            else:
                operation = st.selectbox(
                    "Operation",
                    ["Contains", "Starts with", "Ends with", "Equals", "Not equals"],
                    key=f"condition_op_{i}",
                )

        with c3:
            connector = "AND"
            if i > 0:
                connector = st.selectbox(
                    "Combine with previous",
                    ["AND", "OR"],
                    key=f"condition_connector_{i}",
                )

        with c4:
            value = st.text_input(
                "Value",
                key=f"condition_value_{i}",
            )

        not_condition = st.checkbox(
            "NOT this condition",
            key=f"condition_not_{i}",
        )

        conditions.append((col, operation, value, connector, not_condition))

    if st.button("Apply Composite Search", type="primary", use_container_width=True):
        final_mask = None
        valid = True

        for i, (col, operation, value, connector, not_condition) in enumerate(conditions):
            series = df[col]

            try:
                if pd.api.types.is_numeric_dtype(series):
                    number = float(value)

                    if operation == "Equals":
                        mask = series == number
                    elif operation == "Not equals":
                        mask = series != number
                    elif operation == "Greater than":
                        mask = series > number
                    elif operation == "Greater than or equal":
                        mask = series >= number
                    elif operation == "Less than":
                        mask = series < number
                    else:
                        mask = series <= number

                else:
                    text = value.strip().lower()
                    text_series = series.fillna("").astype(str).str.lower()

                    if operation == "Contains":
                        mask = text_series.str.contains(text, regex=False)
                    elif operation == "Starts with":
                        mask = text_series.str.startswith(text)
                    elif operation == "Ends with":
                        mask = text_series.str.endswith(text)
                    elif operation == "Equals":
                        mask = text_series == text
                    else:
                        mask = text_series != text

                if not_condition:
                    mask = ~mask

                if final_mask is None:
                    final_mask = mask
                elif connector == "AND":
                    final_mask = final_mask & mask
                else:
                    final_mask = final_mask | mask

            except ValueError:
                st.error(f"Condition {i + 1}: enter a valid value.")
                valid = False
                break

        if valid and final_mask is not None:
            composite_result = df[final_mask]
            st.session_state["composite_result"] = composite_result

    if "composite_result" in st.session_state:
        result = st.session_state["composite_result"]
        st.success(f"{len(result):,} matching rows found.")
        st.dataframe(result, use_container_width=True, height=450)

except Exception as error:
    st.error(str(error))

