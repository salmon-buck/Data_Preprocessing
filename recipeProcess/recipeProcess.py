import re
import nltk
import os
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from openpyxl import Workbook
wordnet_lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer('english')

def preProcessing(example):
    letters_only = re.sub('[^a-zA-Z]', ' ', example)
    lower_case = letters_only.lower()
    words = lower_case.split()
    words = [w for w in words if not w in stopwords.words('english')]
    words = [stemmer.stem(w) for w in words]
    words = [wordnet_lemmatizer.lemmatize(w) for w in words]
    return words

f = open('recipe.txt', 'rt', encoding='UTF8')
list = []

for i in range(100):
    line = f.readline()
    lines = line.split(';')
    # print(i)

    description = preProcessing(lines[2])
    ingredient = preProcessing(lines[4])

    lines[2] = ",".join(description)
    lines[4] = ",".join(ingredient)

    filename = str(lines[1]) + ".txt"

    list.append(filename)

    # print(filename)
    if os.path.isfile(filename):
        df = open(filename, 'rt', encoding='UTF8')
        des = ""
        for j in range(2):
            des = df.readline()
        lines[2] = lines[2] + "," + des[:-1]
        df.close()

    nf = open(filename, 'wt', encoding='UTF8')

    for j in range(1, len(lines)):
        nf.writelines(lines[j])
        nf.write('\n')
    nf.close()

f.close()

f = open('recipe.txt', 'rt', encoding='UTF8')
list = []
db = {}
for i in range(100):
    dic = {}
    line = f.readline()
    lines = line.split(';')
    # print(i)

    rname = lines[1]
    rname = str.strip(rname)
    description = preProcessing(lines[2])
    ingredient = preProcessing(lines[4])

    dic['name'] = rname
    dic['description'] = ' '.join(description)
    dic['country'] = str.strip(lines[3])
    dic['ingredient'] = ' '.join(ingredient)
    dic['recipe'] = str.strip(lines[5])
    dic['time'] = str.strip(lines[6])
    dic['ImageUrl'] = str.strip(lines[7])
    db[rname] = dic
f.close()

print(db.keys())

write_wb = Workbook()                                                           # workbook 생성
sheets=[]                                                                       # sheet 이름 저장해놓는 sheets
                                                            # 디폴트로 생성되는 sheet1이 있기때문에 이름을 filenames[0] 의 이름으로 바꾼다
s=write_wb.active
s.title='DB'

db=sorted(db.items(), key=lambda x : x[1]['country'])
count=1
for word in db :                                          # 엑셀 채워넣기
    s.cell(count, 1, word[1]['name'])                                     # 1열 : 단어
    s.cell(count, 2, word[1]['description'])                           # 2열 : term frequency(tf)
    s.cell(count, 3, word[1]['country'])                                # 3열 : document frequency(df)
    s.cell(count, 4, word[1]['ingredient'])                          # 4열 : weight (tf-idf)
    s.cell(count, 5, word[1]['recipe'])
    s.cell(count, 6, word[1]['time'])
    s.cell(count, 7, word[1]['ImageUrl'])
    count+=1

write_wb.save('DB.xlsx')     # 엑셀파일에 저장
