import pandas as pd
from collections import defaultdict
import statsmodels.api as sm

train = pd.read_csv("FeatureData.csv")    #FeatureData�ĸ�ʽ��target,feature1,feature2,... �����Ǻõ�ѵ��������һ���Ǳ���
train_cols = train.columns[1:]       #��һ���Ƿ���label��������о���ѵ������

logit = sm.Logit(train['target'], train[train_cols]) #��ʾ�Ժ�������Ϊѵ��������target��Ϊ���ֵ�����߼��ع�
result = logit.fit()              #Ҫ�ǿ��ĵĻ�������result.summary()��һ�»ع���

combos = pd.read_csv("vectors.csv")   #vectors��δ��ǵ�����������Ҳ��������ҪԤ��ģ���ʽΪuid,bid,view_num,buy_num
train_cols = combos.columns[2:]       #ǰ������uid-bid������Ĳ�����������
combos['prediction'] = result.predict(combos[train_cols])  #Ϊÿ����������Ԥ���֣��洢��һ���µ�prediction�У������ǵ�����

writer = csv.writer(file('predict_result.csv','wb'))
writer.writerow(['user_id','item_id'])
for term in combos.values:
    uid, bid, prediction = str(int(term[0])), str(int(term[1])), term[4]
if prediction > POINT:      #����ͨ������POINT�Ĵ�С������������ĸ�������Ȼ��Ҳ����ȡ����topN
    writer.writerow([uid,pid]) #���������µ�csv����
