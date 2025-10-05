''' IPL Analytics Dashboard '''
import streamlit as st
import pandas as pd
from src.series_analysis import no_of_wins, pair_analysis, venue_run, tosschoice_bb
from src.team_performance import (
    sunburst, match_count, overseas_players, performance, toss_performance, toss_choice
    )

st.set_page_config(
    page_title = 'IPL Dashboard',
    layout = 'wide',
    initial_sidebar_state = 'collapsed'
)

st.title("IPL Analytics")

tab1, tab2, tab3 = st.tabs(['Series Analysis', 'Team Performance Analysis', 'Match Analysis'])

with tab1: #Series Analysis
    match_list = pd.read_csv('data/match_list-9jun25.csv')
    match_info = pd.read_csv('data/match_info-10jun25.csv')

    col = st.columns([0.7, 0.3], gap='medium')

    with col[0]:
        st.plotly_chart(venue_run, use_container_width=True)
        # with col2[1]:
        #     st.plotly_chart(tosschoice_venue, use_container_width=True)

        st.dataframe(pair_analysis)

    with col[1]:
        with st.container().markdown("**Right Container 1**"):
            st.plotly_chart(no_of_wins, use_container_width=True)

        with st.container().markdown("**Right Container 2**"):
            st.plotly_chart(tosschoice_bb, use_container_width=True)

with tab2: #Team Performance
    match_list = pd.read_csv('data/match_list-9jun25.csv')
    match_info = pd.read_csv('data/match_info-10jun25.csv')

    team_names = match_info.Team1.str.replace(' ', '_').unique().tolist()

    team_name = st.selectbox(
        'Select a Team: ',
        team_names
    )

    col = st.columns(3, gap='small')

    with col[0]:
        with st.container():
            st.plotly_chart(performance(team_name), use_container_width=True)
            st.plotly_chart(toss_performance(team_name), use_container_width=True)

    with col[1]:
        with st.container():
            st.plotly_chart(sunburst(team_name), use_container_width=True)
            st.write('Overseas Player:')
            st.dataframe(overseas_players(team_name))

    with col[2]:
        with st.container():
            st.plotly_chart(match_count(team_name), use_container_width=True)
            st.plotly_chart(toss_choice(team_name), use_container_width=True)

with tab3: #Match Analysis
    match_list = pd.read_csv('data/match_list-9jun25.csv')

    selection = st.selectbox(
        'Select a Match',
        (match_list.MatchDate + ', ' + match_list.MatchName).to_list()
    )

    match_id = match_list.MatchID.loc[match_list.MatchName == selection.split(', ')[1]]
