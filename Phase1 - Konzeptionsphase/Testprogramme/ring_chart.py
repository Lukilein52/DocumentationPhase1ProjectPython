import matplotlib.pyplot as plt
fig, ax = plt.subplots()

ects = [50, 130]

ax.pie(ects, radius=1.0,
       colors=['#ff0000', '#000'],
       startangle=90,
       wedgeprops=dict(width=0.4, edgecolor='white'))

plt.show()