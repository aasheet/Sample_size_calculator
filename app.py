import numpy as np
import pandas as pd
from scipy import stats
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('A/B Testing Sample Size Calculator',
                        className = 'text-center mb4 bg-secondary'))
    ]),
    dbc.Row([
        dbc.Col(html.Br())
    ]),
    dbc.Row([
        dbc.Col(html.H3('INPUTS:',className = 'text-center mb4'))
    ]),
    dbc.Row([
        dbc.Col(html.Br())
    ]),
    dbc.Row([
        dbc.Col(html.H4('Baseline Conversion Rate',
                        className = 'text-center mb4')),
        dbc.Col(html.H4('Minimum Detectable Effect',
                        className = 'text-center mb4'))
    ]),
    dbc.Row([
        dbc.Col(dcc.Input(id='baseline_conversion_rate', value=15
                          ),style={'textAlign': 'center'}),
        dbc.Col(dcc.Input(id='minimum_detectable_effect',value=10
                          ),style={'textAlign': 'center'})
    ]),
    dbc.Row([
        dbc.Col(html.Br())
    ]),
    dbc.Row([
        dbc.Col(html.H4('Statiscical significance',className = 'text-center mb4'))
    ]),
    dbc.Row([
        dbc.Col(dcc.Slider(80, 99, 1,value=95,id='statiscical_significance',),style={'textAlign': 'center'})
    ]),
    dbc.Row([
        dbc.Col(html.H4('Power',className = 'text-center mb4'))
    ]),
    dbc.Row([
        dbc.Col(dcc.Slider(70, 90, 1,value=80,id='power'),style={'textAlign': 'center'})
    ]),
    dbc.Row([
        dbc.Col(html.H4('Number of Variants (Not including Control)',className = 'text-center mb4'))
    ]),
    dbc.Row([
        dbc.Col(dcc.Slider(1, 5, 1,value=1,id='vars'),style={'textAlign': 'center'})
    ]),
    dbc.Row([
        dbc.Col(html.Hr())
    ]),
    dbc.Row([
        dbc.Col(html.H3('OUTPUTS :',className = 'text-center mb4'))
    ]),
    dbc.Row([
        dbc.Col(html.H4('Estimated Conversion rate of variant:',
                        className = 'text-center mb4')),
        dbc.Col(html.H4('Effective Statistical Significance of test:',
                        className = 'text-center mb4'))
    ]),
    dbc.Row([
        dbc.Col(html.H4(id = 'estimated_conv',
                        className = 'text-center mb4 bg-light text-dark')),
        dbc.Col(html.H4(id = 'stat_sig_new',
                        className = 'text-center mb4 bg-light text-dark'))
    ]),
    dbc.Row([
        dbc.Col(html.Br())
    ]),
    dbc.Row([
        dbc.Col(html.H4('Total Sample Size Needed:',
                        className = 'text-center mb4')),
        dbc.Col(html.H4('Sample Size Per Variant:',
                        className = 'text-center mb4'))
    ]),
    dbc.Row([
        dbc.Col(html.H4(id = 'n_total',
                        className = 'text-center mb4 bg-light text-dark')),
        dbc.Col(html.H4(id = 'n_var1',
                        className = 'text-center mb4 bg-light text-dark'))
    ])
])

@app.callback(
    [dash.dependencies.Output('estimated_conv', 'children'),
     dash.dependencies.Output('stat_sig_new', 'children'),
     dash.dependencies.Output('n_total', 'children'),
     dash.dependencies.Output('n_var1', 'children'),
    ],
    [dash.dependencies.Input('baseline_conversion_rate', 'value'),
     dash.dependencies.Input('minimum_detectable_effect', 'value'),
     dash.dependencies.Input('statiscical_significance', 'value'),
     dash.dependencies.Input('power', 'value'),
     dash.dependencies.Input('vars', 'value')
    ])

def calc(baseline_conversion_rate,minimum_detectable_effect,statiscical_significance,power,vars):
    var_conv_rate = float(baseline_conversion_rate)*(1+(float(minimum_detectable_effect)/100))
    alpha_new = (1-(float(statiscical_significance)/100))/float(vars)
    ss2 = 100 - alpha_new*100
    r = float(vars)/1
    r2 = (r+1)/r
    za = abs(stats.norm.ppf(alpha_new/2))
    zb = abs(stats.norm.ppf(1-(float(power)/100)))
    p1 = float(baseline_conversion_rate)/100
    p2 = float(var_conv_rate)/100
    pavg = ((p1+p2)/2)
    p_diff_sq = np.power(p1-p2,2)
    n_2 = int(((r2)*(pavg)*(1-pavg)*(np.power(zb+za,2)))/(p_diff_sq))
    n = int(n_2*(float(vars)+1))
    return var_conv_rate, ss2,n,n_2



if __name__=='__main__':
    app.run_server(debug=True)