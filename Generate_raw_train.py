# -*- coding: cp936 -*-
import csv
import time
import re

cut_time   = '2014-12-05 23'
remove_time = '2014-12-12 23'

dir = 'D://TianChi//'
input_user_file = dir + 'tianchi_mobile_recommend_train_user.csv'
input_item_file = dir + 'tianchi_mobile_recommend_train_item.csv'
#input_user_file = dir + 'G2.csv'
#input_item_file = dir + 'G1.csv'
raw_train_file = dir + 'row_record.csv'
raw_buy_file = dir + 'buy_record.csv'
good_dic = {} # ��Ʒ�ʵ�

#����ʱ����ַ���Ϊ Сʱ
def TransferTime(TimeString) :
        if(re.match(r"time",TimeString)) :
                return -1;
        test_time_array = time.strptime(TimeString,"%Y-%m-%d %H")
        test_time_stamp = int(time.mktime(test_time_array))
        #0���ʱ����Ҫת������Ȼ�������
        days = int(test_time_stamp/(3600*24))
        if test_time_array[3] == 0 :
            return days + 1
        else :
            return days

def GenerateTrainTest() :
	#��Ʒ�Ӽ���ͳ��
	with open(input_item_file) as item_csv_file :
		item_reader = csv.DictReader(item_csv_file)
		for row in item_reader :
			good_dic[row['item_id']] = {'category': row['item_category'],'geohash': row['item_geohash']}
	
	#��ȡ����Ʒ�Ӽ�����
	writer = csv.writer(file(raw_train_file,'wb'))
	writer.writerow(['user_id','item_id','behaviro_type','user_geohash','item_geohash','item_category','time'])
	reader = csv.reader(open(input_user_file))
	for user_id, item_id, behaviro_type, user_geohash, item_category, time in reader:
	if good_dic.has_key(item_id) and (TransferTime(time) != TransferTime(remove_time)) :  #���Ҫ��ȡĳһ��ģ��ͼ���ʱ���ж�
			writer.writerow([user_id, item_id, behaviro_type, user_geohash, good_dic[item_id]['geohash'], item_category, time]) 

	return 1;

#��ȡĳһ��Ĺ����¼����dic�ķ�ʽ���أ�
def GetOneDayBuyData(ref_time) :
	#��Ʒ�Ӽ���ͳ��
	with open(input_item_file) as item_csv_file :
		item_reader = csv.DictReader(item_csv_file)
		for row in item_reader :
			good_dic[row['item_id']] = {'category': row['item_category'],'geohash': row['item_geohash']}

	#��ȡ����Ʒ�Ӽ�����
	writer = csv.writer(file(raw_train_file,'wb'))
	writer.writerow(['user_id','item_id','behaviro_type','user_geohash','item_geohash','item_category','time'])
	reader = csv.reader(open(input_user_file))
	for user_id, item_id, behaviro_type, user_geohash, item_category, time in reader:
	if good_dic.has_key(item_id) and (TransferTime(time) != TransferTime(remove_time)) :  #���Ҫ��ȡĳһ��ģ��ͼ���ʱ���ж�
			writer.writerow([user_id, item_id, behaviro_type, user_geohash, good_dic[item_id]['geohash'], item_category, time]) 

	return 1;

if __name__ == '__main__' :
        GenerateTrainTest()
        print "row record generate ok"
