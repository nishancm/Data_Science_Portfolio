import plotly
from plotly.graph_objs import Data, Layout, Marker, Scattermapbox


def plotly_map():
    mapbox_access_token = 'pk.eyJ1Ijoic3VodHdpbnMiLCJhIjoi' +\
                        'Y2pnNGJvbXRhMGpoNDJwcWRva3JieWgwcCJ9' +\
                        '.cmsuwG65XkGUh2pv07nIVg'

    data = Data([
        Scattermapbox(
            lat=['37.7765', '37.791377'],
            lon=['-122.4506', '-122.392609'],
            mode='markers',
            marker=Marker(size=15),
            text=["University of San Francisco, Main Campus",
                  "University of San Francisco, Downtown Campus"])])
    layout = Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=37.773972,
                lon=-122.431297
            ),
            pitch=0,
            zoom=11
        ),
    )

    fig = dict(data=data, layout=layout)
    output = plotly.offline.plot(fig, include_plotlyjs=False,
                                 output_type='div')
    return(output)
