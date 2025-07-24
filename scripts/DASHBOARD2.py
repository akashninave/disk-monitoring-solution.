import pandas as pd
from prophet import Prophet
import dash
from dash import html, dcc
import plotly.graph_objs as go

# Path to your unified CSV file
csv_path = r'/Users/akashninave/Akash_Drive/JOB HUNTER/LUCIDITY/client outputs/unified_time_series_data.csv'

# Load and clean columns
df = pd.read_csv(csv_path, parse_dates=['timestamp'])
df.columns = df.columns.str.strip()

client_col = 'client_name'
vm_col = 'vm_id'

clients = sorted(df[client_col].unique())
client_vms = {c: sorted(df[df[client_col] == c][vm_col].unique()) for c in clients}

app = dash.Dash(__name__)
app.title = "Disk Usage Forecast Dashboard"

def make_vm_forecast_trace(client, vm_id):
    vm_data = df[(df[client_col] == client) & (df[vm_col] == vm_id)][['timestamp', 'used_percent']] \
        .rename(columns={'timestamp': 'ds', 'used_percent': 'y'}).dropna().sort_values('ds')

    # Fit on all historical data
    model = Prophet(daily_seasonality=False, yearly_seasonality=False)
    model.fit(vm_data)

    # Forecast next 15 days hourly
    future = model.make_future_dataframe(periods=15*24, freq='H')
    forecast = model.predict(future)

    # Clip values between 0 and 100%
    forecast['yhat'] = forecast['yhat'].clip(lower=0, upper=100)
    forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0, upper=100)
    forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=0, upper=100)

    last_actual_time = vm_data['ds'].max()

    # Split forecast into historical + future for plotting
    forecast_hist = forecast[forecast['ds'] <= last_actual_time]
    forecast_future = forecast[forecast['ds'] > last_actual_time]

    fig = go.Figure()

    # Plot actual usage (solid blue)
    fig.add_trace(go.Scatter(
        x=vm_data['ds'], y=vm_data['y'],
        mode='lines+markers',
        name='Actual',
        line=dict(color='blue', width=3),
        marker=dict(size=5)
    ))

    # Plot forecast over historical period (faded orange)
    fig.add_trace(go.Scatter(
        x=forecast_hist['ds'], y=forecast_hist['yhat'],
        mode='lines',
        name='Forecast (Historical)',
        line=dict(color='orange', width=2, dash='dot'),
        opacity=0.4
    ))

    # Plot forecast over future period (solid orange dashed)
    fig.add_trace(go.Scatter(
        x=forecast_future['ds'], y=forecast_future['yhat'],
        mode='lines',
        name='Forecast (Next 15 days)',
        line=dict(color='orange', width=2, dash='dash')
    ))

    # Add forecast uncertainty shaded area for future period
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_future['ds'], forecast_future['ds'][::-1]]),
        y=pd.concat([forecast_future['yhat_upper'], forecast_future['yhat_lower'][::-1]]),
        fill='toself',
        fillcolor='rgba(255, 165, 0, 0.2)',  # light orange
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Forecast Uncertainty'
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=30, r=30, t=30, b=30),
        xaxis_title='Time',
        yaxis_title='Disk Usage (%)',
        yaxis=dict(range=[0, 105]),
        hovermode='x unified'
    )
    return fig

app.layout = html.Div([
    html.H1("Disk Usage Forecast Dashboard", style={'textAlign': 'center', 'marginBottom': '30px'}),
    *[
        html.Div([
            html.H2(client, style={'cursor': 'pointer', 'backgroundColor': '#ddd', 'padding': '10px'}),
            html.Div(
                id=f"{client}-container",
                children=[
                    dcc.Graph(id=f'graph-{vm_id}', figure=make_vm_forecast_trace(client, vm_id))
                    for vm_id in client_vms[client]
                ],
                style={'marginLeft': '20px', 'marginBottom': '40px'}
            )
        ], style={'border': '1px solid #ccc', 'marginBottom': '20px',
                  'borderRadius': '5px', 'padding': '5px'})
        for client in clients
    ]
])

if __name__ == '__main__':
    app.run(debug=True, port=8060)
