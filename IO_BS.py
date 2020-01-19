
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
from datetime import datetime as dt
import IO_BS_core_engine
from dash.exceptions import PreventUpdate


params={}

VALID_USERNAME_PASSWORD_PAIRS = [
    ['hello', 'world']
]

app = dash.Dash('auth')
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
markdown_text = '''
### European Option Pricer
Security list
'''

sec_list=IO_BS_core_engine.get_BS_inputs().get_security_list()
sec_list_dict=[]
for ISIN in sec_list:
    sec_list_dict.append({'label':ISIN,'value':ISIN})

app.layout = html.Div([
        
    
    dcc.Markdown(children=markdown_text),
    
    dcc.Dropdown(      
        options=sec_list_dict,
        multi=False,
        id='SecList'
    ),
    
    dcc.Markdown(children='Currency of valuation'),
    
    dcc.RadioItems(
        options=[
            {'label': 'USD', 'value': 'USD'},
            {'label': 'PLN', 'value': 'PLN'}
        ],
        value='USD',
        id='CCY'
    ),
    
    html.Label('European Call/Put'),
    dcc.RadioItems(
        options=[
            {'label': 'Call Option', 'value': 'Call'},
            {'label': 'Put Option', 'value': 'Put'}
        ],
        value='Call',
        id='opt_type'
    ),
    
    dcc.Markdown(children='Option Maturity'),
    
    dcc.Slider(
        id='my-slider',
        min=0,
        max=12,
        step=3,
        value=0,
        marks={
        0: '7D',
        3: '3M',
        6: '6M',
        9: '9M',
i        12:'12M'
    },
    ),
    html.Div(id='slider-output-container'),
    
    dcc.Markdown(children='Date of valuation'),
    
    dcc.DatePickerSingle(
    id='date-picker-single',
    date=dt(2020,1, 11)
    ),
    
    dcc.Markdown(children=' '),
    
    html.Button('Get parameters', id='GetParameters'),
    
    dcc.Markdown(children='Current price'),
    
    dcc.Input(
    placeholder='Current price',
    type='number',
    value='',
    id='current-price'
    ),
            
    dcc.Markdown(children='Volatility'),
            
    dcc.Input(
    placeholder='Volatility',
    type='number',
    value='',
    id='vol'
    ),
            
    dcc.Markdown(children='Interest Rate'),
            
    dcc.Input(
    placeholder='Interest Rate',
    type='number',
    value='',
    id='Interest Rate'
    ),
            
    dcc.Markdown(children='Strike Price'),
            
    dcc.Input(
    placeholder='Strike',
    type='number',
    value='',
    id='Strike'
    ),
            
    dcc.RadioItems(
        options=[
            {'label': 'Option Price', 'value': 'Price'},
            {'label': 'Implied Volatility', 'value': 'ImlVol'}
        ],
        value='Price'
    ),
    
    html.Button('Calculate', id='Calculate'),
    
    dcc.Input(
    placeholder='Result',
    type='text',
    value='',
    id='Results'
    ),
            
    html.Div(id='hidden-div1', style={'display':'none'}),
    html.Div(id='hidden-div2', style={'display':'none'}),
    html.Div(id='hidden-div3', style={'display':'none'}),
    html.Div(id='hidden-div4', style={'display':'none'})
    
])
  
    
@app.callback(
    dash.dependencies.Output('current-price', 'value'),
    [dash.dependencies.Input('GetParameters', 'n_clicks'),
     dash.dependencies.Input('CCY', 'value')])
def update_cp(n_clicks,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        opt_instance=IO_BS_core_engine.get_BS_inputs("WW123456789",CCY=value)
        return str(opt_instance.get_current_price())
    
@app.callback(
    dash.dependencies.Output('Interest Rate', 'value'),
    [dash.dependencies.Input('GetParameters', 'n_clicks'),
     dash.dependencies.Input('CCY', 'value')])
def update_ir(n_clicks,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        opt_instance=IO_BS_core_engine.get_BS_inputs("WW123456789",CCY=value)
        return str(opt_instance.get_interestrate())

@app.callback(
    dash.dependencies.Output('vol', 'value'),
    [dash.dependencies.Input('GetParameters', 'n_clicks'),
     dash.dependencies.Input('CCY', 'value')])
def update_vol(n_clicks,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        opt_instance=IO_BS_core_engine.get_BS_inputs("WW123456789",CCY=value)
        return str(opt_instance.get_volatility())
    
@app.callback(
    dash.dependencies.Output('hidden-div1', 'children'),
    [dash.dependencies.Input('Calculate', 'n_clicks'),dash.dependencies.Input('vol', 'value')])
def update_results_vol(n_clicks,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        params['v']=value
        return params['v']
    
@app.callback(
    dash.dependencies.Output('hidden-div2', 'children'),
    [dash.dependencies.Input('Calculate', 'n_clicks'),dash.dependencies.Input('Interest Rate', 'value')])
def update_results_ir(n_clicks,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        params['r']=value
        return "" 
    
@app.callback(
    dash.dependencies.Output('hidden-div3', 'children'),
    [dash.dependencies.Input('Calculate', 'n_clicks'),dash.dependencies.Input('Strike', 'value')])
def update_results_strike(n_clicks,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        params['K']=value
        return ""
    
@app.callback(
    dash.dependencies.Output('hidden-div4', 'children'),
    [dash.dependencies.Input('Calculate', 'n_clicks'),dash.dependencies.Input('current-price', 'value')])
def update_results_cp(n_clicks,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        params['S']=value
        return ""    
    
@app.callback(
    dash.dependencies.Output('Results', 'value'),
    [dash.dependencies.Input('Calculate', 'n_clicks'),dash.dependencies.Input('opt_type', 'value')])
def update_results(n_clicks,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        pricing_instance=IO_BS_core_engine.price_European_Option(float(params['S']),float(params['K']),7/252,float(params['r']),float(params['v'])/100.)
        if str(value)=='Call':
            return str(pricing_instance.call)
        else:
            return pricing_instance.put
        
@app.callback(
    dash.dependencies.Output('SecList', 'value'),
    [dash.dependencies.Input('SecList', 'n_clicks')])
def update_seclist(n_clicks,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return value

if __name__ == '__main__':
    app.run_server()


