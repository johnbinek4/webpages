import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    section[data-testid="stSidebarNav"] {
        display: none;
    }
    .main-title {
        text-align: center;
        color: #1f1f1f;
        font-size: 36px;
        font-weight: 600;
        margin-bottom: 30px;
        padding-top: 20px;
    }
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

# Calculate monthly returns
df['YearMonth'] = df['Date'].dt.to_period('M')
monthly_returns = df.groupby('YearMonth').agg({
    'Portfolio_Return': lambda x: (1 + x).prod() - 1,
    'SPXTR_Return': lambda x: (1 + x).prod() - 1
}).reset_index()

def calculate_metrics(filtered_df, monthly_rets):
    """Calculate enhanced portfolio metrics including all major risk-adjusted ratios"""
    days_in_year = 252
    
    # Daily returns calculations
    returns = filtered_df['Portfolio_Return'].dropna()
    benchmark_returns = filtered_df['SPXTR_Return'].dropna()
    
    # Monthly returns calculations
    monthly_port_returns = monthly_rets['Portfolio_Return']
    monthly_bench_returns = monthly_rets['SPXTR_Return']
    
    # Basic return metrics
    total_return = (filtered_df['Portfolio'].iloc[-1] / filtered_df['Portfolio'].iloc[0] - 1)
    annualization_factor = days_in_year / (len(filtered_df) - 1)
    annualized_return = (1 + total_return) ** annualization_factor - 1
    
    # Risk calculations
    daily_std = returns.std()
    monthly_std = monthly_port_returns.std()
    annualized_vol = daily_std * np.sqrt(days_in_year)
    
    # Sharpe Ratio calculations
    daily_sharpe = np.mean(returns) / np.std(returns)
    annualized_sharpe = daily_sharpe * np.sqrt(days_in_year)
    
    monthly_sharpe = np.mean(monthly_port_returns) / np.std(monthly_port_returns)
    monthly_annualized_sharpe = monthly_sharpe * np.sqrt(12)
    
    # Beta calculation
    beta = returns.cov(benchmark_returns) / benchmark_returns.var()
    
    # Treynor Ratio (annualized return / beta)
    treynor_ratio = annualized_return / beta if beta != 0 else np.nan
    
    # Information Ratio calculations
    # Daily tracking error and IR
    daily_active_returns = returns - benchmark_returns
    tracking_error_daily = np.std(daily_active_returns) * np.sqrt(days_in_year)
    information_ratio = np.mean(daily_active_returns) * days_in_year / tracking_error_daily if tracking_error_daily != 0 else np.nan
    
    # Monthly tracking error and IR
    monthly_active_returns = monthly_port_returns - monthly_bench_returns
    tracking_error_monthly = np.std(monthly_active_returns) * np.sqrt(12)
    monthly_information_ratio = np.mean(monthly_active_returns) * 12 / tracking_error_monthly if tracking_error_monthly != 0 else np.nan
    
    # Sortino Ratio calculations
    # Daily Sortino
    downside_returns = returns[returns < 0]
    downside_std = np.sqrt(np.mean(downside_returns**2)) * np.sqrt(days_in_year)
    sortino_ratio = annualized_return / downside_std if len(downside_returns) > 0 else np.nan
    
    # Monthly Sortino
    monthly_downside_returns = monthly_port_returns[monthly_port_returns < 0]
    monthly_downside_std = np.sqrt(np.mean(monthly_downside_returns**2)) * np.sqrt(12)
    monthly_sortino = (np.mean(monthly_port_returns) * 12) / monthly_downside_std if len(monthly_downside_returns) > 0 else np.nan
    
    # Drawdown calculations
    portfolio_values = filtered_df['Portfolio']
    rolling_max = portfolio_values.expanding().max()
    drawdowns = (portfolio_values - rolling_max) / rolling_max
    max_drawdown = drawdowns.min() * 100  # Convert to percentage
    
    # Monthly statistics
    best_month = monthly_port_returns.max() * 100
    worst_month = monthly_port_returns.min() * 100
    avg_month = monthly_port_returns.mean() * 100
    up_months = (monthly_port_returns > 0).mean() * 100
    down_months = (monthly_port_returns < 0).mean() * 100
    avg_loss = monthly_port_returns[monthly_port_returns < 0].mean() * 100 if len(monthly_port_returns[monthly_port_returns < 0]) > 0 else 0
    
    # Distribution statistics
    skewness = stats.skew(monthly_port_returns)
    kurtosis = stats.kurtosis(monthly_port_returns)
    
    metrics_data = {
        'Metric': [
            'Total Return',
            'Annualized Return',
            'Annualized Volatility',
            'Sharpe Ratio (Ann.)',
            'Monthly Sharpe (Ann.)',
            'Sortino Ratio (Ann.)',
            'Monthly Sortino (Ann.)',
            'Information Ratio',
            'Monthly Info Ratio',
            'Treynor Ratio',
            'Tracking Error (Ann.)',
            'Beta',
            'Maximum Drawdown',
            'Best Month',
            'Worst Month',
            'Average Month',
            'Up Months %',
            'Down Months %',
            'Average Loss',
            'Monthly Std Dev (Ann.)',
            'Skewness',
            'Kurtosis'
        ],
        'Value': [
            f"{total_return*100:,.2f}%",
            f"{annualized_return*100:,.2f}%",
            f"{annualized_vol*100:,.2f}%",
            f"{annualized_sharpe:.2f}",
            f"{monthly_annualized_sharpe:.2f}",
            f"{sortino_ratio:.2f}",
            f"{monthly_sortino:.2f}",
            f"{information_ratio:.2f}",
            f"{monthly_information_ratio:.2f}",
            f"{treynor_ratio:.2f}",
            f"{tracking_error_daily*100:.2f}%",
            f"{beta:.2f}",
            f"{max_drawdown:,.2f}%",
            f"{best_month:.2f}%",
            f"{worst_month:.2f}%",
            f"{avg_month:.2f}%",
            f"{up_months:.1f}%",
            f"{down_months:.1f}%",
            f"{avg_loss:.2f}%",
            f"{monthly_std*np.sqrt(12)*100:.2f}%",
            f"{skewness:.2f}",
            f"{kurtosis:.2f}"
        ]
    }
    
    return pd.DataFrame(metrics_data)

