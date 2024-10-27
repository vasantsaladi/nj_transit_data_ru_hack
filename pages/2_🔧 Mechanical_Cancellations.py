import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from sklearn.linear_model import LinearRegression
import calendar

# Set page config
st.set_page_config(layout="wide", page_title="NJ Transit Mechanical Cancellations Analysis")

@st.cache_data
def load_data():
    # Load rail cancellations data
    df = pd.read_csv('/Users/chetan/Documents/GitHub/nj_transit_data_ru_hack/data/RAIL_CANCELLATIONS_DATA.csv')
    
    # Clean and prepare data
    df['MONTH'] = df['MONTH'].str.strip()
    df = df[df['CATEGORY'].str.contains('Mechanical', na=False)]
    
    # Convert month names to numbers
    month_map = {
        'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4,
        'MAY': 5, 'JUNE': 6, 'JULY': 7, 'AUGUST': 8,
        'SEPTEMBER': 9, 'OCTOBER': 10, 'NOVEMBER': 11, 'DECEMBER': 12
    }
    df['MONTH_NUM'] = df['MONTH'].map(month_map)
    
    # Create date column for better visualization
    df['DATE'] = pd.to_datetime(df.apply(lambda x: f"{x['YEAR']}-{x['MONTH_NUM']:02d}-01", axis=1))
    
    return df

def predict_mechanical_failures(data, target_month=None):
    X = data[['YEAR', 'MONTH_NUM']].values
    y = data['CANCEL_PERCENTAGE'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    if target_month:
        # Predict for specific month across years
        years = range(data['YEAR'].min(), data['YEAR'].max() + 2)
        future_dates = [[year, target_month] for year in years]
        predictions = model.predict(np.array(future_dates))
        return future_dates, predictions
    else:
        # Predict next 6 months
        current_year = data['YEAR'].max()
        current_month = data['MONTH_NUM'].max()
        
        future_dates = []
        for i in range(1, 7):
            month = (current_month + i) % 12
            if month == 0:
                month = 12
            year = current_year + (current_month + i - 1) // 12
            future_dates.append([year, month])
        
        predictions = model.predict(np.array(future_dates))
        return future_dates, predictions

def create_monthly_heatmap(df):
    # Pivot data for heatmap
    heatmap_data = df.pivot_table(
        values='CANCEL_PERCENTAGE',
        index='YEAR',
        columns='MONTH_NUM',
        aggfunc='mean'
    ).round(1)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=[calendar.month_abbr[i] for i in range(1, 13)],
        y=heatmap_data.index,
        colorscale='RdYlBu_r',
        text=np.round(heatmap_data.values, 1),
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title='Cancellation Rate (%)')
    ))
    
    fig.update_layout(
        title='Monthly Mechanical Cancellation Rates Heatmap',
        xaxis_title='Month',
        yaxis_title='Year'
    )
    
    return fig

