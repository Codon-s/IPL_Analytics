''' IPL Analytics Dashboard '''
import json
import streamlit as st
import pandas as pd
from src.series_analysis import no_of_wins, pair_analysis, venue_run, tosschoice_bb
from src.team_performance import (
    sunburst, match_count, overseas_players, performance, toss_performance, toss_choice
    )
from src.match_analysis import (
    dismissals, boundaries, batsman_perf, bowler_perf, fielder_perf
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

    @st.cache_data
    def load_match_data(match):
        ''' Read data for Match Data Files '''
        with open(f'data/scorecard/{match}.json', 'r', encoding="utf-8") as f:
            data = json.load(f)

        return data

    # Data Ingestion
    inn1 = load_match_data(match_id.values[0])[0]
    inn2 = load_match_data(match_id.values[0])[1]
    inn1_name = inn1['inning'].replace(' Inning 1', '')
    inn2_name = inn2['inning'].replace(' Inning 1', '')

    # Data Preprocessing
    ## Match First Half
    batting = pd.DataFrame.from_records(inn1['batting'])
    batting.batsman = pd.json_normalize(batting.batsman)['name']
    batting.bowler = pd.json_normalize(batting.bowler)['name']
    batting.catcher = pd.json_normalize(batting.catcher)['name']

    bowling = pd.DataFrame.from_records(inn1['bowling'])
    bowling.bowler = pd.json_normalize(bowling.bowler)['name']
    bowling['extras'] = bowling['nb'] + bowling['wd']

    # KPIs
    total_runs = batting['r'].sum()
    total_balls = batting['b'].sum()
    team_strike = round((total_runs / total_balls) * 100, 2)
    total_dismissals = batting['dismissal'].notna().sum()

    col = st.columns(2, gap='small')
    # Dashoard
    with col[0]:
        with st.container(border=True):
            st.header(inn1_name, anchor=False)
            inner_col = st.columns(4, gap='small')
            with inner_col[0]:
                st.metric('Total Runs', total_runs, border=True)
            with inner_col[1]:
                st.metric('Total Balls Faced', total_balls, border=True)
            with inner_col[2]:
                st.metric('Team Strike Rate', team_strike, border=True)
            with inner_col[3]:
                st.metric('Total Dismissals', total_dismissals, border=True)

            inner_col2 = st.columns(2, gap='small')
            with inner_col2[0]:
                # Visualization: Dismissals
                dismissial_counts = batting['dismissal'].value_counts()
                st.plotly_chart(dismissals(dismissial_counts))
            with inner_col2[1]:
                # Visualization: Boundaries
                boundaries_count = batting.groupby('batsman')[['4s', '6s']].sum().reset_index()
                st.plotly_chart(boundaries(boundaries_count))

            # Visualization: Batsman Performance
            st.plotly_chart(batsman_perf(batting))

            # Visualization: Bowler Performance
            st.plotly_chart(bowler_perf(bowling))

            # Visualization: Fielder Performance
            st.plotly_chart(fielder_perf(batting))

    ## Match Second Half
    batting1 = pd.DataFrame.from_records(inn2['batting'])
    batting1.batsman = pd.json_normalize(batting1.batsman)['name']
    batting1.bowler = pd.json_normalize(batting1.bowler)['name']
    batting1.catcher = pd.json_normalize(batting1.catcher)['name']

    bowling1 = pd.DataFrame.from_records(inn2['bowling'])
    bowling1.bowler = pd.json_normalize(bowling1.bowler)['name']
    bowling1['extras'] = bowling1['nb'] + bowling1['wd']

    total_runs = batting1['r'].sum()
    total_balls = batting1['b'].sum()
    team_strike = round((total_runs / total_balls) * 100, 2)
    total_dismissals = batting1['dismissal'].notna().sum()

    # Dashoard
    with col[1]:
        with st.container(border=True):
            st.header(inn2_name, anchor=False)
            inner_col = st.columns(4, gap='small')
            with inner_col[0]:
                st.metric('Total Runs', total_runs, border=True)
            with inner_col[1]:
                st.metric('Total Balls Faced', total_balls, border=True)
            with inner_col[2]:
                st.metric('Team Strike Rate', team_strike, border=True)
            with inner_col[3]:
                st.metric('Total Dismissals', total_dismissals, border=True)

            inner_col2 = st.columns(2, gap='small')
            with inner_col2[0]:
                # Visualization: Dismissals
                dismissial_counts = batting1['dismissal'].value_counts()
                st.plotly_chart(dismissals(dismissial_counts))
            with inner_col2[1]:
                # Visualization: Boundaries
                boundaries_count = batting1.groupby('batsman')[['4s', '6s']].sum().reset_index()
                st.plotly_chart(boundaries(boundaries_count))

            # Visualization: Batsman Performance
            st.plotly_chart(batsman_perf(batting1))

            # Visualization: Bowler Performance
            st.plotly_chart(bowler_perf(bowling1))

            # Visualization: Fielder Performance
            st.plotly_chart(fielder_perf(batting1))
