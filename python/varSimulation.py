import numpy as np
import matplotlib.pyplot as plt

zeros = 0
moneys = []
for trial in range(20000):
    money = 1
    for day in range(40):
        if money < 0:
            zeros += 1
            break
        money *= 1.0008
        added = np.random.normal(0, .3*money)
        money += added
    moneys.append(money)

print(np.std(moneys))
print(np.mean(moneys))
print(zeros)

plt.hist(moneys, bins = 100, range=(0, 4))

plt.show()



#new companies and first or second eanings