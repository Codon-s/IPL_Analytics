''' IPL Team Performance Analysis '''
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
import pandas as pd
import numpy as np

# Initilization
shared_color=pc.sequential.Mint

# Data Ingestion
df1 = pd.read_csv("./data/match_info-10jun25.csv")
df2 = pd.read_csv("./data/match_list-9jun25.csv")
df = pd.merge(df1, df2, left_on='id', right_on='MatchID', how='inner')
df['Cities'] = df.MatchVenue.str.split(',', n=1, expand=True)[1]

def fetch_team(name):
    ''' Fetching team data for files '''
    team = pd.read_csv(f'./data/squad/{name}.csv')
    team['style'] = np.select(
        [
            team.role.str.lower() == 'bowler',
            team.role.str.lower() == 'batsman',
            team.role.str.lower() == 'batting allrounder',
            team.role.str.lower() == 'bowling allrounder',
            team.role.str.lower() == 'wk-batsman'
        ],

        [
            team.bowlingStyle,
            team.battingStyle,
            team.battingStyle,
            team.bowlingStyle,
            team.battingStyle
        ],

        default=np.nan
    )
    return team

# Visulizations
def sunburst(team_name):
    ''' Sunburst Chart for Team Players Distribution '''
    data = fetch_team(team_name)
    fig = px.sunburst(
        data,
        path = ['role', 'style', 'name'],
        color_discrete_sequence=shared_color
    )

    fig.update_layout(
        title=dict(
        text='Players Distribution',
        x=0.5,
        xanchor='center'
        )
    )

    return fig

def match_count(team_name, dataframe=df):
    ''' Match Count and Average Runs by City '''
    # Venue average score (line)
    team_name = team_name.replace('_', ' ')
    data = dataframe.loc[(dataframe.Team1==team_name) | (dataframe.Team2==team_name)]
    data['Cities'] = data.MatchVenue.str.split(',', n=1, expand=True)[1]

    venue_score = data.groupby('Cities')[['r1','r2']].mean().max(axis=1).reset_index()
    venue_score = venue_score.rename(columns={0: 'Avg_Runs'})

    # Match count per city (bar)
    count = data.groupby('Cities')[['MatchName']].count().reset_index()
    count = count.rename(columns={'MatchName': 'Match_Count'})

    # Merge both on 'Cities'
    combined = pd.merge(count, venue_score, on='Cities')

    fig = go.Figure()

    # Bar Chart for Match Count
    fig.add_trace(go.Bar(
        x=combined['Cities'],
        y=combined['Match_Count'],
        name='Match Count',
        yaxis='y',
        marker=dict(color=shared_color[:len(combined)])
    ))

    # Line Chart for Average Runs
    fig.add_trace(go.Scatter(
        x=combined['Cities'],
        y=combined['Avg_Runs'],
        name='Average Runs',
        mode='lines',
        yaxis='y2',
        marker=dict(color=shared_color[:len(combined)])
    ))

    # Layout with Dual Axes
    fig.update_layout(
        title='Match Count and Average Runs by City',
        title_x=0.4,
        xaxis=dict(title='City'),
        yaxis=dict(title='Match Count', side='left'),
        yaxis2=dict(title='Average Runs', overlaying='y', side='right'),
        legend=dict(x=0.1, y=1.1, orientation='h'),
    )

    return fig

def overseas_players(team_name):
    ''' Overseas Players Dataframe '''
    data = fetch_team(team_name)
    players = data[data['country'] != 'India'][['name', 'country', 'role']]
    players.reset_index(drop=True, inplace=True)
    players.attrs["title"] = f"Overseas Players of {team_name}"
    return players

def performance (team_name,dataframe=df):
    ''' Matches Played vs Won by City '''
    team_name = team_name.replace('_', ' ')
    data = dataframe.loc[(dataframe.Team1==team_name) | (dataframe.Team2==team_name)]
    data['Cities'] = data.MatchVenue.str.split(',', n=1, expand=True)[1]

    matches_won=data.loc[(data.matchWinner==team_name)]

    won=matches_won.groupby('Cities')[['MatchName']].count().reset_index()
    y=data.groupby('Cities')[['MatchName']].count().reset_index()
    combined1 = pd.merge(won, y, on='Cities', how='outer')
    combined1 = combined1.rename(columns={'MatchName_x': 'Won','MatchName_y': 'Played'})

    # Replace NaN with 0 for plotting
    combined1['Won'] = combined1['Won'].fillna(0)

    # Create the plot
    fig = go.Figure()

    # Line for Matches Played
    fig.add_trace(go.Scatter(
        x=combined1['Cities'],
        y=combined1['Played'],
        mode='lines+markers',
        name='Matches Played',
        line=dict(color=shared_color[0], dash='dash'),
        marker=dict(color='blue')
    ))

    # Line for Matches Won
    fig.add_trace(go.Scatter(
        x=combined1['Cities'],
        y=combined1['Won'],
        mode='lines+markers',
        name='Matches Won',
        line=dict(color=shared_color[3], width=3),
        marker=dict(color='green')
    ))

    # Update layout
    fig.update_layout(
        title='Matches Played vs Won by City',
        title_x=0.3,
        yaxis_title='Count',
        legend=dict(
        x=0.20,
        y=0.80,
        xanchor='center',
        yanchor='top',
        orientation='h'
        )
    )

    return fig

def toss_performance(team_name, dataframe=df):
    ''' Toss Win Percentage '''
    team_name = team_name.replace('_', ' ')
    data = dataframe.loc[(dataframe.Team1==team_name) | (dataframe.Team2==team_name)]
    data['Cities'] = data.MatchVenue.str.split(',', n=1, expand=True)[1]

    tosses = data[(data['Team1'] == team_name) | (data['Team2'] == team_name)]

    # Tosses won by RCB
    toss_wins = tosses[tosses['tossWinner'] == team_name]

    # Percentage calculation
    total = len(tosses)
    wins = len(toss_wins)
    losses = total - wins

    # Pie Chart for Toss Win %
    fig = go.Figure(go.Pie(
        labels=['Toss Won', 'Toss Lost'],
        values=[wins, losses],
        hole=0.5,
        marker_colors=shared_color[:2]
    ))

    fig.update_layout(
        title="Toss Win Percentage",
        title_x=0.2,
        legend=dict(
        orientation='h',
        x=0.5,
        xanchor='center',
        y=1.1
    ))

    return fig

def toss_choice(team_name,dataframe=df):
    ''' Toss Choice Analysis (Bat vs Bowl) '''
    team_name = team_name.replace('_', ' ')
    data = dataframe.loc[(dataframe.Team1==team_name) | (dataframe.Team2==team_name)]
    data['Cities'] = data.MatchVenue.str.split(',', n=1, expand=True)[1]

    tosses = data[(data['Team1'] == team_name) | (data['Team2'] == team_name)]

    # Tosses won by RCB
    toss_wins = tosses[tosses['tossWinner'] == team_name]

    # Count toss choices
    choice_counts = toss_wins['tossChoice'].value_counts().reset_index()
    choice_counts.columns = ['Toss Choice', 'Count']

    fig = go.Figure(
        go.Bar(
            name='Team',
            x=choice_counts['Toss Choice'],
            y=choice_counts['Count'],
            marker=dict(color=shared_color[:len(choice_counts)])
        )
    )

    fig.update_layout(
        title='Toss Choices: Bat vs Bowl',
        title_x=0.3,
        xaxis_title='Toss Choice',
        yaxis_title='Count',
        barmode='group',
        template='plotly_white'
    )

    return fig
