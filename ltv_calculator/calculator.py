import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(page_title="Advanced LTV/CAC Calculator", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {padding: 20px;}
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .section-header {
        background-color: #f7f7f7;
        padding: 10px;
        border-radius: 5px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for scenario planning
if 'base_ltv' not in st.session_state:
    st.session_state.base_ltv = 0
if 'base_cac' not in st.session_state:
    st.session_state.base_cac = 0

# Title
st.title("🚀 Advanced Business Metrics Calculator")
st.markdown("### Detailed Analysis & Scenario Planning")

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1️⃣ LTV Calculator", 
    "2️⃣ CAC Analysis", 
    "3️⃣ Churn Analysis",
    "4️⃣ Detailed Insights",
    "5️⃣ Scenario Planning"
])

# Section 1: LTV Calculator
with tab1:
    st.markdown("### 📊 Lifetime Value (LTV) Calculation")
    
    ltv_col1, ltv_col2 = st.columns(2)
    
    with ltv_col1:
        avg_purchase = st.number_input(
            "Average Purchase Value ($)",
            min_value=0.0,
            value=50.0,
            help="Average amount a customer spends per transaction"
        )
        
        purchase_freq = st.number_input(
            "Annual Purchase Frequency",
            min_value=0.0,
            value=2.0,
            help="Number of times a customer purchases in a year"
        )
        
        use_churn = st.checkbox("Calculate lifespan using churn rate?")
        
        if use_churn:
            monthly_churn = st.number_input(
                "Monthly Churn Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=5.0
            ) / 100
            customer_lifespan = 1 / (monthly_churn * 12)  # Convert to years
        else:
            customer_lifespan = st.number_input(
                "Customer Lifespan (years)",
                min_value=0.0,
                value=3.0
            )
    
    # Calculate LTV
    ltv = avg_purchase * purchase_freq * customer_lifespan
    st.session_state.base_ltv = ltv
    
    with ltv_col2:
        st.metric("Calculated Lifetime Value (LTV)", f"${ltv:,.2f}")
        st.metric("Annual Revenue per Customer", f"${avg_purchase * purchase_freq:,.2f}")
        st.metric("Average Customer Lifespan", f"{customer_lifespan:.1f} years")
        
        # Section 2: CAC Calculator
