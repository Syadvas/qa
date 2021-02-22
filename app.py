import json
from flask import Flask, request
import pandas as pd
import datetime
import re


app = Flask(__name__)

with open('questions.json','r') as fl:
    a = json.loads(fl.read())
    q_pt = a['tags']

def cleaner(x):
    try:
        if len(x.split()) == 1:
            return re.sub('[^a-zA-Z0-9 \']+',' ',x)
        # to check single repetative occurances
        x = x.lower()
        x = re.sub('[^a-zA-Z0-9 ]+',' ',x)
        x = x.split()
        sent = []
        for word in x:
            try:
                if sent[-1] != word:
                    sent.append(word)
            except:
                sent.append(word)
        x = ' '.join(sent)
        # to check double repetative occurances
        y = re.findall("[\S]+ [\S]+",x)

        a = []
        for i in y:
            try:
                if i!=a[-1]:
                    a.append(i)
            except Exception as e:
                a.append(i)
                print(e)
        if x.split()[-1] not in y[-1].split()[-1]:
            a.append(x.split()[-1])

        # to check double occurances
        x = x.split()
        firstword = x[0]
        x = x[1:]
        x = ' '.join(x)
        y = re.findall("[\S]+ [\S]+",x)

        b = []
        for i in y:
            try:
                if i!=b[-1]:
                    b.append(i)
            except Exception as e:
                b.append(i)
                print(e)
        if x.split()[-1] not in y[-1].split()[-1]:
            b.append(x.split()[-1])
        b = [firstword] +b

        a = ' '.join(a)
        b = ' '.join(b)

        a_u = list(pd.Series(a.split()).unique())
        a_u.sort()

        b
        b_u = list(pd.Series(b.split()).unique())
        b_u.sort()

        lenArray = [len(a),len(b)]
        ind = lenArray.index(min(lenArray))
        if ind == 0:
            return a
        else:
            return b
    except Exception as e:
        print(e)
        return None


def qfinder(x):
    for i in q_pt:
        if i in x:
            return True
    return False

@app.route('/webhook', methods = ['POST'])
def webhook():
    req = request.get_json(silent=True,force=True)
    req = req.get('statements')
    print(req)
    df = pd.DataFrame(req,columns=['statement'])
    df.statement = df.statement.map(cleaner)
    df['question'] = df.statement.map(qfinder)
    a = df.to_json()
    return str(a)

if __name__ == '__main__':
    app.run()