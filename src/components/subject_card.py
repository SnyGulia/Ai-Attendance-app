import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    """Show a subject in a compact, consistently styled dashboard card."""
    with st.container(border=True):
        st.subheader(f":material/menu_book: {name}")
        st.caption(f"{code} | Section {section}")
        if stats:
            columns = st.columns(len(stats))
            for column, (icon, label, value) in zip(columns, stats):
                with column:
                    st.metric(label, value, help=label)
        if footer_callback:
            st.divider()
            footer_callback()
