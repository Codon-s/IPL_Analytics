''' IPL Series Analysis '''
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
import pandas as pd

# Initializing colors
shared_color = pc.sequential.Mint

# Reading data
df=pd.read_csv('../iplanalytics/data/match_info-10jun25.csv')
kf=pd.read_csv('../iplanalytics/data/match_list-9jun25.csv')
kf.rename(columns={'MatchID':'id'}, inplace=True)
ds=pd.merge(df,kf, on='id')

# Number of Wins by Each Team
match_counts = ds['matchWinner'].value_counts().reset_index()
match_counts.columns = ['Match Winner', 'Match Count']

no_of_wins = px.bar(
    match_counts,
    x='Match Count',
    y='Match Winner',
    orientation='h',
    labels={'Match Winner': 'Match Winner', 'Match Count': 'Match Count'},
    color='Match Winner',
    title="Number of Wins by Each Team",
    color_discrete_sequence=shared_color
)

no_of_wins.update_layout(showlegend=False)

# match count venue(line)and max runs at match venue
match_venue=ds.groupby('MatchVenue')[['r1','r2']].max().max(axis=1).reset_index()
venue_count = ds['MatchVenue'].value_counts()
venue_count = venue_count.reset_index()
bar_line = pd.merge(match_venue, venue_count, on='MatchVenue')
bar_line['MatchVenue'] = bar_line['MatchVenue'].str.split(',', n=1).str[1]

venue_run = go.Figure()

venue_run.add_trace(go.Bar(
    x = bar_line.MatchVenue,
    y = bar_line['count'],
    yaxis = 'y',
    marker=dict(color=shared_color[:len(bar_line)]),
    name='Match Count'
))

venue_run.add_trace(go.Scatter(
    x = bar_line.MatchVenue,
    y = bar_line[0],
    yaxis = 'y2',
    mode='lines',
    marker=dict(color=shared_color[:len(bar_line)]),
    name='Average Runs'
))

venue_run.update_layout(
    xaxis = dict(title = 'Match Venue'),
    yaxis =dict(title= 'Match Count', side = 'left'),
    yaxis2 = dict(title='Max Runs', overlaying = 'y', side = 'right'),
    legend = dict(x = 0.1, y = 1.1, orientation = 'h'),
    title = 'Match Count and Average Runs at Match Venue',
    width=200
)


# Pair analysis

pair_analysis = pd.DataFrame(columns=[
    'Team',
    'Matches_Played',
    'Matches_Won',
    'Dominating'
])

teams = df['Team1'].unique().tolist()

for i in teams:
    matches_played = df.loc[(df['Team1'] == i) | (df['Team2'] == i)].shape[0]
    a = df.loc[(df['matchWinner'] == i)]
    matches_won = a.shape[0]
    t1 = a['Team1'].unique().tolist()
    t2 = a['Team2'].unique().tolist()
    domination = list(set(t1) & set(t2))
    domination.remove(i)
    pair_analysis.loc[pair_analysis.shape[0]] = [i, matches_played, matches_won, domination]

#toss choice by match venue (bat & bowl)
ct=pd.crosstab(index=ds.MatchVenue,columns=ds.tossChoice).reset_index()
long_df = ct.melt(id_vars='MatchVenue', var_name='Toss Choice', value_name='Count')
long_df['MatchVenue'] = long_df['MatchVenue'].str.split(',', n=1).str[1]

tosschoice_bb = px.sunburst(
    long_df,
    path=['Toss Choice', 'MatchVenue'],
    values='Count',
    color='Toss Choice',
    title='Toss Choices by Match Venue',
    color_discrete_sequence=shared_color
)

 #toss choice by each team(team1)vertical bar graph
team1 = pd.crosstab(index=ds.tossChoice, columns=ds.Team1)
teams = team1.columns.tolist()
color_map = {team: shared_color[i % len(shared_color)] for i, team in enumerate(teams)}
tosschoice_venue = go.Figure()

for team in team1.columns:
    tosschoice_venue.add_trace(go.Bar(
        x=team1.index,        # Toss choices: bat, field
        y=team1[team],        # Count values
        name=team,
        marker_color=color_map[team]
    ))

tosschoice_venue.update_layout(
    barmode='stack',
    title='Toss Choices by Each Team (Team1)',
    xaxis_title='Toss Choice',
    yaxis_title='Count',
    legend_title='Team1'
)
