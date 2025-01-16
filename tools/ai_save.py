import numpy as np
from sklearn.decomposition import PCA
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import joblib

data = []
ai_answer =[]
with open("ai_data/first_ai.txt","r",encoding="utf-8") as f:
    ai_data_ = []
    for line in f:
        line = line.rstrip()
        tmp = line.split()
        for i in range(len(tmp)):
            tmp[i] = float(tmp[i])
        ai_data_.append([])

        pl_ = int(tmp[0])
        tmp_len_ = len(tmp)
        tmp_len = len(ai_data_)
        ai_data_[tmp_len - 1].append([0,0,pl_])
        for i in range(pl_):
            ai_data_[tmp_len - 1].append(tmp[1+i*3:1+(i+1)*3])
        for i in range(4-pl_):
            ai_data_[tmp_len - 1].append([0,0,0])
        en_ = int(tmp[int(tmp[0])*3+1])
        ai_data_[tmp_len - 1].append([0,0,en_])
        for i in range(en_):
            tm = [0,tmp[(int(tmp[0])*3+2)+i*2],tmp[(int(tmp[0])*3+2)+i*2+1]]
            ai_data_[tmp_len - 1].append(tm)
        for i in range(4-en_):
            ai_data_[tmp_len - 1].append([0,0,0])
        c = tmp[tmp_len_ - 3]
        c = [0,0,c]
        ai_data_[tmp_len - 1].append(c)
        d = tmp[tmp_len_ - 2:tmp_len_]
        nd_ = np.array([])
        ai_data_[tmp_len - 1] = np.append(nd_,ai_data_[tmp_len-1]).tolist()
        ai_answer.append(d)

data = np.array(ai_data_)
data_answer = np.array(ai_answer)

pca = PCA(n_components = 20, whiten = False)
pca.fit(data)
data = pca.fit_transform(data)
scaler = StandardScaler()
data = scaler.fit_transform(data)


clf = MultiOutputRegressor(MLPClassifier(alpha=0.00001, hidden_layer_sizes=(400,200,100,50),max_iter=1000,random_state=0,early_stopping=True))
clf.fit(data , data_answer)

joblib.dump(clf, "rpg.aibi",compress=3)