with tab2:
    st.markdown("### 💰 Customer Acquisition Cost (CAC) Analysis")
    
    cac_col1, cac_col2 = st.columns(2)
    
    with cac_col1:
        st.markdown("#### Monthly Marketing Metrics")
        marketing_spend = st.number_input(
            "Total Monthly Marketing Spend ($)",
            min_value=0.0,
            value=5000.0,
            help="Include all marketing costs: ads, sales team, tools, etc."
        )
        
        new_customers = st.number_input(
            "New Customers Acquired This Month",
            min_value=0,
            value=50,
            help="Number of new customers acquired from your marketing efforts"
        )
        
        # Optional breakdown of marketing spend
        show_breakdown = st.checkbox("Show Marketing Spend Breakdown")
        if show_breakdown:
            st.markdown("#### Marketing Spend Breakdown")
            ad_spend = st.number_input("Ad Spend ($)", min_value=0.0, value=3000.0)
            team_cost = st.number_input("Sales/Marketing Team Cost ($)", min_value=0.0, value=1500.0)
            tool_cost = st.number_input("Marketing Tools/Software ($)", min_value=0.0, value=500.0)
            other_cost = marketing_spend - (ad_spend + team_cost + tool_cost)
            if other_cost < 0:
                st.warning("⚠️ Total breakdown exceeds total marketing spend!")
    
    # Calculate CAC
    cac = marketing_spend / new_customers if new_customers > 0 else 0
    st.session_state.base_cac = cac
    monthly_revenue = avg_purchase * purchase_freq / 12 if 'avg_purchase' in locals() and 'purchase_freq' in locals() else 0
    payback_period = cac / monthly_revenue if monthly_revenue > 0 else 0
    
    with cac_col2:
        st.markdown("#### Key Metrics")
        st.metric("Customer Acquisition Cost (CAC)", f"${cac:,.2f}")
        
        # Monthly metrics
        st.metric(
            "Monthly Revenue per Customer",
            f"${monthly_revenue:,.2f}",
            help="Average monthly revenue generated per customer"
        )
        
        # Payback period
        if payback_period > 0:
            if payback_period < 3:
                st.success(f"CAC Payback Period: {payback_period:.1f} months")
            elif payback_period < 6:
                st.info(f"CAC Payback Period: {payback_period:.1f} months")
            elif payback_period < 12:
                st.warning(f"CAC Payback Period: {payback_period:.1f} months")
            else:
                st.error(f"CAC Payback Period: {payback_period:.1f} months")
        
        # ROI calculation
        if cac > 0:
            monthly_roi = (monthly_revenue - (cac/12)) / (cac/12) * 100
            st.metric(
                "Monthly ROI",
                f"{monthly_roi:,.1f}%",
                help="Return on investment per month after CAC"
            )
        
        # Efficiency metrics
        if show_breakdown and marketing_spend > 0:
            st.markdown("#### Marketing Efficiency")
            st.metric("Cost per Dollar Acquired", f"${cac/monthly_revenue:.2f}" if monthly_revenue > 0 else "N/A")
            
            # Spend breakdown chart
            spend_data = {
                'Category': ['Ad Spend', 'Team Cost', 'Tools', 'Other'],
                'Amount': [ad_spend, team_cost, tool_cost, other_cost]
            }
            fig = px.pie(spend_data, values='Amount', names='Category', title='Marketing Spend Distribution')
            st.plotly_chart(fig, use_container_width=True)

        # Recommendations based on CAC metrics
        st.markdown("#### CAC Analysis")
        if cac > monthly_revenue * 3:
            st.error("⚠️ High CAC Alert: Your acquisition cost is too high relative to monthly revenue")
        elif cac > monthly_revenue * 2:
            st.warning("⚡ CAC Warning: Consider optimizing acquisition channels")
        else:
            st.success("✅ Healthy CAC: Good ratio of acquisition cost to revenue")
            # Section 3: Churn Analysis
with tab3:
    st.markdown("### 📉 Churn Rate Analysis")
    
    churn_col1, churn_col2 = st.columns(2)
    
    with churn_col1:
        churn_method = st.radio(
            "Churn Calculation Method",
            ["Lost Customers", "Start/End Comparison"]
        )
        
        if churn_method == "Lost Customers":
            start_customers = st.number_input(
                "Customers at Start of Month",
                min_value=0,
                value=1000
            )
            lost_customers = st.number_input(
                "Customers Lost During Month",
                min_value=0,
                value=50
            )
            churn_rate = lost_customers / start_customers if start_customers > 0 else 0
        else:
            start_customers = st.number_input(
                "Customers at Start of Month",
                min_value=0,
                value=1000
            )
            end_customers = st.number_input(
                "Customers at End of Month",
                min_value=0,
                value=950
            )
            churn_rate = (start_customers - end_customers) / start_customers if start_customers > 0 else 0
    
    with churn_col2:
        st.metric("Monthly Churn Rate", f"{churn_rate*100:.1f}%")
        st.metric("Annual Churn Rate", f"{(1 - (1-churn_rate)**12)*100:.1f}%")
        st.metric("Average Customer Lifespan", f"{1/(churn_rate*12):.1f} years" if churn_rate > 0 else "∞")

