# import pandas as pd
# from dash import Dash, dcc, html, Input, Output
# import plotly.express as px

# # Load the data
# df = pd.read_excel(r'C:\Users\Vidhi Shah\Downloads\order-summary-3.xlsx', sheet_name='Sheet1')
# # Clean column names and remove unnamed columns
# df.columns = df.columns.str.strip()
# df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# # Drop rows with missing key fields
# df = df.dropna(subset=['State', 'Lost Reason', 'Priority', 'Frequency (No. of Orders lost)'])

# # Ensure correct data types
# df['Frequency (No. of Orders lost)'] = pd.to_numeric(df['Frequency (No. of Orders lost)'], errors='coerce').fillna(0)

# # Get unique sorted list of states
# states = sorted(df['State'].unique())

# # Initialize the Dash app
# app = Dash(__name__)
# app.title = "Lost Orders Dashboard"

# app.layout = html.Div([
#     html.H1("Lost Orders by State and Reason", style={'textAlign': 'center'}),
#     html.Div([
#         html.Label("Select State:", style={'fontWeight': 'bold'}),
#         dcc.Dropdown(
#             id='state-dropdown',
#             options=[{'label': state, 'value': state} for state in states],
#             value=states[0],
#             clearable=False,
#             style={'width': '300px'}
#         ),
#     ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '20px'}),
#     dcc.Graph(id='lost-reason-bar')
# ])

# @app.callback(
#     Output('lost-reason-bar', 'figure'),
#     Input('state-dropdown', 'value')
# )
# def update_chart(selected_state):
#     filtered = df[df['State'] == selected_state]
#     # Group by Lost Reason and Priority for stacking
#     grouped = filtered.groupby(['Lost Reason', 'Priority'])['Frequency (No. of Orders lost)'].sum().reset_index()
#     # Sort Lost Reasons by total frequency for better visuals
#     reason_order = grouped.groupby('Lost Reason')['Frequency (No. of Orders lost)'].sum().sort_values(ascending=False).index
#     grouped['Lost Reason'] = pd.Categorical(grouped['Lost Reason'], categories=reason_order, ordered=True)
#     fig = px.bar(
#         grouped,
#         x='Lost Reason',
#         y='Frequency (No. of Orders lost)',
#         color='Priority',
#         barmode='stack',
#         title=f"Lost Orders Reasons in {selected_state}",
#         labels={'Frequency (No. of Orders lost)': 'Number of Lost Orders'},
#         color_discrete_sequence=px.colors.qualitative.Pastel
#     )
#     fig.update_layout(xaxis_tickangle=-45, legend_title_text='Priority', yaxis_title='Number of Lost Orders')
#     return fig

# if __name__ == '__main__':
#     app.run(debug=True)
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load the data
df = pd.read_excel(r'C:\Users\Vidhi Shah\Downloads\order-summary-3.xlsx', sheet_name='Sheet1')
df.columns = df.columns.str.strip()
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.dropna(subset=['State', 'Lost Reason', 'Priority', 'Frequency (No. of Orders lost)'])
df['Frequency (No. of Orders lost)'] = pd.to_numeric(df['Frequency (No. of Orders lost)'], errors='coerce').fillna(0)
states = sorted(df['State'].unique())

