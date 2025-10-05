''' IPL Match Analysis '''
import plotly.graph_objects as go
import plotly.colors as pc

color = pc.sequential.Mint

def dismissals(data, theme=None):
    ''' Distribution of Dismissal Types '''
    if theme is None:
        theme = color

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels = data.index,
            values = data.values,
            name='Dismissal',
            hole=0.4,
            marker=dict(colors=theme[:len(data)])
        )
    )

    fig.update_layout(
        title = 'Dismissals',
        xaxis_title = 'Dismissal Type',
        yaxis_title = 'Count',
        legend_title = 'Dismissal Type',
        plot_bgcolor = 'rgba(0,0,0,0)',
        legend = dict(
            x = 0.5,
            y = -0.2,
            orientation = 'h',
            xanchor = 'center'
        )
    )

    return fig

def boundaries(data, theme=None):
    ''' Distribution of Boundaries Scored '''
    if theme is None:
        theme = color

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels = data[['4s', '6s']].columns,
            values = [data['4s'].sum(), data['6s'].sum()],
            name='Boundary',
            hole=0.4,
            marker=dict(colors=theme[:len(data)]),
        )
    )

    fig.update_layout(
        title = 'Boundaries',
        xaxis_title = 'Boundary Type',
        yaxis_title = 'Count',
        legend_title = 'Boundary Type',
        plot_bgcolor = 'rgba(0,0,0,0)',
        legend = dict(
            x = 0.5,
            y = -0.2,
            orientation = 'h',
            xanchor = 'center'
        )
    )

    return fig

def batsman_perf(data, theme=None):
    ''' Batsman Performance: Runs and Strike Rate '''
    if theme is None:
        theme = color

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = data['batsman'],
            y = data['r'],
            name = 'Runs',
            yaxis = 'y', # left y-axis
            marker_color = theme[:data.shape[0]]
        )
    )

    fig.add_trace(
        go.Scatter(
            x = data['batsman'],
            y = data['sr'],
            name = 'Strike Rate',
            mode = 'lines',
            yaxis = 'y2', # right y-axis
            marker_color = 'blue'
        )
    )

    fig.update_layout(
        title_text = 'Batsman Performance (Runs and Strike Rate)',
        xaxis = dict(
            title = 'Batsman'
        ),
        yaxis=dict(
            title = 'Runs'
        ),
        yaxis2=dict(
            title='Strike Rate',
            overlaying='y',
            side='right',
            rangemode = 'tozero'
        ),
        legend = dict(
            x = 0.5,
            y = 1.1,
            orientation = 'h',
            xanchor = 'center'
        ),
        plot_bgcolor = 'rgba(0,0,0,0)'
    )

    return fig

def bowler_perf(data, theme=None):
    ''' Bowler Performance: Runs Conceded including Extras and Economy Rate '''
    if theme is None:
        theme = color

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = data['bowler'],
            y = data['r'],
            name = 'Runs Conceded',
            yaxis = 'y', # left y-axis
            marker_color = theme[:data.shape[0]]
        )
    )

    fig.add_trace(
        go.Bar(
            x = data['bowler'],
            y = data['extras'],
            name = 'extras',
            yaxis = 'y', # left y-axis
            marker_color = 'red'
        )
    )

    fig.add_trace(
        go.Scatter(
            x = data['bowler'],
            y = data['eco'],
            name = 'Economy Rate',
            mode = 'lines',
            yaxis = 'y2', # right y-axis
            marker_color = 'blue'
        )
    )

    fig.update_layout(
        barmode = 'group',
        title = 'Bowler Performance (Runs Conceded including Extras)',
        xaxis_title = 'Bowler',
        plot_bgcolor = 'rgba(0,0,0,0)',
        xaxis = dict(
            title = 'Bowler'
        ),
        yaxis_title = 'Runs',
        yaxis = dict(
            title = 'Runs Conceded'
        ),
        yaxis2 = dict(
            title = 'Economy Rate',
            overlaying = 'y',
            side = 'right',
            rangemode = 'tozero'
        ),
        legend_title = 'Runs Conceded and Economy Rate',
        legend = dict(
            x = 0.5,
            y = 1.1,
            orientation = 'h',
            xanchor = 'center'
        )
    )

    return fig

def fielder_perf(data, theme=None):
    ''' Fielder Performance: Catches by Catcher vs Batsman '''
    if theme is None:
        theme = color

    catch_df = data.groupby(['catcher', 'batsman']).size().reset_index(name='catches')

    pivot_df = catch_df.pivot(index='catcher', columns='batsman', values='catches').fillna(0)

    fig = go.Figure()

    for batsman in pivot_df.columns:
        fig.add_trace(
            go.Bar(
                x = pivot_df.index,
                y = pivot_df[batsman],
                name = batsman,
                marker_color = theme[:len(pivot_df)],
                hovertemplate = f'Batsman: {batsman}<extra></extra>'
            )
        )

    fig.update_layout(
        title = 'Catches by Fielder (catcher) vs Batsman',
        xaxis_title = 'Catcher',
        yaxis_title = 'Number of Catches',
        barmode = 'stack',
        legend_title = 'Batsman',
        legend = dict(
            x = 0.5,
            y = 1.1,
            orientation = 'h',
            xanchor = 'center'
        ),
        showlegend = False,
        plot_bgcolor = 'rgba(0,0,0,0)'
    )

    return fig
