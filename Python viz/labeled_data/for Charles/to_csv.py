import pickle
import csv
import time
now =time.asctime()[4:-5]

with open(now+"_curls.csv","wb") as csvFile:
	data=pickle.load(open("shoulder_press.p"))
	writer=csv.writer(csvFile)
	writer.writerow(["t (sec)","x","y","z"]) #header
	for i in data:
		writer.writerow(list(i))