# State-specific solutions (state names must match your Excel exactly!)
state_solutions = {
    'ANDHRA PRADESH': {
        'problem': "Price discovery (customers finding better prices elsewhere or perceiving your price as too high).",
        'solutions': [
            "Dynamic Price Benchmarking & Tiered Value Offerings: Log every competitor price for top SKUs, update weekly. Create three value tiers: Basic (within 2-3% of lowest competitor), Core (standard), Premium (extra service/warranty).",
            "Cost-Down Price-Match Guarantee: Identify top 2 undercutting competitors, do rapid cost-down analysis, and offer price-match guarantee only against those two, contingent on customer proof."
        ]
    },
    'WEST BENGAL': {
        'problem': "Price discovery (customers finding better prices elsewhere or perceiving your price as too high).",
        'solutions': [
            "Dynamic Price Benchmarking & Tiered Value Offerings: Log every competitor price for top SKUs, update weekly. Create three value tiers: Basic (within 2-3% of lowest competitor), Core (standard), Premium (extra service/warranty).",
            "Cost-Down Price-Match Guarantee: Identify top 2 undercutting competitors, do rapid cost-down analysis, and offer price-match guarantee only against those two, contingent on customer proof."
        ]
    },
    'CHHATTISGARH': {
        'problem': "Bidding/Requirement cancelled/Uncertain/Delay.",
        'solutions': [
            "Pre-Emptive Requirement Shaping & Risk-Scored Bidding: Identify large bids early, offer consultative sessions, and use a bid risk scorecard (budget, requirement stability, influence, timeline, funding source).",
            "Phased Commitment & Modular Bidding: Propose phased bids (e.g., Phase 1: 100MT, Phase 2: 500MT) and modular offers for uncertain projects."
        ]
    },
    'GOA': {
        'problem': "Bidding/Requirement cancelled/Uncertain/Delay.",
        'solutions': [
            "Phased Commitment & Modular Bidding: Propose phased bids (e.g., Phase 1: 100MT, Phase 2: 500MT) and modular offers for uncertain projects.",
            "Shorter price validity or escalation clause for government bids prone to delays."
        ]
    },
    'MADHYA PRADESH': {
        'problem': "Bidding/Requirement cancelled/Uncertain/Delay.",
        'solutions': [
            "Pre-Emptive Requirement Shaping & Risk-Scored Bidding: Identify large bids early, offer consultative sessions, and use a bid risk scorecard (budget, requirement stability, influence, timeline, funding source).",
            "Phased Commitment & Modular Bidding: Propose phased bids (e.g., Phase 1: 100MT, Phase 2: 500MT) and modular offers for uncertain projects."
        ]
    },
    'RAJASTHAN': {
        'problem': "Bidding/Requirement cancelled/Uncertain/Delay.",
        'solutions': [
            "Phased Commitment & Modular Bidding: Propose phased bids (e.g., Phase 1: 100MT, Phase 2: 500MT) and modular offers for uncertain projects.",
            "Shorter price validity or escalation clause for government bids prone to delays."
        ]
    },
    'KARNATAKA': {
        'problem': "Customer loyalty to competitor brands.",
        'solutions': [
            "Competitive Switcher Program with Performance Guarantee: Identify top competitor brands, offer a switcher kit (side-by-side comparison, testimonials, pilot batch with performance guarantee).",
            "Influencer Seeding & Co-Marketing: Partner with local influencers and complementary businesses for testimonials and bundled offers."
        ]
    },
    'MAHARASHTRA': {
        'problem': "Customer loyalty to competitor brands and credit issues.",
        'solutions': [
            "Influencer Seeding & Co-Marketing: Partner with local influencers and complementary businesses for testimonials and bundled offers.",
            "Risk-Based Dynamic Credit Policy & Early Payment Incentive: Implement a strict credit scoring model and offer early payment discounts for low-risk customers."
        ]
    },
    'TELANGANA': {
        'problem': "Customer loyalty to competitor brands.",
        'solutions': [
            "Competitive Switcher Program with Performance Guarantee: Identify top competitor brands, offer a switcher kit (side-by-side comparison, testimonials, pilot batch with performance guarantee)."
        ]
    },
    'TAMIL NADU': {
        'problem': "Customer loyalty to competitor brands and credit issues.",
        'solutions': [
            "Influencer Seeding & Co-Marketing: Partner with local influencers and complementary businesses for testimonials and bundled offers.",
            "Risk-Based Dynamic Credit Policy & Early Payment Incentive: Implement a strict credit scoring model and offer early payment discounts for low-risk customers."
        ]
    },
    'GUJARAT': {
        'problem': "Restricted vendor lists (empanelment barriers).",
        'solutions': [
            "Targeted Empanelment Strike Team & Value Proposition for Approvers: Dedicate a team to target top 10 restricted organizations, tailor value proposition for procurement committee, and track progress weekly."
        ]
    },
    'UTTAR PRADESH': {
        'problem': "Other (requires deep investigation).",
        'solutions': [
            "Rapid Root Cause Analysis Sprints & Pilot Solution Testing: Cross-functional team conducts interviews and data analysis, then pilots small solutions (e.g., Hindi brochures, local support) in one district and tracks conversion rates."
        ]
    }
}

# Initialize the Dash app
app = Dash(__name__)
app.title = "Lost Orders Dashboard"

app.layout = html.Div([
    html.H1("Lost Orders by State and Reason", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select State:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in states],
            value=states[0],
            clearable=False,
            style={'width': '300px'}
        ),
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '20px'}),
    dcc.Graph(id='lost-reason-bar'),
    html.Div(id='state-solutions', style={
        'margin': '30px',
        'padding': '20px',
        'border': '1px solid #ddd',
        'borderRadius': '5px',
        'backgroundColor': '#f9f9f9'
    })
])

@app.callback(
    [Output('lost-reason-bar', 'figure'),
     Output('state-solutions', 'children')],
    [Input('state-dropdown', 'value')]
)
def update_content(selected_state):
    filtered = df[df['State'] == selected_state]
    grouped = filtered.groupby(['Lost Reason', 'Priority'])['Frequency (No. of Orders lost)'].sum().reset_index()
    reason_order = grouped.groupby('Lost Reason')['Frequency (No. of Orders lost)'].sum().sort_values(ascending=False).index
    grouped['Lost Reason'] = pd.Categorical(grouped['Lost Reason'], categories=reason_order, ordered=True)
    fig = px.bar(
        grouped,
        x='Lost Reason',
        y='Frequency (No. of Orders lost)',
        color='Priority',
        barmode='stack',
        title=f"Lost Orders Reasons in {selected_state}",
        labels={'Frequency (No. of Orders lost)': 'Number of Lost Orders'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(xaxis_tickangle=-45, legend_title_text='Priority', yaxis_title='Number of Lost Orders')

    # State-specific solution section
    if selected_state in state_solutions:
        strat = state_solutions[selected_state]
        solution_block = [
            html.H3(f"{selected_state} - Statistical Problem & Solutions", style={'color': '#2c3e50'}),
            html.H4("Problem:", style={'color': '#dc3545'}),
            html.P(strat['problem'], style={'marginLeft': '20px'}),
            html.H4("Recommended Statistical Solutions:", style={'color': '#28a745', 'marginTop': '15px'}),
            html.Ul([html.Li(sol) for sol in strat['solutions']], style={'marginLeft': '30px'})
        ]
    else:
        solution_block = [
            html.H3("General Recommendations", style={'color': '#2c3e50'}),
            html.Ul([
                html.Li("Analyze top 3 lost reasons for targeted interventions"),
                html.Li("Implement regional price benchmarking"),
                html.Li("Develop local distributor partnerships")
            ], style={'marginLeft': '30px'})
        ]

    return fig, solution_block

if __name__ == '__main__':
    app.run_server(debug=True)
