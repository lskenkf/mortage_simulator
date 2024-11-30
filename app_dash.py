import dash
from dash import dcc, html, Input, Output, dash_table, State
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import numpy as np
from datetime import datetime, timedelta
from dash_utilities import *
import io
import base64
import pandas as pd

# Initialize the Dash app first
app = dash.Dash(__name__)
server = app.server  # Now app is defined before we use it

# Translation dictionary with additional plot-related translations
translations = {
    'en': {
        'title': 'Mortgage Calculator',
        'purchase_price': 'Purchase Price',
        'equity': 'Equity',
        'broker_fee': 'Broker Fee Rate',
        'notary_fee': 'Notary Fee Rate',
        'real_estate_transfer_tax': 'Real Estate Transfer Tax',
        'land_registry': 'Land Registry Rate',
        'extra_payment': 'Extra Payment Rate',
        'repayment_rate': 'Repayment Rate',
        'interest_rate': 'Interest Rate',
        'fixed_interest': 'Fixed Interest Period',
        'calculate': 'Calculate',
        'language': 'Language',
        'monthly_payment': 'Monthly Payment',
        'total_interest': 'Total Interest',
        'loan_duration': 'Loan Duration (Years)',
        'remaining_debt': 'Remaining Debt (€)',
        'plot_title': 'Mortgage Amortization Schedule',
        'standard_payment': 'Standard Payment',
        'high_repayment': 'High Repayment',
        'remaining_loan': 'Remaining Loan',
        'cumulative_interest': 'Cumulative Interest',
        'paid_principal': 'Paid Principal',
        'monthly_interest': 'Monthly Interest',
        'monthly_principal': 'Monthly Principal',
        'with_extra_repayment': "With Extra Repayment",
        'without_extra_repayment': "Without Extra Repayment",
        'download_button': 'Download Amortization Schedule',
        'period': 'Period',
        'year': 'Year',
    },

    'de': {
        'title': 'Hypothekenrechner',
        'purchase_price': 'Kaufpreis',
        'equity': 'Eigenkapital',
        'broker_fee': 'Maklerprovision',
        'notary_fee': 'Notarkosten',
        'real_estate_transfer_tax': 'Grunderwerbsteuer',
        'land_registry': 'Grundbucheintrag',
        'extra_payment': 'Sondertilgung',
        'repayment_rate': 'Tilgungsrate',
        'interest_rate': 'Sollzins',
        'fixed_interest': 'Sollzinsbindung',
        'calculate': 'Berechnen',
        'language': 'Sprache',
        'monthly_payment': 'Monatliche Rate',
        'total_interest': 'Gesamtzinsen',
        'loan_duration': 'Kreditlaufzeit (Jahre)',
        'remaining_debt': 'Restschuld (€)',
        'plot_title': 'Tilgungsplan',
        'standard_payment': 'Standardzahlung',
        'high_repayment': 'Höhere Tilgung',
        'remaining_loan': 'Verbleibender Kredit',
        'cumulative_interest': 'Kumulierte Zinsen',
        'paid_principal': 'Gezahlte Tilgung',
        'monthly_interest': 'Monatliche Zinsen',
        'monthly_principal': 'Monatliche Tilgung',
        'with_extra_repayment': "Mit Sondertilgung",
        'without_extra_repayment': "Ohne Sondertilgung",
        'download_button': 'Tilgungsplan Herunterladen',
        'period': 'Zeitraum',
        'year': 'Jahr',
    },

    'zh': {
        'title': '房贷计算器',
        'purchase_price': '购房价格',
        'equity': '首付',
        'broker_fee': '中介费率',
        'notary_fee': '公证费率',
        'real_estate_transfer_tax': '不动产转让税',
        'land_registry': '土地登记费率',
        'extra_payment': '额外还款率',
        'repayment_rate': '还款率',
        'interest_rate': '利率',
        'fixed_interest': '固定利率期限',
        'calculate': '计算',
        'language': '语言',
        'monthly_payment': '月供',
        'total_interest': '总利息',
        'loan_duration': '贷款期限（年）',
        'remaining_debt': '剩务（€）',
        'plot_title': '还款计划表',
        'high_repayment': '高额还款',
        'remaining_loan': '剩余贷款',
        'cumulative_interest': '累计利息',
        'paid_principal': '已还本金',
        'monthly_interest': '每月利息',
        'monthly_principal': '每月本金',
        'with_extra_repayment': "有额外还款",
        'without_extra_repayment': "无额外还款",
        'download_button': '下载还款计划表',
        'period': '期间',
        'year': '年',
    }
}

