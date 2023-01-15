import matplotlib.pyplot as plt
import json

data = json.loads(open('balance.json').read())

x_axis = []
y_axis = []
for k, v in data.items():
    x_axis.append(k)
    y_axis.append(float(v))

plt.plot(x_axis, y_axis)
plt.title('Balance graph')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Balance')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--')
plt.subplots_adjust(bottom=0.3)
plt.show()