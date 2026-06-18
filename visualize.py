import matplotlib.pyplot as plt

# Visualization: Pie Chart for Debit vs Credit
summary.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
plt.title('Expense vs Income Distribution')
plt.ylabel('') # Remove y-label
plt.show()