# Section 4: Granular Insights
with tab4:
    st.markdown("### 🔍 Detailed Business Insights")
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        has_segments = st.checkbox("Do you have different customer segments?")
        if has_segments:
            num_segments = st.number_input("Number of segments", min_value=1, max_value=5, value=2)
            segments_data = []
            for i in range(int(num_segments)):
                st.markdown(f"#### Segment {i+1}")
                segment_name = st.text_input(f"Segment {i+1} Name", value=f"Segment {i+1}")
                segment_value = st.number_input(f"{segment_name} Average Value", min_value=0.0)
                segment_percent = st.number_input(f"{segment_name} % of Customers", min_value=0.0, max_value=100.0)
                segments_data.append({
                    "Segment": segment_name,
                    "Value": segment_value,
                    "Percentage": segment_percent
                })
        
        retention_rate = st.number_input(
            "Repeat Purchase Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=40.0
        )
        
        upsell_rate = st.number_input(
            "Upsell/Cross-sell Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=20.0
        )
        
        referral_rate = st.number_input(
            "Referral Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0
        )
with insight_col2:
    st.markdown("### Key Insights")
    
    # Retention Analysis
    if retention_rate < 30:
        st.error("⚠️ Low retention rate - Focus on customer satisfaction and loyalty programs")
    elif retention_rate < 50:
        st.warning("📊 Average retention - Room for improvement")
    else:
        st.success("✅ Strong retention rate - Keep up the good work!")
    
    # Upsell Analysis
    if upsell_rate < 15:
        st.error("⚠️ Low upsell rate - Review your upsell strategy")
    elif upsell_rate < 25:
        st.warning("📊 Average upsell performance - Consider testing new offers")
    else:
        st.success("✅ Strong upsell performance - Continue optimizing")
    
    # Referral Analysis
    if referral_rate < 5:
        st.error("⚠️ Low referral rate - Implement a referral program")
    elif referral_rate < 15:
        st.warning("📊 Average referral rate - Enhance referral incentives")
    else:
        st.success("✅ Strong referral program - Maintain and scale")

# Section 5: Scenario Planning
with tab5:
    st.markdown("### 🎯 Scenario Planning")
    
    scenario_col1, scenario_col2 = st.columns(2)
    
    with scenario_col1:
        st.markdown("#### Adjust Metrics")
        
        purchase_value_change = st.slider(
            "Change in Average Purchase Value (%)",
            min_value=-50,
            max_value=100,
            value=0
        )
        
        cac_reduction = st.slider(
            "Change in CAC (%)",
            min_value=-50,
            max_value=50,
            value=0
        )
        
        retention_improvement = st.slider(
            "Change in Retention Rate (%)",
            min_value=-50,
            max_value=100,
            value=0
        )
    
    with scenario_col2:
        st.markdown("#### Impact Analysis")
        
        # Calculate scenario impacts
        new_ltv = st.session_state.base_ltv * (1 + purchase_value_change/100)
        new_cac = st.session_state.base_cac * (1 + cac_reduction/100)
        
        # Display metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "New LTV",
                f"${new_ltv:,.2f}",
                f"{purchase_value_change:+.1f}%"
            )
            st.metric(
                "New CAC",
                f"${new_cac:,.2f}",
                f"{cac_reduction:+.1f}%"
            )
        
        with col2:
            current_ratio = st.session_state.base_ltv / st.session_state.base_cac if st.session_state.base_cac > 0 else 0
            new_ratio = new_ltv / new_cac if new_cac > 0 else 0
            
            st.metric(
                "New LTV/CAC Ratio",
                f"{new_ratio:.2f}",
                f"{((new_ratio/current_ratio)-1)*100:+.1f}%" if current_ratio > 0 else "N/A"
            )

# Footer with recommendations
st.markdown("---")
st.markdown("### 📋 Advanced Recommendations")

