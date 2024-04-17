import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time

# Select wide mode
st.set_page_config(layout="wide")

dai_dose = st.slider("Daily dose", min_value=1, step=1, key="pk1")
dose_per_day = st.slider("Dose per day", min_value=1, step=1, key="pk2")
day = st.slider("Days", min_value=1, step=1, key="pk3")
on = st.toggle("TK stats", help="It provides information about AUC, Peak, Mean")

def display_current_graph(on):
    graph1 = st.session_state.df_graph1[st.session_state.count]
    graph2 = st.session_state.df_graph2[st.session_state.count]
    stats = st.session_state.tkstats[st.session_state.count]

    # # Commenting this because I dont have this theme, feel free to uncomment 
    # plt.style.use('seaborn-darkgrid')
    plt.style.use("ggplot")
    # Crear dos columnas para colocar las gráficas
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        plt.figure(figsize=(8, 6))
        plt.plot(graph1["time"], graph1["Cplasma"], color="black")
        plt.xlabel("Time, days")
        plt.ylabel("Cplasma, uM")
        plt.title(
            f"Plasma concentration vs. time for dose 1 mg/kg {st.session_state.names[st.session_state.count]}"
        )
        st.pyplot(plt)

    with fig_col2:
        plt.figure(figsize=(8, 6))
        plt.scatter(graph2["dose"], graph2["Css"], color="black")
        plt.plot(
            graph2[graph2["dose"] == 1]["dose"],
            graph2[graph2["dose"] == 1]["Css"],
            linestyle="--",
        )  # Línea punteada
        plt.plot(
            graph2["dose"], graph2["Css"], linestyle="--", color="black"
        )  # Línea sólida
        plt.xlabel("Dose")
        plt.ylabel("Css")
        plt.title(
            f"CSS vs. daily dose of {st.session_state.names[st.session_state.count]}"
        )
        st.pyplot(plt)

    if on:
        st.markdown(
            '## <span style="color:black">TK Parameters</span>', unsafe_allow_html=True
        )
        parameters = ["AUC", "Peak", "Mean"]
        values = stats
        for parameter, value in zip(parameters, values):
            st.markdown(f"- **{parameter}:** {value}", unsafe_allow_html=True)


def next_quote():
    N = max(len(st.session_state.df_graph1), len(st.session_state.df_graph2))
    # Roll over if the next counter is going to be out of bounds
    if st.session_state.count + 1 == N:
        st.session_state.count = 0
    else:
        st.session_state.count += 1


def previous_quote():
    N = max(len(st.session_state.df_graph1), len(st.session_state.df_graph2)) - 1
    # Roll back if the previous counter is going to be out of bounds
    if st.session_state.count == 0:
        st.session_state.count = N
    else:
        st.session_state.count -= 1


if "Run PK Analysis" not in st.session_state:
    st.session_state["Run PK Analysis"] = False

if "PK interpretation" not in st.session_state:
    st.session_state["PK interpretation"] = False

if st.button("Run PK Analysis", key="pk_button"):
    st.session_state["Run PK Analysis"] = not st.session_state["Run PK Analysis"]
    with st.spinner("Building graphs..."):

        time.sleep(2)

        if "count" not in st.session_state:
            st.session_state.count = 0

        # Almacenar df_graph1 en el estado de la sesión
        if "df_graph1" not in st.session_state:
            st.session_state.df_graph1 = [
                pd.read_csv("data.csv"),
                pd.read_csv("data2.csv"),
                pd.read_csv("data3.csv"),
            ]

        # Almacenar df_graph2 en el estado de la sesión
        if "df_graph2" not in st.session_state:
            st.session_state.df_graph2 = [
                pd.read_csv("data4.csv"),
                pd.read_csv("data5.csv"),
                pd.read_csv("data6.csv"),
            ]

        if "tkstats" not in st.session_state:
            st.session_state.tkstats = [
                [0.1, 0.2, 0.3],
                [0.2, 0.5, 0.9],
                [0.1, 0.2, 0.4],
            ]

        # Almacenar los nombres de los gráficos en el estado de la sesión
        if "names" not in st.session_state:
            st.session_state.names = ["chemical1", "chemical2", "chemical3"]

        # Mostrar la gráfica actual según el contador

    if st.session_state["Run PK Analysis"]:
        with st.expander("PK interpretation"):
            st.write("blabla")

# Create a set of items which must be there in the session state before the graphs can be displayed
required_states = {"df_graph1", "df_graph2"}

# Only display the graph and navigation buttons once the analysis is done at least once and the fields df_graph1, df_graph2 are populated in the session state
if required_states - set(st.session_state.keys()) == set():    
    # Display the navigation buttons
    prev_btn, _, next_btn = st.columns([1, 12, 1])

    if prev_btn.button("⏮️ Previous"):
        previous_quote()

    if next_btn.button("Next ⏭️"):
        next_quote()
    
    # Display the current graph
    display_current_graph(on)