# Layout remains the same as before until the callbacks
app.layout = html.Div([
    dcc.Store(id='translation-store', data='en'),
    dcc.Store(id='calculation-store', data={}),
    
    # Main container
    html.Div([
        # Centered title only
        html.Div([
            html.H1(id='title', className='app-title'),
        ], className='header-container'),
        
        # Language selector and main content
        html.Div([
            # Left column - Language selector and Inputs
            html.Div([
                html.Div([
                    # Add label above dropdown
                    html.Label(
                        id='language-label',
                        className='input-label'
                    ),
                    dcc.Dropdown(
                        id='language-selector',
                        options=[
                            {'label': 'English', 'value': 'en'},
                            {'label': 'Deutsch', 'value': 'de'},
                            {'label': '中文', 'value': 'zh'}
                        ],
                        value='en',  # Set default to English
                        className='language-dropdown'
                    )
                ], className='language-container'),
                
                # Input fields
                html.Div([
                    html.Div([
                        html.Label(id='purchase-price-label', className='input-label'),
                        dcc.Input(id='purchase-price', type='number', value=500000, className='input-field'),
                    ], className='input-container'),
                    
                    html.Div([
                        html.Label(id='equity-label', className='input-label'),
                        dcc.Input(id='equity', type='number', value=100000, className='input-field'),
                    ], className='input-container'),
                    
                    html.Div([
                        html.Label(id='broker-fee-label', className='input-label'),
                        dcc.Input(id='broker-fee', type='number', value=3.57, className='input-field'),
                    ], className='input-container'),
                    
                    html.Div([
                        html.Label(id='notary-fee-label', className='input-label'),
                        dcc.Input(id='notary-fee', type='number', value=2, className='input-field'),
                    ], className='input-container'),

                     html.Div([
                        html.Label(id='real-estate-transfer-tax-label', className='input-label'),
                        dcc.Input(id='real-estate-transfer-tax', type='number', value=0.5, className='input-field'),
                    ], className='input-container'),
                    
                    html.Div([
                        html.Label(id='land-registry-label', className='input-label'),
                        dcc.Input(id='land-registry', type='number', value=0.5, className='input-field'),
                    ], className='input-container'),
                    

                    html.Div([
                        html.Label(id='extra-payment-label', className='input-label'),
                        dcc.Input(id='extra-payment', type='number', value=5, className='input-field'),
                    ], className='input-container'),
                    
                    html.Div([
                        html.Label(id='repayment-rate-label', className='input-label'),
                        dcc.Input(id='repayment-rate', type='number', value=2, className='input-field'),
                    ], className='input-container'),
                    
                    html.Div([
                        html.Label(id='interest-rate-label', className='input-label'),
                        dcc.Input(id='interest-rate', type='number', value=3.5, className='input-field'),
                    ], className='input-container'),
                    
                    html.Div([
                        html.Label(id='fixed-interest-label', className='input-label'),
                        dcc.Input(id='fixed-interest', type='number', value=30, className='input-field'),
                    ], className='input-container'),
                    
                    html.Button(
                        id='calculate-button',
                        n_clicks=0,
                        className='calculate-button'
                    ),
                ], className='inputs-grid'),
            ], className='inputs-column'),
            
            # Right column - Plot and Table stacked vertically
            html.Div([
                # Plot container
                html.Div([
                    dcc.Graph(
                        id='mortgage-plot',
                        className='plot-container'
                    )
                ], className='plot-wrapper'),
                
                # Table container with download button
                html.Div([
                    # Download section
                    html.Div([
                        html.Button(
                            [
                                html.I(className="fas fa-download"),
                                html.Span(id='download-button-text')
                            ],
                            id="btn-download",
                            className='download-button'
                        ),
                        dcc.Download(id="download-dataframe-csv"),
                    ], className='download-section'),
                    
                    # Table
                    dash_table.DataTable(
                        id='mortgage-table',
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'center',
                            'padding': '10px',
                            'minWidth': '100px'
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        page_size=20
                    )
                ], className='table-wrapper')
            ], className='plot-column'),
            
        ], className='main-content'),
    ], className='app-container')
], className='root-container')

