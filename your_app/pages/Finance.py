import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

# Set the page title and layout
st.set_page_config(page_title="Finance Page", layout="wide")

# Add sidebar with styling
st.markdown("""
    <style>
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    #MainMenu {
        display: none;
    }
    /* Hide default sidebar nav */
    section[data-testid="stSidebarNav"] {
        display: none;
    }
    /* Main title styling */
    .main-title {
        text-align: center;
        color: #1f1f1f;
        font-size: 36px;
        font-weight: 600;
        margin-bottom: 30px;
        padding-top: 20px;
    }
    /* Table styling */
    [data-testid="stDataFrame"] {
        padding: 0px !important;
    }
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stDataFrame"] > div {
        height: fit-content !important;
    }
    </style>
""", unsafe_allow_html=True)

# Add main title
st.markdown('<div class="main-title">Quantitative Trading</div>', unsafe_allow_html=True)

# Read and process data
import os
df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tradingHist.csv'))
df.rename(columns={'hyp': 'Portfolio', 'hyp2': 'SPXTR Index'}, inplace=True)
df['Portfolio'] = df['Portfolio'].str.replace('$', '').astype(float)
df['SPXTR Index'] = df['SPXTR Index'].str.replace('$', '').astype(float)
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
df['Portfolio_Return'] = df['Portfolio'].pct_change()
df['SPXTR_Return'] = df['SPXTR Index'].pct_change()

def calculate_metrics(filtered_df):
    """Calculate portfolio metrics"""
    # Calculate actual number of trading days and annualization factor
    total_days = len(filtered_df) - 1  # Subtract 1 because we lose a day calculating returns
    days_in_year = 252
    annualization_factor = days_in_year / total_days
    
    returns = filtered_df['Portfolio_Return'].dropna()
    benchmark_returns = filtered_df['SPXTR_Return'].dropna()
    
    # Basic return metrics
    total_return = (filtered_df['Portfolio'].iloc[-1] / filtered_df['Portfolio'].iloc[0] - 1)
    
    # Annualize the total return properly
    annualized_return = (1 + total_return) ** annualization_factor - 1
    
    # Risk calculations
    daily_std = returns.std()
    annualized_vol = daily_std * np.sqrt(days_in_year)  # Standard deviation still uses sqrt(252)
    
    # Sharpe Ratio using raw decimals
    sharpe_ratio = annualized_return / annualized_vol
    
    # Convert to percentages for display
    total_return_pct = total_return * 100
    annualized_return_pct = annualized_return * 100
    annualized_vol_pct = annualized_vol * 100
    
    # Calculate drawdown
    cum_returns = (1 + returns).cumprod()
    rolling_max = cum_returns.expanding().max()
    drawdowns = cum_returns / rolling_max - 1
    max_drawdown = drawdowns.min() * 100
    
    # Beta and Correlation
    beta = returns.cov(benchmark_returns) / benchmark_returns.var()
    correlation = returns.corr(benchmark_returns)
    
    metrics_data = {
        'Metric': [
            'Total Return',
            'Annualized Return',
            'Annualized Volatility',
            'Sharpe Ratio',
            'Maximum Drawdown',
            'Beta',
            'Correlation'
        ],
        'Value': [
            f"{total_return_pct:,.2f}%",
            f"{annualized_return_pct:,.2f}%",
            f"{annualized_vol_pct:,.2f}%",
            f"{sharpe_ratio:.2f}",
            f"{max_drawdown:,.2f}%",
            f"{beta:.2f}",
            f"{correlation:.2f}"
        ]
    }
    
    return pd.DataFrame(metrics_data)

# Add sidebar navigation
with st.sidebar:
    # Trading Philosophy section only
    st.title("Trading Philosophy")
    philosophy_nav = st.radio(
        "Trading Strategy Selection",  # Added descriptive label
        ["Performance Dashboard", "Market Maker Exposure", "Long / Short Volatility"],
        key="philosophy_nav",
        label_visibility="collapsed"  # Hides the label while keeping it accessible
    )

# Handle Trading Philosophy navigation
if philosophy_nav == "Performance Dashboard":
    # Create two columns for plot and metrics
    col1, col2 = st.columns([2, 1], gap="small")

    with col1:
        # Create figure with buttons
        fig = px.line(df, x='Date', y=['Portfolio', 'SPXTR Index'],
                    labels={'value': 'Value ($)', 'variable': 'Series'},
                    title='Performance')

        # Add range selector buttons inside the plot
        fig.update_xaxes(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(step="all", label="ALL")
                ])
            )
        )

        # Customize layout
        fig.update_layout(
            height=700,
            margin=dict(l=0, r=0, t=40, b=0),
            title_font_size=24,
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Value ($)",
            legend_title="Series",
            template="plotly_dark",
            hovermode='x unified',
            yaxis_tickprefix='$',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        metrics_df = calculate_metrics(df)
        
        # Center align the title
        st.markdown("<h2 style='text-align: center; color: #333333;'>Analytics</h2>", unsafe_allow_html=True)
        
        # Calculate row height based on number of metrics
        row_height = 43  # Approximate height per row
        num_metrics = len(metrics_df)
        table_height = row_height * num_metrics
        
        # Style the dataframe
        st.dataframe(
            metrics_df,
            column_config={
                "Metric": st.column_config.Column(
                    "Metric",
                    width=200,
                ),
                "Value": st.column_config.Column(
                    "Value",
                    width=150,
                ),
            },
            hide_index=True,
            use_container_width=True,
            height=table_height
        )

elif philosophy_nav == "Market Maker Exposure":
    st.write("""
    Coming Soon
    """)

elif philosophy_nav == "Long / Short Volatility":
    st.write("""
    Coming Soon
    """)