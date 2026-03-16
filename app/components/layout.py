import streamlit as st


import streamlit as st


def two_column_divider(divider_height: int = 560):
    """
    Return two columns separated by a visible vertical divider.
    """
    col1, divider, col2 = st.columns([1, 0.05, 1])

    with divider:
        st.markdown(
            f"""
            <div style="
                width: 2px;
                height: {divider_height}px;
                background-color: #D9E2EC;
                margin: 0 auto;
            "></div>
            """,
            unsafe_allow_html=True,
        )

    return col1, col2
