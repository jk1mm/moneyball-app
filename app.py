import streamlit as sl

from moneyball.constants import MIN_YEAR, MAX_YEAR

sl.set_page_config(
    page_title="Moneyball",
    layout="wide",
    initial_sidebar_state="auto",
)


def display():

    # Sidebar configurations
    sl.sidebar.write("# Selections")
    season = sl.sidebar.selectbox(
        "Season:", list(reversed(range(MIN_YEAR, MAX_YEAR + 1)))
    )


if __name__ == "__main__":
    display()
