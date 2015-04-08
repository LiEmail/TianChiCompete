import csv
import time
print time.time()

#����ģ��
start_time = '2014-11-13 00'
cut_time = '2014-12-18 00'
test_time = '2014-12-19 00'
#input_user_file = 'E:\\���_�ƶ��Ƽ�\\tianchi_mobile_recommend_train_user.csv'
#input_item_file = 'E:\\���_�ƶ��Ƽ�\\tianchi_mobile_recommend_train_item.csv'
input_user_file = 'E:\\���_�ƶ��Ƽ�\\G2.csv'
input_item_file = 'E:\\���_�ƶ��Ƽ�\\G1.csv'
output_train_file = 'E:\\���_�ƶ��Ƽ�\\TrainSet.csv'
output_ref_file = 'E:\\���_�ƶ��Ƽ�\\RefSet.csv'
train_title  = ['target','feature1','feature2','feature3'] #trainSet��title row
Predict_title  = ['user_id','item_id','feature1','feature2','feature3'] #PredictSet��title row
days_feature = (3, 7, 15)  #ǰ3, 7, 15�������
days_featureName = ("Sales_3","Sales_7","Sales_15")
behavior = ("","click","store","shopcar","buy") 	#�û���Ϊ��title
user_feature  = ("active_day","buy_sum","buy_day")  #�û�������title
ratio = 10 # �ٷֱ��͵�������һ���Ĳ���
#########################################################################################

start_time_stamp = TransferTime(start_time)
cut_time_stamp   = TransferTime(cut_time)
test_time_stamp  = TransferTime(test_time)
total_day = float(cut_time_stamp - start_time_stamp)

user_dic = {}  #�û���Ʒ�ʵ�
good_dic = {}  #��Ʒͳ�ƴʵ�  
user_item_dic = {}  #�û�-Ʒ�ƴʵ�
use_item_result = Set() # �û�-��Ʒ�������(������)
test_user_dic = {}

#ʱ���ת����Сʱ��
def TransferTime(Time) :
	Time_array = time.strptime(Time,"%Y-%m-%d %H")
	Time_stamp = int(time.mktime(Time_array))
	Time_stamp = int(Time_stamp/(3600*24))
	return Time_stamp
	
#�γ� userid_itemid��������ƥ��target
def AppendString(user_id, item_id) :
    s = []
    s.append(user_id)
    s.append('-')
    s.append(item_id)
    item = ''.join(s)
    return item

def GenerateFeature(Title) :
	#��Ʒ��Ϣ��ͳ��
	with open(input_item_file) as item_csv_file:
		item_reader = csv.DictReader(item_csv_file)
		for item_row in item_reader
			good_dic[row['item_id']] = {'category': row['item_category'],\
										'geohash': row['item_geohash'],\
										behavior[1]: 0,\
										behavior[2]: 0,\
										behavior[3]: 0,\
										behavior[4]: 0,\
										days_featureName[0]: 0,\
										days_featureName[1]: 0,\
										days_featureName[2]: 0\
										}
	#�û� && �û�-Ʒ�� ��Ϣ��ͳ��
	with open(input_user_file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			user_id = row['user_id']
			item_id = row['item_id']
			behavior_type = behavior[row['behavior_type']]
			b_time = TransferTime(row['time'])
			item_category = row['item_category']
			
			if b_time <= cut_time_stamp :  # ʱ��ָ��֮ǰ�Ĳż���trainSet
				
				#������Ʒͳ�ƴʵ䣨ֻͳ�Ƴ��ֹ�����Ʒ/δ������Ʒ��ʱ���˵���
				if good_dic.has_key(item_id) == True :
					one_good = good_dic[item_id]
					# ������Ϊ
					one_good[behavior[behavior_type]] = one_good[behavior[behavior_type]] + 1
					# ���»𱬳̶�
					if b_time - cut_time_stamp >= days_feature[0] :
						one_good[days_featureName[0]] = one_good[days_featureName[0]] + 1
						one_good[days_featureName[1]] = one_good[days_featureName[1]] + 1
						one_good[days_featureName[2]] = one_good[days_featureName[2]] + 1
					else if b_time - cut_time_stamp >= days_feature[1] :
						one_good[days_featureName[1]] = one_good[days_featureName[1]] + 1
						one_good[days_featureName[2]] = one_good[days_featureName[2]] + 1
					else if b_time - cut_time_stamp >= days_feature[2] :
						one_good[days_featureName[2]] = one_good[days_featureName[2]] + 1
				
				#�����û�ͳ�ƴʵ�
				if user_dic.has_key(user_id) == False :  #��������ڼ�ֵ���ȴ���һ����ֵ
					user_dic[user_id] = { behavior[1]: 0,\
										  behavior[2]: 0,\
										  behavior[3]: 0,\
										  behavior[4]: 0,\
  										  AppendString(behavior[1], 'days'): Set(),\
										  AppendString(behavior[2], 'days'): Set(),\
										  AppendString(behavior[3], 'days'): Set(),\
										  AppendString(behavior[4], 'days'): Set()
										}
				one_user = user_dic[user_id]
				one_user[behavior[behavior_type]] = one_good[behavior[behavior_type]] + 1  	#������Ϊ
				one_user[AppendString(behavior[behavior_type],'days')].add(b_time)			#���»�Ծ��		
				if behavior_type == 4 :
					use_item_result.add(AppendItems(user_id, item_id))
											  
				#�����û�-Ʒ������ ���ȴ���ӣ�
				'''
				if one_user_one_good.has_key(behavior_type) == True:
					one_user_one_good_one_behavior = one_user_one_good[behavior_type]
					one_user_one_good_one_behavior = one_user_one_good_one_behavior + [b_time]
				else:
					one_user_one_good[behavior_type] = [b_time]
				else:
					one_user[item_id] = {behavior_type:[b_time]}
				
				if test_user_dic.has_key(user_id) == True:
					good = test_user_dic[user_id]
					if good.has_key(item_id) != True:
						good[item_id] = 1
				else:
					test_user_dic[user_id] = {item_id:1}
				'''
	csvfile.close()
	print "read ok"

	#������ȡ
	writer = csv.writer(file(output_train_file,'wb'))
	writer.writerows(Title)
	for user in user_dic.keys() : 	#���ڿ����޳� �������˻�����ʱ��ȫ���û���		
		for good in good_dic.keys() :
			target = 0
			if AppendString(user, good) in user_behavior :
				target = 1
			
			good_feature = good_dic[good]
			user_feature = user_dic[user]
			
			good_f1	= good_feature[behavior[4]]
			good_f2	= good_feature[behavior[3]]
			good_f3	= good_feature[days_featureName[0]]
			good_f4 = good_feature[days_featureName[1]]
			user_f1 = len(user_feature[AppendItems(behavior[4], 'days')]) * 1.0 * ratio / (cut_time - start_time)  
			user_f2 = user_feature[behavior[4]] * 1.0 * ratio /( user_feature[behavior[1]] + user_feature[behavior[2]] + user_feature[behavior[3]] + user_feature[behavior[4]] )
			
			if Title[0] == 'target' : 
				writer.writerows([target, good_f1, good_f2, good_f3, good_f4, \
							  user_f1, user_f2])
			else if Title[0] == 'user_id'
				writer.writerows([good, user, good_f1, good_f2, good_f3, good_f4, \
							  user_f1, user_f2])
	csvfile.close()
	print '��ȡ���'
	return
	
if __name__ == '__main__' :
	GenerateFeature(train_title)
	#GenerateFeature(Predict_title)
