import pandas as pd
import matplotlib.pyplot as plt

data= pd.read_csv("Tabella_Affluenza_Comma.csv")
#print(ds)

plt.rcParams["figure.figsize"] = (10,5)

df=pd.DataFrame(data)
groups = ['1996','1998','2000','2002','2004','2006','2008', '2010','2012','2014','2016','2018', '2020','2022','2024']

#15 values
X= list(df.iloc[:,1])
X.reverse()
Y= list(df.iloc[:,2])
Y.reverse()

fig, ax = plt.subplots()
ax.bar(groups, X,label="Students who didn't vote")
ax.bar(groups, Y,label="Students who did vote")
ax.legend()

ax.set_title("Student Participation in the Election" )
ax.set_ylabel("Total students who cold vote")

plt.show()