# Add sidebar navigation
with st.sidebar:
    st.title("Trading Philosophy")
    philosophy_nav = st.radio(
        "Trading Strategy Selection",
        ["Performance Dashboard", "Market Maker Exposure", "Long / Short Volatility"],
        key="philosophy_nav",
        label_visibility="collapsed"
    )

# Handle Trading Philosophy navigation
if philosophy_nav == "Performance Dashboard":
    # Create two columns with metrics on left, charts on right
    col1, col2 = st.columns([1, 2], gap="small")

    with col1:
        # Calculate metrics
        metrics_df = calculate_metrics(df, monthly_returns)
        
        # Display the dataframe with exact height
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
            height=(len(metrics_df) * 35 + 3)  # Precise height calculation based on number of rows
        )

    with col2:
        # Create performance figure
        fig = px.line(df, x='Date', y=['Portfolio', 'SPXTR Index'],
                    labels={'value': 'Value ($)', 'variable': 'Series'},
                    title='Performance')

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

        fig.update_layout(
            height=500,
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

        # Create monthly returns distribution
        fig_dist = go.Figure()

        # Add histogram for Portfolio returns
        fig_dist.add_trace(go.Histogram(
            x=monthly_returns['Portfolio_Return'] * 100,
            name='Portfolio',
            opacity=0.75,
            nbinsx=20
        ))

        # Add histogram for SPXTR returns
        fig_dist.add_trace(go.Histogram(
            x=monthly_returns['SPXTR_Return'] * 100,
            name='SPXTR Index',
            opacity=0.75,
            nbinsx=20
        ))

        fig_dist.update_layout(
            title='Monthly Returns Distribution',
            title_x=0.5,
            xaxis_title='Monthly Return (%)',
            yaxis_title='Frequency',
            barmode='overlay',
            template="plotly_dark",
            height=300,
            margin=dict(l=0, r=0, t=40, b=0),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        st.plotly_chart(fig_dist, use_container_width=True)

elif philosophy_nav == "Market Maker Exposure":
    st.write("""
    Coming Soon
    """)

elif philosophy_nav == "Long / Short Volatility":
    st.write("""
    Coming Soon
    """)