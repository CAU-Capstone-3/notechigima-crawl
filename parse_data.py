import csv
import hashlib
import re

# f_target_name = 'words.tsv'
f_target_name = 'words_exclude_q.tsv'

f_target = open(f_target_name, 'w', encoding='utf-8', newline='')
wr = csv.writer(f_target, delimiter='\t')
wr.writerow(['sentence'])

base_dir = 'raw_data/'

sentence_set = set()
sentence_list = []

def run_parser(exclude_question):

    for i in range(1, 329):
        f_name = base_dir + 'data%d.txt'%i
        f_from = open(f_name, mode='r', encoding='utf-8')
        print('processing: ' + f_name)

        while True:
            line = f_from.readline()
            if not line:
                break

            line = line.replace('\t', '')
            
            reg_exclude = False
            if exclude_question:
                reg_exclude = re.search('.[?]', line)

            if (not re.search('[ㄱ-힣]', line)) or reg_exclude:
                continue

            line = re.sub('[0-9]+[.]|①|②|③|④|❶|❷|❸|❹', '', line)
            line = line.lstrip().rstrip()
                
            if not (line in sentence_set):
                sentence_set.add(line)
                sentence_list.append(line)            
        
        f_from.close()

    line_num = 1
    for row in sentence_list:
        wr.writerow([row])
        print('#%d\t'%line_num + row)
        line_num += 1

    print('>> write complete: %s'%f_target_name)
    f_target.close()

run_parser(exclude_question=True)