if 'base_ltv' in st.session_state and 'base_cac' in st.session_state:
    ratio = st.session_state.base_ltv / st.session_state.base_cac if st.session_state.base_cac > 0 else 0
    
    # Create columns for different metric analyses
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown("#### Current Status")
        
         # LTV/CAC Analysis with Benchmarks
        st.markdown("##### Industry Benchmarks:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - 🔴 Below 1:1 - Critical
            - 🟡 1:1 to 3:1 - Needs Work
            - 🟢 3:1 to 5:1 - Healthy
            - 🌟 Above 5:1 - Excellent
            """)
        with col2:
            st.markdown("##### Your Current Ratio:")
            st.markdown(f"<h3 style='text-align: center;'>{int(ratio)}:1</h3>", unsafe_allow_html=True)
        
        # LTV/CAC Analysis with specific improvement suggestions
        if ratio < 1:
            st.error(f"⚠️ Critical LTV/CAC Ratio: {ratio:.2f}")
            st.markdown("""
            **Quick Wins to Improve Ratio:**
            - Increase average order value through bundles
            - Reduce ad spend on underperforming channels
            - Focus on higher-converting traffic sources
            """)
        elif ratio < 3:
            st.warning(f"⚡ Below Target LTV/CAC Ratio: {ratio:.2f}")
            st.markdown("""
            **Next Steps to Improve Ratio:**
            - Add upsell/cross-sell opportunities
            - Optimize marketing targeting
            - Implement a customer loyalty program
            """)
        elif ratio < 5:
            st.success(f"✅ Good LTV/CAC Ratio: {ratio:.2f}")
            st.markdown("""
            **Ways to Further Improve:**
            - Test premium pricing tiers
            - Expand successful marketing channels
            - Enhance customer experience
            """)
        else:
            st.success(f"🌟 Excellent LTV/CAC Ratio: {ratio:.2f}")
            st.markdown("""
            **Maintain Your Success:**
            - Scale winning strategies
            - Explore new market segments
            - Document best practices
            """)
    
    with rec_col2:
        st.markdown("#### Strategic Recommendations")
        
        # Comprehensive recommendations based on multiple metrics
        if ratio < 1:
            st.error("""
            ### Emergency Actions Required:
            1. 🛑 Pause non-performing marketing channels
            2. 📊 Analyze customer acquisition sources
            3. 💰 Review pricing strategy immediately
            4. 🎯 Focus on high-value customer segments
            5. 🔄 Optimize conversion funnel
            """)
        elif ratio < 3:
            st.warning("""
            ### Optimization Required:
            1. 📈 Increase average order value
               - Add upsells
               - Create product bundles
               - Implement tiered pricing
            2. 🔄 Reduce customer acquisition costs
               - Optimize ad targeting
               - Improve landing page conversion
               - Test different marketing channels
            3. 🤝 Enhance customer retention
               - Launch loyalty program
               - Improve onboarding
               - Implement feedback loops
            """)
        elif ratio < 5:
            st.success("""
            ### Growth Opportunities:
            1. 🚀 Scale successful channels
               - Increase ad spend on performing campaigns
               - Expand to similar audiences
            2. 📊 Optimize unit economics
               - Test premium offerings
               - Implement cross-sells
            3. 🌱 Explore new markets
               - Geographic expansion
               - New customer segments
            """)
        else:
            st.success("""
            ### Scaling Strategy:
            1. 🎯 Aggressive expansion
               - Significantly increase marketing budget
               - Enter new markets
               - Launch new products
            2. 🏢 Build infrastructure
               - Invest in automation
               - Strengthen team
               - Improve systems
            3. 🔄 Maintain efficiency
               - Monitor key metrics
               - Regular optimization
               - Build moats
            """)

# Help section
with st.expander("📘 How to Use This Calculator"):
    st.markdown("""
    1. Start with the LTV Calculator tab to understand your customer value
    2. Move to CAC Analysis to evaluate acquisition costs
    3. Analyze your Churn Rate to understand customer retention
    4. Review Detailed Insights for deeper understanding
    5. Use Scenario Planning to model potential improvements
    
    Target Metrics:
    - LTV/CAC Ratio > 3
    - Monthly Churn Rate < 5%
    - Retention Rate > 50%
    """)
