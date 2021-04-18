# refference https://matplotlib.org/3.1.1/gallery/pie_and_polar_charts/pie_features.html
import matplotlib.pyplot as plt
import pandas

pan = pandas.read_csv('tweet_NLP_2.csv')
labels = []
sizes = []
for i,j in zip(pan['word'],pan['number']):
    labels.append(i)
    sizes.append(j)
fig1, ax1 = plt.subplots()

ax1.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
ax1.axis('equal')
ax1.figure.savefig('C:/Users/Lenovo/Desktop/New folder/abc.png')
#sentiment.setStyleSheet('border-image:url(C:/Users/Lenovo/Desktop/New folder/abc.png);')

plt.show()