def main():
    st.title("🚂 NJ Transit Rail Mechanical Cancellations Analysis")
        # Display explanation image
    st.image('/Users/chetan/Documents/GitHub/nj_transit_data_ru_hack/assets/output.png',
             caption='Distribution of Cancellation Categories',
             use_column_width=True)
    # Load data
    df = load_data()
    
    # Main metrics
    st.header("Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_mechanical_rate = df['CANCEL_PERCENTAGE'].mean()
        st.metric("Average Mechanical Cancellation Rate", f"{avg_mechanical_rate:.1f}%")
    
    with col2:
        recent_rate = df[df['YEAR'] == df['YEAR'].max()]['CANCEL_PERCENTAGE'].mean()
        st.metric("Recent Year Average", f"{recent_rate:.1f}%", 
                 f"{recent_rate - avg_mechanical_rate:.1f}%")
    
    with col3:
        max_month = df.loc[df['CANCEL_PERCENTAGE'].idxmax()]
        st.metric("Highest Cancellation Month", 
                 f"{max_month['MONTH']} {max_month['YEAR']}", 
                 f"{max_month['CANCEL_PERCENTAGE']:.1f}%")

    # Monthly Pattern Analysis
    st.header("Monthly Cancellation Patterns")
    
    # Heatmap
    heatmap_fig = create_monthly_heatmap(df)
    st.plotly_chart(heatmap_fig, use_container_width=True)
    
    # Historical trend with trend line
    fig_trend = px.scatter(df, 
                          x='DATE', 
                          y='CANCEL_PERCENTAGE',
                          trendline="lowess",
                          title='Historical Mechanical Cancellation Trend',
                          labels={'CANCEL_PERCENTAGE': 'Cancellation Rate (%)',
                                 'DATE': 'Date'})
    
    fig_trend.update_traces(marker=dict(size=8))
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Monthly box plot
    fig_box = px.box(df, 
                     x='MONTH', 
                     y='CANCEL_PERCENTAGE',
                     title='Monthly Distribution of Mechanical Cancellations',
                     labels={'CANCEL_PERCENTAGE': 'Cancellation Rate (%)',
                            'MONTH': 'Month'})
    st.plotly_chart(fig_box, use_container_width=True)

    # Prediction Section
    st.header("Mechanical Failure Predictions")
    
    # Month selector for predictions
    months = list(calendar.month_name)[1:]
    selected_month = st.selectbox("Select month for prediction", months)
    selected_month_num = months.index(selected_month) + 1
    
    # Get predictions for selected month
    future_dates, predictions = predict_mechanical_failures(df, selected_month_num)
    
    # Create prediction chart
    fig_predict = go.Figure()
    
    # Historical data for selected month
    historical_data = df[df['MONTH_NUM'] == selected_month_num]
    fig_predict.add_trace(go.Scatter(
        x=historical_data['YEAR'],
        y=historical_data['CANCEL_PERCENTAGE'],
        name='Historical Data',
        mode='markers+lines',
        marker=dict(size=8)
    ))
    
    # Predictions
    fig_predict.add_trace(go.Scatter(
        x=[date[0] for date in future_dates],
        y=predictions,
        name='Prediction Trend',
        mode='lines',
        line=dict(dash='dash', color='red')
    ))
    
    fig_predict.update_layout(
        title=f'Mechanical Cancellation Predictions for {selected_month}',
        xaxis_title='Year',
        yaxis_title='Cancellation Rate (%)',
        hovermode='x unified'
    )
    st.plotly_chart(fig_predict, use_container_width=True)

    # Cost Impact Analysis
    st.header("Cost Impact Analysis")
    avg_cost_per_cancellation = 5000
    
    col1, col2 = st.columns(2)
    with col1:
        predicted_rate = predictions[-1]
        predicted_cost = predicted_rate * avg_cost_per_cancellation
        st.metric(
            f"Predicted Cost for {selected_month}",
            f"${predicted_cost:,.2f}",
            f"Based on {predicted_rate:.1f}% cancellation rate"
        )
    
    with col2:
        potential_savings = predicted_cost * 0.15
        st.metric(
            "Potential Monthly Savings",
            f"${potential_savings:,.2f}",
            "Through preventive maintenance"
        )

    # Insights
    st.header("Key Insights")
    st.write(f"""
    ### Monthly Analysis for {selected_month}:
    - Historical average cancellation rate: {historical_data['CANCEL_PERCENTAGE'].mean():.1f}%
    - Predicted cancellation rate: {predicted_rate:.1f}%
    - Risk level: {'High' if predicted_rate > avg_mechanical_rate else 'Moderate' if predicted_rate > avg_mechanical_rate/2 else 'Low'}
    
    ### Recommendations:
    - {'Increase maintenance frequency' if predicted_rate > avg_mechanical_rate else 'Maintain regular schedule'}
    - {'Schedule additional inspections' if predicted_rate > avg_mechanical_rate * 1.2 else 'Continue standard inspections'}
    - Focus on preventive maintenance during {'winter months' if selected_month_num in [12,1,2] else 'summer months' if selected_month_num in [6,7,8] else 'transition months'}
    """)

if __name__ == "__main__":
    main()