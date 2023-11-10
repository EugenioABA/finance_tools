import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator
import numpy as np

st.set_option('deprecation.showPyplotGlobalUse', False)

#add ABA logo
st.image('https://upload.wikimedia.org/wikipedia/commons/7/7d/Abawikilogo.png', width=70)

st.title("Price Elasticity of Demand")
st.caption('Developed by Eugenio Gallastegui')

#subheader
st.subheader("1. Enter the previous membership price and demand")

#columns
col1, col2 = st.columns([1,1])

# price of good
price_1 = col1.number_input("Enter previous membership price: $", value=50, step=10)
    # quantity of good
quantity_1 = col2.number_input("Enter previous membership demand: ", value=3454, step=500)
    #revenue 1
revenue_1 = price_1 * quantity_1

#subheader
st.subheader("2. Enter the current membership price and demand")

#columns
col3, col4 = st.columns([1,1])

    # new price of good
price_2 = col3.number_input("Enter current membership price: $", value=75, step=10)
    # new quantity of good
quantity_2 = col4.number_input("Enter current membership demand: ", value=3316, step=500)
    #revenue 2
revenue_2 = price_2 * quantity_2
    # calculate percentage change in price
price_change = (price_2 - price_1) / price_1
    # calculate percentage change in quantity
quantity_change = (quantity_2 - quantity_1) / quantity_1
    # calculate price elasticity of demand
price_elasticity = quantity_change / price_change


#subheader
st.subheader("3. Results")

    # print price elasticity of demand
st.info(f"Price elasticity of demand: {round(price_elasticity,1)}. Meaning that for each 1% the prices changes, the demand will change by {round(price_elasticity, 1)}.")

st.info(f"When price changes by {round(price_change * 100,0):,.0f}%, the demand changes by {round(quantity_change * 100,0):,.0f}%.")

#columns
col5, col6 = st.columns([1,1])
col7, col8 = st.columns([1,1])

col5.info(f"Revenue under previous price model was ${revenue_1:,.0f}")

if revenue_2 > revenue_1:
    col7.success(f"Revenue under the new price model was ${revenue_2:,.0f}")
else:
    col7.error(f"Revenue under the new price model was ${revenue_2:,.0f}")

#revenue change
revenue_change = revenue_2 - revenue_1
#revenue change percentage
revenue_change_percentage = ((revenue_2 - revenue_1) / revenue_1) * 100

col8.metric(label="Revenue Change", value=f"${revenue_change:,.0f}", delta=f"{revenue_change_percentage:,.1f}%", delta_color="normal")


 #now plot the curve of price elasticity of demand
x = [price_1, price_2] # create a list of the x values
y = [quantity_1, quantity_2] # create a list of the y values

x_min, x_max = min(x) - 0.15 * min(x), max(x) + 1.5 * max(x) # add 15% to the max and min values and use that as the range for the x axis
y_min, y_max = min(y) - 0.15 * min(y), max(y) + 1.5 * max(y) # add 15% to the max and min values and use that as the range for the y axis
plt.rcParams["figure.figsize"] = (10,10) # set the size of the plot in inches
#plt.figure(figsize=(14, 20))
plt.plot(x, y) # plot the line
plt.plot(price_1, quantity_1, 'ro') # plot the points for the old price and quantity
plt.plot(price_2, quantity_2, 'ro') # plot the points for the new price and quantity
plt.plot([price_1, price_1], [y_min, quantity_1], 'r--') # plot the dashed lines for the old price and quantity
plt.plot([x_min, price_1], [quantity_1, quantity_1], 'r--') # plot the dashed linnes to connect the old price and quantity
plt.plot([price_2, price_2], [y_min, quantity_2], 'r--') # plot the dashed lines for the new price and quantity
plt.plot([x_min, price_2], [quantity_2, quantity_2], 'r--') # plot the dashed linnes to connect the new price and quantity
plt.text(price_1, quantity_1, f"(${price_1:,.0f}, {quantity_1:,.0f})") # add the text for the old price and quantity at the point
plt.text(price_2, quantity_2, f"(${price_2:,.0f}, {quantity_2:,.0f})") # add the text for the new price and quantity at the point
plt.text(price_1, y_min, f"Price: ${price_1:,.0f}") # add the text for the old price on the x axis
plt.text(x_min, quantity_1, f"Demand: {quantity_1:,.0f}") # add the text for the old quantity on the y axis
plt.text(price_2, y_min, f"Price: ${price_2:,.0f}") # add the text for the new price on the x axis
plt.text(x_min, quantity_2, f"Demand: {quantity_2:,.0f}") # add the text for the new quantity on the y axis
plt.xlabel("Membership Price ($)", fontsize=16) # add the x axis label
plt.ylabel("Membership Demand", fontsize=16) # add the y axis label
plt.title("Price Elasticity of Demand", fontsize=20) # add the title # show the plot
st.pyplot() # show the plot in streamlit


