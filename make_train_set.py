import pandas as pd
import csv

f = open('train.tsv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f, delimiter='\t')

label = ["sentence1", "sentence2", "gold_label"]
wr.writerow(label)


wr.writerow(["안녕", "꺼져", "contradiction"])

f.close()

dataset = pd.read_csv("train.tsv", delimiter='\t', header=None)
print(dataset)