import streamlit as st
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.stats import norm
import plotly.figure_factory as ff

#add ABA logo
st.image('https://upload.wikimedia.org/wikipedia/commons/7/7d/Abawikilogo.png', width=70)

st.title('Monte Carlo Simulation')
st.caption('Developed by Eugenio Gallastegui | Sr. Data Scientist')



#take user input
st.subheader('1. Enter the number of simulations')

#columns
col0, col01 = st.columns([3,3])
#number of simulations
n = col0.number_input('Number of simulations', min_value=1000, max_value=1000000, value=100000, step=10000)



#enter the average price of an ABA Membership
st.subheader('2. Enter the average price of an ABA Membership')
#columns 
col1, col2 = st.columns([4,1])
#take user input as a slider
avg_price = col1.slider('Average ABA Membership Price', min_value=75, max_value=750, value=250, step=10)
uncertainty_price = col2.number_input('Uncertainty %', min_value=0.0, max_value=1.0, value=0.34, step=0.01)
std_price = avg_price * uncertainty_price
st.caption(f'Average Price \$ {avg_price:,.0f} (+/- \$ {round(std_price,1):,.0f})')



#enter the expected total members
st.subheader('3. Enter the expected total ABA members')
#columns
col3, col4 = st.columns([4,1])
#take user input as a slider
avg_members = col3.slider('Expected Total ABA Members', min_value=10000, max_value=500000, value=160000, step=1000)
uncertainty_members = col4.number_input('Uncertainty % ', min_value=0.0, max_value=1.0, value=0.34, step=0.01)
std_members = avg_members * uncertainty_members
st.caption(f'Expected Total Members {avg_members:,.0f} (+/- {round(std_members,0):,.0f})')



#expected total revenue
avg_rev = avg_price * avg_members
avg_rev_std = avg_rev * 0.34
st.info(f'Expected Total Revenue \$ {avg_rev:,.0f}')



#enter annual budgeted expenses
st.subheader('4. Enter the annual budgeted expenses to create and deliver the ABA Membership VP')
#columns
col5, col6 = st.columns([4,1])
#take user input as a slider
expenses = col5.slider('Annual Budgeted Expenses', min_value=10000000, max_value=100000000, value=33000000, step=1000000)
uncertainty_expenses = col6.number_input('Uncertainty %  ', min_value=0.0, max_value=1.0, value=0.34, step=0.01)
std_expenses = expenses * uncertainty_expenses
st.caption(f'Annual Budgeted Expenses \$ {expenses:,.0f} (+/- \$ {round(std_expenses,0):,.0f})')



#generate random revenue numbers based on the average and standard deviation
revenue = np.random.normal(avg_rev, avg_rev_std, n)
#gegerate random expenses numbers based on the average and standard deviation
expense = np.random.normal(expenses, std_expenses, n)

#calculate the profit
profit = revenue - expense


# Calculate with 95% confidence the profit probability
profit_mean = np.mean(profit)
profit_std = np.std(profit)
confidence = 0.95
profit_conf = norm.interval(confidence, loc=profit_mean, scale=profit_std)

# Calculate the percentage of simulations in which profit is greater than 0
profit_positive = profit[profit > 0]
profit_positive_pct = len(profit_positive) / n




# Print the results
st.subheader('5. Simulation Results')

#if profit_prositve_pct >= 0.6, then st.success"
#if profit_prositve_pct >= 0.5 and profit_prositve_pct < 0.6, then st.warning"
#if profit_prositve_pct < 0.5, then st.error"
if profit_positive_pct >= 0.6:
    st.success(f'{profit_positive_pct:,.0%} of simulations resulted in a profit greater than $0 (the break-even point)')
elif profit_positive_pct >= 0.5 and profit_positive_pct < 0.6:
    st.warning(f'{profit_positive_pct:,.0%} of simulations resulted in a profit greater than $0 (the break-even point)')
else:
    st.error(f'{profit_positive_pct:,.0%} of simulations resulted in a profit greater than $0 (the break-even point)')

#if profit.mean() >= 1000000, then st.success"
#if profit.mean() >= 0 and profit.mean() < 1000000, then st.warning"
#if profit.mean() < 0, then st.error"
if profit.mean() >= 1000000:
    st.success(f'Given the inputs and levels of uncertainty, the most likely scenerio is ${profit.mean():,.0f}', icon="✔️")
elif profit.mean() >= 0 and profit.mean() < 1000000:
    st.warning(f'Given the inputs and levels of uncertainty, the most likely scenerio is ${profit.mean():,.0f}', icon="⚠️")
else:
    st.error(f'Given the inputs and levels of uncertainty, the most likely scenerio is ${profit.mean():,.0f}', icon="❌")

#display the 95% confidence interval
st.caption(f'Given the inputs provided, the margin of profit with 95% of confidence would range between \${profit_conf[0]:,.0f} and \${profit_conf[1]:,.0f}')

#plot the results adding a line at 0, the average profit and the 95% confidence interval
fig = ff.create_distplot([profit], ['Profit'], bin_size=10000, show_rug=False, show_hist=False, show_curve=True)
fig.add_vline(x=0, line_width=2, line_dash='solid' , line_color='red')
fig.add_vline(x=profit_mean, line_width=2, line_dash='solid', line_color='green')
fig.add_vline(x=profit_conf[0], line_width=1, line_dash='dash', line_color='blue')
fig.add_vline(x=profit_conf[1], line_width=1, line_dash='dash', line_color='blue')
st.plotly_chart(fig, use_container_width=True)


