import pandas as pd
import statsmodels.api as sm  #�����Ҫ��װ�������⣬import����

train = pd.read_csv("sample.csv")    #sample�ĸ�ʽ��target,view_num,buy_num�����Ǻõ�ѵ�������ǵõ�һ��һ��Ҫ�Ǳ���
train_cols = train.columns[1:]       #�Ե�һ���Ժ���У�����������Ϊѵ��������������view_num��buy_numΪѵ������
logit = sm.Logit(train['target'], train[train_cols]) #��ʾ�Ժ�������Ϊѵ��������target��Ϊ���ֵ�����߼��ع�
result = logit.fit()              #Ҫ�ǿ��ĵĻ�������result.summary()��һ�»ع���

combos = pd.read_csv("vectors.csv")   #vectors��δ��ǵ�����������Ҳ��������ҪԤ��ģ���ʽΪuid,bid,view_num,buy_num
train_cols = combos.columns[2:]
combos['prediction'] = result.predict(combos[train_cols])  #Ϊÿ����������Ԥ���֣��洢��һ���µ�prediction�У������ǵ�����

predicts = defaultdict(set)
for term in combos.values:
    uid, bid, prediction = str(int(term[0])), str(int(term[1])), term[4]
if prediction > POINT:      #����ͨ������POINT�Ĵ�С������������ĸ�������Ȼ��Ҳ����ȡ����topN
    predicts[uid].add(bid)