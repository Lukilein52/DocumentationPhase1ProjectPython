import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# Bar Chart
months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul']
ects = [5, 15, 0, 20, 10, 5, 5]
bar_colors = ['tab:red', 'tab:red', 'tab:red', 'tab:red', 'tab:red', 'tab:red', 'tab:red']
ax.bar(months, ects, color = bar_colors)
ax.set_ylabel('ECTS')
ax.set_title('ECTS pro Monat')

plt.show()

# Ring Chart