####################################################################################################################################
####    Curves
####################################################################################################################################

# Calculate the price elasticity of demand
price_elasticity_of_demand = (quantity_2 - quantity_1) / ((quantity_2 + quantity_1) / 2) / (price_2 - price_1) * (price_2 + price_1) / 2

# Calculate the slope and intercept of the demand line
slope = (quantity_2 - quantity_1) / (price_2 - price_1)
intercept = quantity_1 - (slope * price_1)

# Calculate the price at which revenue is maximized
optimal_price = -intercept / (2 * slope)

# Generate prices from 0 to just beyond the price that gives zero demand
max_price_for_demand = -intercept / slope
extended_prices = np.linspace(0, max_price_for_demand, 1000)

# Calculate the demand and revenue for the extended price range
extended_demands = slope * extended_prices + intercept
extended_revenues = extended_prices * extended_demands

# Plot the demand and revenue curves
plt.figure(figsize=(14, 20))

# Demand curve plot
ax1 = plt.subplot(2, 1, 1)
ax1.plot(extended_prices, extended_demands, label='Demand Curve')
ax1.scatter([price_1, price_2], [quantity_1, quantity_2], color='red', zorder=5)
ax1.axvline(x=optimal_price, color='red', linestyle='--')
ax1.axvline(x=price_1, color='grey', linestyle='--')
ax1.axvline(x=price_2, color='grey', linestyle='--')
ax1.text(price_1, quantity_1, f'  Q1 = {quantity_1}', verticalalignment='bottom', horizontalalignment='right')
ax1.text(price_2, quantity_2, f'  Q2 = {quantity_2}', verticalalignment='bottom', horizontalalignment='right')
ax1.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=15))
ax1.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=15))
ax1.set_title('Demand Curve', fontsize=24)
ax1.set_xlabel('Price', fontsize=16)
ax1.set_ylabel('Quantity Demanded', fontsize=16)
ax1.grid(True)
ax1.legend()

# Revenue curve plot
ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.plot(extended_prices, extended_revenues, label='Revenue Curve', color='green')
ax2.scatter([price_1, price_2, optimal_price], [price_1 * quantity_1, price_2 * quantity_2, optimal_price * (slope * optimal_price + intercept)], color='red', zorder=5)
ax2.axvline(x=optimal_price, color='red', linestyle='--')
ax2.axvline(x=price_1, color='grey', linestyle='--')
ax2.axvline(x=price_2, color='grey', linestyle='--')
ax2.text(price_1, price_1 * quantity_1, f'  TR1 = ${price_1 * quantity_1:.2f}', verticalalignment='bottom', horizontalalignment='right')
ax2.text(price_2, price_2 * quantity_2, f'  TR2 = ${price_2 * quantity_2:.2f}', verticalalignment='bottom', horizontalalignment='right')
ax2.text(optimal_price, optimal_price * (slope * optimal_price + intercept), f'  Max TR = ${optimal_price * (slope * optimal_price + intercept):.2f}', verticalalignment='bottom', horizontalalignment='left')
ax2.get_yaxis().set_major_formatter(FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
ax2.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=15))
ax2.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=15))
ax2.set_title('Revenue Curve', fontsize=24)
ax2.set_xlabel('Price', fontsize=16)
ax2.set_ylabel('Total Revenue', fontsize=16)
ax2.grid(True)
ax2.legend()

plt.tight_layout()
#plt.show()
st.pyplot()

# Output the calculated values
st.info(f"Price Elasticity of Demand: {price_elasticity_of_demand}")
st.info(f"Slope: {slope}")
st.info(f"Intercept: {intercept}")

