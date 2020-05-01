import matplotlib.pyplot as plt

a0 = [6, 6, 7, 7]
a1 = [8, 10, 4]
a2 = [1, 2, 2, 3, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2]
a3 = [2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 2]
a4 = [2, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2]
a5 = [5, 5, 5, 5, 6]
a6 = [10, 14]
a7 = [14, 3]
a8 = [9, 8, 8]
a9 = [2, 3, 3, 3, 2, 3, 3, 2, 4, 2]

fig, ax = plt.subplots()
ax.plot([i for i in range(len(a0))], a0, label='a0')
ax.plot([i for i in range(len(a1))], a1, label='a1')
ax.plot([i for i in range(len(a2))], a2, label='a2')
ax.plot([i for i in range(len(a3))], a3, label='a3')
ax.plot([i for i in range(len(a4))], a4, label='a4')
ax.plot([i for i in range(len(a5))], a5, label='a5')
ax.plot([i for i in range(len(a6))], a6, label='a6')
ax.plot([i for i in range(len(a7))], a7, label='a7')
ax.plot([i for i in range(len(a8))], a8, label='a8')
ax.plot([i for i in range(len(a9))], a9, label='a9')

plt.show()
