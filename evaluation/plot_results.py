import numpy as np
import matplotlib.pyplot as plt

labels = ['5%', '10%', '20%', '50%']
x = np.arange(len(labels))

LSBMR_error = [0.2089, 0.1518, 0.1023, 0.0236]
LoG_error = [0.3131, 0.2175, 0.1244, 0.0273]
Canny_error = [0.3497, 0.2453, 0.1405, 0.0327]
Sobel_error = [0.3667, 0.2509, 0.1367, 0.0312]
Canny_AND_LoG_error = [0.234, 0.1611, 0.1064, 0.024]
Canny_AND_Sobel_error = [0.2742, 0.1782, 0.1143, 0.0278]
Sobel_AND_LoG_error = [0.2395, 0.1637, 0.1071, 0.0245]
Canny_OR_LoG_error = [0.3703, 0.2804, 0.1714, 0.0389]
Sobel_OR_LoG_error = [0.3762, 0.2858, 0.1694, 0.0376]
Canny_OR_Sobel_error = [0.3995, 0.3021, 0.1771, 0.0399]

width = 0.08

r2 = [i + width for i in x]
r3 = [i + width for i in r2]
r4 = [i + width for i in r3]
r5 = [i + width for i in r4]
r6 = [i + width for i in r5]
r7 = [i + width for i in r6]
r8 = [i + width for i in r7]
r9 = [i + width for i in r8]
r10 = [i + width for i in r9]


fig, ax = plt.subplots()
rects1 = plt.bar(x, LSBMR_error, width, edgecolor='white', label='LSBMR')
rects2 = plt.bar(r2, LoG_error, width, edgecolor='white', label='LoG')
rects3 = plt.bar(r3, Canny_error, width, edgecolor='white', label='Canny')
rects4 = plt.bar(r4, Sobel_error, width, edgecolor='white', label='Sobel')
rects5 = plt.bar(r5, Canny_AND_LoG_error, width, edgecolor='white', label='Canny AND LoG')
rects6 = plt.bar(r6, Canny_AND_Sobel_error, width, edgecolor='white', label='Canny AND Sobel')
rects7 = plt.bar(r7, Sobel_AND_LoG_error, width, edgecolor='white', label='Sobel AND LoG')
rects8 = plt.bar(r8, Canny_OR_LoG_error, width, edgecolor='white', label='Canny OR LoG')
rects9 = plt.bar(r9, Sobel_OR_LoG_error, width, edgecolor='white', label='Sobel OR LoG')
rects10 = plt.bar(r10, Canny_OR_Sobel_error, width, edgecolor='white', label='Canny OR Sobel')

plt.xlabel('Embedding Rates', fontweight='bold')
plt.ylabel('Testing Error', fontweight='bold')
plt.title('Testing Error of edge schemes for four embedding rates')

plt.xticks([r + width + 0.28 for r in range(len(labels))], labels)
plt.legend()

fig.tight_layout()
plt.show()