# Updated custom CSS with narrower input section
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <style>
            /* Root styles */
            :root {
                --primary-color: #007bff;
                --background-color: #f8f9fa;
                --border-color: #ddd;
                --text-color: #333;
            }

            /* Reset and base styles */
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: var(--text-color);
                background-color: #fff;
            }

            /* Container styles */
            .root-container {
                min-height: 100vh;
                width: 100%;
            }

            .app-container {
                max-width: 1600px;
                margin: 0 auto;
                padding: 20px;
            }

            /* Header styles */
            .header-container {
                width: 100%;
                background-color: #fff;
                padding: 20px 0;
                margin-bottom: 30px;
                text-align: center;
            }

            .app-title {
                font-size: 2.5rem;
                color: var(--primary-color);
                margin: 0;
            }

            /* Main content layout - three columns */
            .main-content {
                display: grid;
                grid-template-columns: 280px 1fr;
                gap: 30px;
                align-items: start;
            }

            .plot-column {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }

            .plot-wrapper {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 15px;
            }

            .table-wrapper {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 15px;
                margin-top: 20px;
            }

            .plot-container {
                width: 100%;
                height: 600px;
            }

            /* Language selector */
            .language-container {
                margin-bottom: 20px;
            }

            .language-dropdown {
                width: 100%;
            }

            /* Inputs column */
            .inputs-column {
                background-color: var(--background-color);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            .inputs-grid {
                display: grid;
                gap: 15px;
            }

            .input-container {
                width: 100%;
            }

            .input-label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                font-size: 0.9rem;
            }

            .input-field {
                width: 100%;
                padding: 8px;
                border: 1px solid var(--border-color);
                border-radius: 4px;
                font-size: 0.9rem;
            }

            .input-field:focus {
                border-color: var(--primary-color);
                outline: none;
                box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
            }

            .calculate-button {
                width: 100%;
                padding: 12px;
                background-color: var(--primary-color);
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1rem;
                margin-top: 20px;
                transition: background-color 0.3s;
            }

            .calculate-button:hover {
                background-color: #0056b3;
            }

            /* Visualization column (Plot and Table) */
            .visualization-column {
                display: grid;
                grid-template-columns: 1fr 1fr;  /* Split space between plot and table */
                gap: 20px;
                width: 100%;
            }

            .plot-wrapper, .table-wrapper {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 15px;
                height: 800px;  /* Fixed height for both containers */
                overflow: auto;  /* Add scrolling if content overflows */
            }

            /* Responsive design */
            @media (max-width: 1400px) {
                .main-content {
                    grid-template-columns: 280px 1fr;  /* Stack visualization column */
                }
                .visualization-column {
                    grid-template-columns: 1fr;  /* Stack plot and table */
                    grid-column: 2;
                }
            }

            @media (max-width: 900px) {
                .main-content {
                    grid-template-columns: 1fr;  /* Single column layout */
                }
                .visualization-column {
                    grid-template-columns: 1fr;
                    grid-column: 1;
                }
                .plot-wrapper, .table-wrapper {
                    height: auto;
                    min-height: 400px;
                }
                
                .plot-container {
                    height: 400px;
                }
                
                .table-wrapper {
                    overflow-x: auto;
                }
            }

            .download-section {
                display: flex;
                justify-content: flex-end;
                padding: 10px 0;
                margin-bottom: 15px;
            }
            
            .download-button {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 12px 20px;
                background-color: var(--primary-color);
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1rem;
                transition: all 0.3s ease;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .download-button:hover {
                background-color: #0056b3;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                transform: translateY(-1px);
            }
            
            .download-button:active {
                transform: translateY(0);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .download-button i {
                font-size: 1.1rem;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Callback for updating labels
@app.callback(
    [Output('title', 'children'),
     Output('language-label', 'children'),
     Output('purchase-price-label', 'children'),
     Output('equity-label', 'children'),
     Output('broker-fee-label', 'children'),
     Output('notary-fee-label', 'children'),
     Output('real-estate-transfer-tax-label', 'children'),
     Output('land-registry-label', 'children'),
     Output('extra-payment-label', 'children'),
     Output('repayment-rate-label', 'children'),
     Output('interest-rate-label', 'children'),
     Output('fixed-interest-label', 'children'),
     Output('calculate-button', 'children'),
     Output('translation-store', 'data'),
     Output('download-button-text', 'children')],
    [Input('language-selector', 'value')]
)
def update_language(language):
    translation = translations[language]
    return (
        translation['title'],
        translation['language'],
        translation['purchase_price'],
        translation['equity'],
        translation['broker_fee'],
        translation['notary_fee'],
        translation['real_estate_transfer_tax'],
        translation['land_registry'],
        translation['extra_payment'],
        translation['repayment_rate'],
        translation['interest_rate'],
        translation['fixed_interest'],
        translation['calculate'],
        language,
        translation['download_button']
    )

@app.callback(
    Output('calculation-store', 'data'),
    [Input('calculate-button', 'n_clicks')],
    [State('purchase-price', 'value'),
     State('equity', 'value'),
     State('broker-fee', 'value'),
     State('notary-fee', 'value'),
     State('real-estate-transfer-tax', 'value'),
     State('land-registry', 'value'),
     State('extra-payment', 'value'),
     State('repayment-rate', 'value'),
     State('interest-rate', 'value'),
     State('fixed-interest', 'value')]
)

## call another function here.
def store_calculations(n_clicks, purchase_price, equity, broker_fee,
                      notary_fee, real_estate_transfer_tax, land_registry, extra_payment_rate, 
                      repayment_rate, interest_rate, fixed_interest):
    if n_clicks == 0:
        return {}


    df_with_extra_repayment = generate_graph_df(
    kaufpreis=purchase_price,
    Eigenkapital=equity,
    Tilgungsrate=repayment_rate/100,
    Sollzins=interest_rate/100,
    Sollzinsbindung=fixed_interest,
    Sondertilgung_rate=extra_payment_rate/100,
    Grunderwerbsteuer_rate=real_estate_transfer_tax/100,
    Maklerprovison_rate=broker_fee/100,
    Notarkosten_rate=notary_fee/100,
    Grundbucheintrag_rate=land_registry/100,
    Start_Date='2024-12-01'
    )
    df_with_extra_repayment.to_csv('with_repayment.csv', index=False)  # Set index=False to exclude the index column

    df_without_extra_repayment = generate_graph_df(
        kaufpreis=purchase_price,
    Eigenkapital=equity,
    Tilgungsrate=repayment_rate/100,
    Sollzins=interest_rate/100,
    Sollzinsbindung=fixed_interest,
    Sondertilgung_rate=0,
    Grunderwerbsteuer_rate=real_estate_transfer_tax/100,
    Maklerprovison_rate=broker_fee/100,
    Notarkosten_rate=notary_fee/100,
    Grundbucheintrag_rate=land_registry/100,
    Start_Date='2024-12-01'
    )
    df_without_extra_repayment.to_csv('without_repayment.csv', index=False)  # Set index=False to exclude the index column
    
    scenarios_data={}

    """
    'Zinszahlung_List_Cumu':'累计利息', 
    'Tilgungszahlung_List_Cumu': '累计本金',
    'Sondertilgunszahlung_List_Cumu':'累计提前还款',
    'totaltilgungszahlung_List':'总还款',
    'aktuelle_Nettodarlehen_List':'贷款余额',
    'Familie_Spar_List_Cumu':'累计家庭存款',
    'Years_List':'年',
    'Zinszahlung_List':'每月还款利息',
    'Tilgungszahlung_List':'每月还款本金'
    """

    
    scenarios_data["without_extra_repayment"] = {
            'remaining_debt': df_without_extra_repayment['aktuelle_Nettodarlehen_List'],
            'cumulative_interest': df_without_extra_repayment['Zinszahlung_List_Cumu'],
            'paid_principal': df_without_extra_repayment['totaltilgungszahlung_List'],
            'monthly_interest': df_without_extra_repayment['Zinszahlung_List'],
            'monthly_principal': df_without_extra_repayment['Tilgungszahlung_List']
        }
    

    scenarios_data["with_extra_repayment"] = {
            'remaining_debt': df_with_extra_repayment['aktuelle_Nettodarlehen_List'],
            'cumulative_interest': df_with_extra_repayment['Zinszahlung_List_Cumu'],
            'paid_principal': df_with_extra_repayment['totaltilgungszahlung_List'],
            'monthly_interest': df_with_extra_repayment['Zinszahlung_List'],
            'monthly_principal': df_with_extra_repayment['Tilgungszahlung_List']
        }
    
    months=df_with_extra_repayment['Date']
    years =df_with_extra_repayment['Years_List']

    return {
        'months': months,
        'years':years,
        'scenarios': scenarios_data,
    }

# Modified callback for updating the plot
@app.callback(
    Output('mortgage-plot', 'figure'),
    [Input('calculation-store', 'data'),
     Input('language-selector', 'value')]
)
def update_graph(data, language):
    if not data:
        return go.Figure()
    
    fig = go.Figure()
    
    # Mapping for scenario names
    scenario_names = {
        #'with_extra_repayment': translations[language]['with_extra_repayment'],#,
        'remaining_loan':  translations[language]['remaining_loan'],
        'cumulative_interest':    translations[language]['cumulative_interest'],
        'paid_principal':    translations[language]['paid_principal'],
        'monthly_interest':    translations[language]['monthly_interest'],
        'monthly_principal':    translations[language]['monthly_principal'],
        #'without_extra_repayment': translations[language]['without_extra_repayment'],
        #'high_repayment': translations[language]['high_repayment']
    }
    
    language_map = translations[language]

    # Create hover template
    hover_template = """
        <b>%{customdata[4]}</b><br>
        %{customdata[10]}<br>
        %{customdata[5]}: %{y}<br>
        %{customdata[6]}: %{customdata[0]}<br>
        %{customdata[7]}: %{customdata[1]}<br>
        %{customdata[8]}: %{customdata[2]}<br>
        %{customdata[9]}: %{customdata[3]}<br>
        <extra></extra>
    """

    years=data['years']
    years_month=data['months']
    if language=="zh":
        years_month=convert_to_chinese(years_month)
    
    # Add traces for each scenario

    for scenario_type, scenario_data in data['scenarios'].items():
        # Convert months to years for x-axis
        # Starting point, e.g., January 2024
        # Convert to "Month Year" format
        
        # Prepare custom data for hover
        custom_data = list(zip(
            scenario_data['cumulative_interest'],
            scenario_data['paid_principal'],
            scenario_data['monthly_interest'],
            scenario_data['monthly_principal'],
            [translations[language][scenario_type]] * len(years),  # Scenario name for each point，
            [scenario_names['remaining_loan']]* len(years),
            [scenario_names['cumulative_interest']]* len(years),
            [scenario_names['paid_principal']]* len(years),
            [scenario_names['monthly_interest']]* len(years),
            [scenario_names['monthly_principal']]* len(years),
            years_month
        ))

        
        fig.add_trace(go.Scatter(
            x=years,
            y=scenario_data['remaining_debt'],
            name=translations[language][scenario_type],
            mode='lines+markers',
            customdata=custom_data,
            hovertemplate=hover_template
        ))
    
    # Update layout with translated labels
    fig.update_layout(
        title=translations[language]['plot_title'],
        xaxis_title=translations[language]['loan_duration'],
        yaxis_title=translations[language]['remaining_debt'],
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        height=800,
        hovermode='closest',
        hoverlabel=dict(
            bgcolor="white",  # Transparent hover label background
            font_color="black",       # Black text for hover label
        )
        #color="country"
    )
    
    return fig

# Add new callback for the table
@app.callback(
    Output('mortgage-table', 'data'),
    Output('mortgage-table', 'columns'),
    [Input('calculation-store', 'data'),
     Input('language-selector', 'value')]
)
def update_table(data, language):
    if not data:
        return [], []
    
    # Get the first scenario data (with extra repayment)
    scenario_data = data['scenarios']['with_extra_repayment']
    
    # Create table data with translated year
    table_data = []
    for i, (year, remaining, interest, principal) in enumerate(zip(
        data['years'],
        scenario_data['remaining_debt'],
        scenario_data['monthly_interest'],
        scenario_data['monthly_principal']
    )):
        table_data.append({
            'year': f'{translations[language]["year"]} {int(year)}',
            'remaining_debt': f'€{remaining:,.2f}',
            'monthly_interest': f'€{interest:,.2f}',
            'monthly_principal': f'€{principal:,.2f}',
            'total_payment': f'€{(interest + principal):,.2f}'
        })
    
    # Define columns with translations
    columns = [
        {'name': translations[language]['period'], 'id': 'year'},
        {'name': translations[language]['remaining_debt'], 'id': 'remaining_debt'},
        {'name': translations[language]['monthly_interest'], 'id': 'monthly_interest'},
        {'name': translations[language]['monthly_principal'], 'id': 'monthly_principal'},
        {'name': translations[language]['monthly_payment'], 'id': 'total_payment'}
    ]
    
    return table_data, columns

# Update the download callback
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download", "n_clicks"),
    [State('mortgage-table', 'data'),
     State('language-selector', 'value')],
    prevent_initial_call=True,
)
def download_table(n_clicks, table_data, language):
    if n_clicks is None:
        return None
    
    # Create DataFrame with translated column names
    df = pd.DataFrame(table_data)
    
    # Rename columns based on language
    column_translations = {
        'year': translations[language]['period'],
        'remaining_debt': translations[language]['remaining_debt'],
        'monthly_interest': translations[language]['monthly_interest'],
        'monthly_principal': translations[language]['monthly_principal'],
        'total_payment': translations[language]['monthly_payment']
    }
    
    df = df.rename(columns=column_translations)
    
    # Generate filename based on language
    filename = {
        'en': 'mortgage_amortization.csv',
        'de': 'tilgungsplan.csv',
        'zh': '还款计划表.csv'
    }[language]
    
    return dcc.send_data_frame(df.to_csv, filename, index=False)

if __name__ == '__main__':
    app.run_server(debug=True)