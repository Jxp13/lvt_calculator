import streamlit as st
import plotly.graph_objects as go

# Configure the page first
st.set_page_config(
    page_title="Business Scale Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS to ensure visibility
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

def calculate_ltv(arpu, churn_rate, gross_margin):
    if churn_rate == 0:
        return 0
    ltv = (arpu * (1/churn_rate) * gross_margin)
    return ltv

def get_recommendations(ltv_cac_ratio):
    if ltv_cac_ratio < 1:
        return {
            "status": "Critical - Immediate Action Required",
            "recommendations": [
                "Optimize your ad spend and marketing channels",
                "Improve your conversion rate optimization (CRO)",
                "Consider increasing your prices",
                "Review and reduce your customer acquisition costs",
                "Focus on improving customer retention"
            ]
        }
    elif 1 <= ltv_cac_ratio <= 3:
        return {
            "status": "Healthy - Room for Improvement",
            "recommendations": [
                "Start scaling your marketing efforts gradually",
                "Implement upselling and cross-selling strategies",
                "Focus on customer success and satisfaction",
                "Consider implementing a referral program",
                "Optimize your sales funnel"
            ]
        }
    else:
        return {
            "status": "Excellent - Growth Opportunity",
            "recommendations": [
                "Significantly increase marketing investment",
                "Explore new marketing channels",
                "Consider expanding to new markets",
                "Invest in product development",
                "Build a scalable customer success program"
            ]
        }

# Main app header
st.title("🚀 Business Scale Calculator (LTV/CAC)")
st.markdown("### Based on Alex Hormozi's Principles")

# Create two columns with better spacing
col1, spacer, col2 = st.columns([4, 1, 4])

with col1:
    st.markdown("### 📊 Enter Your Business Metrics")
    
    arpu = st.number_input(
        "Average Monthly Revenue Per Customer ($)",
        min_value=0.0,
        value=100.0,
        help="How much does an average customer pay you per month?"
    )
    
    churn_rate = st.number_input(
        "Monthly Churn Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        help="What percentage of customers leave each month?"
    ) / 100
    
    gross_margin = st.number_input(
        "Gross Margin (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0,
        help="What percentage of revenue remains after direct costs?"
    ) / 100
    
    cac = st.number_input(
        "Customer Acquisition Cost ($)",
        min_value=0.0,
        value=200.0,
        help="How much do you spend to acquire one customer?"
    )

# Calculate metrics
ltv = calculate_ltv(arpu, churn_rate, gross_margin)
ltv_cac_ratio = ltv / cac if cac > 0 else 0
payback_period = cac / (arpu * gross_margin) if arpu * gross_margin > 0 else 0

with col2:
    st.markdown("### 🎯 Key Results")
    
    # Display metrics with better formatting
    st.metric("Lifetime Value (LTV)", f"${ltv:,.2f}")
    st.metric("LTV/CAC Ratio", f"{ltv_cac_ratio:.2f}")
    st.metric("CAC Payback Period (Months)", f"{payback_period:.1f}")

# Get recommendations
recommendations = get_recommendations(ltv_cac_ratio)

# Display status and recommendations
st.markdown("---")
st.subheader(f"📈 Status: {recommendations['status']}")

st.markdown("### 🎯 Recommended Actions:")
for rec in recommendations['recommendations']:
    st.markdown(f"- {rec}")

# Create and display gauge
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=ltv_cac_ratio,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "LTV/CAC Ratio"},
    gauge={
        'axis': {'range': [None, 5]},
        'steps': [
            {'range': [0, 1], 'color': "lightcoral"},
            {'range': [1, 3], 'color': "khaki"},
            {'range': [3, 5], 'color': "lightgreen"}],
        'threshold': {
            'line': {'color': "black", 'width': 4},
            'thickness': 0.75,
            'value': ltv_cac_ratio}}
))

fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

# Additional metrics in a cleaner layout
st.markdown("### 📊 Additional Insights")
metric_cols = st.columns(3)

with metric_cols[0]:
    st.metric("Monthly Revenue per Customer", f"${arpu:,.2f}")
with metric_cols[1]:
    st.metric("Monthly Churn Rate", f"{churn_rate*100:.1f}%")
with metric_cols[2]:
    st.metric("Gross Margin", f"{gross_margin*100:.1f}%")

# Help section
st.markdown("---")
st.markdown("""
### 📘 How to Use This Calculator:
1. Enter your business metrics in the left panel
2. View your results and recommendations
3. Use the gauge to visualize your LTV/CAC ratio
4. Follow the recommended actions to improve your metrics

### 🎯 Target Metrics:
- Aim for an LTV/CAC ratio > 3
- Try to keep monthly churn rate < 5%
- Work towards a CAC payback period < 12 months
""")
