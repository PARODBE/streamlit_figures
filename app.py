import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time

plt.style.use('ggplot')

# Select wide mode 
st.set_page_config(layout="wide")

def display_current_graph(on):
    quote = st.session_state.df_graph1[st.session_state.count]
    quote2 = st.session_state.df_graph2[st.session_state.count]
    quote3 = st.session_state.tkstats[st.session_state.count]


    plt.style.use('seaborn-darkgrid')
    # Crear dos columnas para colocar las gráficas
    col1, col2 = st.columns(2)

    with col1:
        plt.figure(figsize=(8, 6))
        plt.plot(quote['time'], quote['Cplasma'],color='black')
        plt.xlabel("Time, days")
        plt.ylabel("Cplasma, uM")
        plt.title(f"Plasma concentration vs. time for dose 1 mg/kg {st.session_state.names[st.session_state.count]}")
        st.pyplot(plt)
    
    with col2:
        plt.figure(figsize=(8, 6))
        plt.scatter(quote2['dose'], quote2['Css'],color='black')
        plt.plot(quote2[quote2['dose'] == 1]['dose'], quote2[quote2['dose'] == 1]['Css'], linestyle='--')  # Línea punteada
        plt.plot(quote2['dose'], quote2['Css'], linestyle='--', color='black')  # Línea sólida
        plt.xlabel("Dose")
        plt.ylabel("Css")
        plt.title(f"CSS vs. daily dose of {st.session_state.names[st.session_state.count]}")
        st.pyplot(plt)

    # with col1:
    #     p = ggplot(quote) + geom_line(aes(x='time', y='Cplasma')) + theme_bw() + xlab("Time, days") + ylab("Cplasma, uM") + ggtitle(f"Plasma concentration vs. time for dose 1 mg/kg {st.session_state.names[st.session_state.count]}")
    #     # Mostrar el gráfico
    #     st.pyplot(ggplot.draw(p))
    
    # with col2:

    #     c=ggplot(quote2) + geom_point(aes(x = 'dose', y = 'Css'))+ geom_abline(intercept = 0, slope = quote2[quote2.dose==1]['Css'],linetype='dashed') + ggtitle(f"CSS vs. daily dose of {st.session_state.names[st.session_state.count]}")

    #     st.pyplot(ggplot.draw(c))
    # Botones de navegación
    col1, _,_,_,_,col6,col7,col8,col9,col10,col11,col12= st.columns(12)

    with col1:
        if st.button("⏮️ Previous", on_click=previous_quote, args=(on,)):
            pass

    with col12:
        if st.button("Next ⏭️", on_click=next_quote, args=(on,)):
            pass

    if on:
        st.markdown('## <span style="color:black">TK Parameters</span>', unsafe_allow_html=True)
        parameters = ['AUC', 'Peak', 'Mean']
        values = quote3
        for parameter, value in zip(parameters, values):
            st.markdown(f"- **{parameter}:** {value}", unsafe_allow_html=True)

def next_quote(on):
    if st.session_state.count + 1 >= max(len(st.session_state.df_graph1), len(st.session_state.df_graph2)):
        st.session_state.count = 0
    else:
        st.session_state.count += 1
    display_current_graph(on)

def previous_quote(on):
    if st.session_state.count > 0:
        st.session_state.count -= 1
    else:
        st.session_state.count = max(len(st.session_state.df_graph1), len(st.session_state.df_graph2)) - 1
    display_current_graph(on)

dai_dose = st.slider('Daily dose', min_value=1, step=1, key="pk1")
dose_per_day = st.slider('Dose per day', min_value=1, step=1, key="pk2")
day = st.slider('Days', min_value=1, step=1, key="pk3")
on = st.toggle('TK stats' , help='It provides information about AUC, Peak, Mean')

if "Run PK Analysis" not in st.session_state:
    st.session_state["Run PK Analysis"] = False

if "PK interpretation" not in st.session_state:
    st.session_state["PK interpretation"] = False

if st.button("Run PK Analysis", key="pk_button"):
    st.session_state["Run PK Analysis"] = not st.session_state["Run PK Analysis"]
    with st.spinner("Building graphs..."):
        
        time.sleep(5)
        
        if 'count' not in st.session_state:
            st.session_state.count = 0

        # Almacenar df_graph1 en el estado de la sesión
        if 'df_graph1' not in st.session_state:
            st.session_state.df_graph1 = [pd.read_csv("data.csv"),pd.read_csv("data2.csv"),pd.read_csv("data3.csv")]

        # Almacenar df_graph2 en el estado de la sesión
        if 'df_graph2' not in st.session_state:
            st.session_state.df_graph2 = [pd.read_csv("data4.csv"),pd.read_csv("data5.csv"),pd.read_csv("data6.csv")]

        if 'tkstats' not in st.session_state:
            st.session_state.tkstats = [[0.1,0.2,0.3],[0.2,0.5,0.9],[0.1,0.2,0.4]]

        # Almacenar los nombres de los gráficos en el estado de la sesión
        if 'names' not in st.session_state:
            st.session_state.names = ["chemical1", "chemical2", "chemical3"]

        # Mostrar la gráfica actual según el contador
        display_current_graph(on)
    
    if st.session_state["Run PK Analysis"]:
        with st.expander("PK interpretation"):
            st.write('blabla')