import matplotlib.pyplot as plt
import streamlit as st # Streamlit-a import panna maranthudatheenga

# 1. Figure-a create pannunga
fig, ax = plt.subplots()

# 2. Plotting logic-a ax (axis) use panni panunga
summary.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
ax.set_title('Expense vs Income Distribution')
ax.set_ylabel('') # Y-label-a remove panna

# 3. Streamlit-kku chart-a pass pannunga
st.pyplot(fig)