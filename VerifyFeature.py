# -*- coding: cp936 -*-
import csv
import time

dir = 'D:\\TianChi\\'
cut_day = '2014-12-18'
feature_day = ['20141217','20141216','20141215']
input_file_result_file = dir + 'sold_result\\'+cut_day+'result.csv'
#input_user_file = dir + 'tianchi_mobile_recommend_train_user.csv'
input_user_file = dir + 'row_record.csv'

#ʱ���ת��������
def date2hours(date):
    test_time_array = time.strptime(date,'%Y-%m-%d %H')
    hours_i = int((time.mktime(test_time_array))/(3600))
    return hours_i
    #days_f = float((time.mktime(test_time_array))/(3600)
    #if(days_f - days_i) > 0.66 : 
    #    return days_i + 1
    #else:
    #    return days_i
	
#�γ� userid_itemid��������ƥ��target
def AppendUseItemString(user_id, item_id) :
    s = []
    s.append(user_id)
    s.append('-')
    s.append(item_id)
    item = ''.join(s)
    return item

def GetDupRatio() :
	#�õ������ �û�-��Ʒ��
	buy_user_item_dic = set() #�����¼
	with open(input_file_result_file) as csvfile : 
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	       if	AppendUseItemString(row['user_id'],row['item_id']) in buy_user_item_dic :
	           continue
	       else :
	           buy_user_item_dic.add(AppendUseItemString(row['user_id'],row['item_id']))
	
	#ͳ��3��֮�ڣ���6СʱΪ��������
	user_item_dic = set ()
	dup_item_dic = set ()
	with open(input_user_file) as csvfile : 
	    reader = csv.DictReader(csvfile)
	    for row in reader : 
	        index = AppendUseItemString(row['user_id'],row['item_id'])
	        if index in buy_user_item_dic : 
	               if index in buy_user_item_dic : 
	                   dup_item_dic.add(index)
	               else :  
	                   user_item_dic.add(index)

	buy_len = len(buy_user_item_dic)
	print 'All_buy ' + str(buy_len)
	print 'Dup Ratio ' + str(len(dup_item_dic) * 100.0 / len(buy_user_item_dic)) 
			
        '''
	#���ɷָ����ڼ�    
        if(split_date != null && !split_date.equals("null")){
            //ת��ΪСʱ
            String[] ls = split_date.split("-");
            if(ls != null ){
                //����monthֻΪ12
                int month = Integer.parseInt(ls[0]);
                int day = Integer.parseInt(ls[1]);
                //Ҳ����˵,����һ��ó���Ҳ��ͬʱ��������Ԥ��19�����ݵ������ļ�(������12-18�Ľ��׼�¼)
                while(day < 20){
                    long hour = 0;
                    if(month == 11){
                        hour = (day - 18) * 24;
                    }
                    else if(month == 12){
                        hour = 13 * 24 + (day - 1) * 24;
                    }
                    split_dates.put(hour,ls[0] + ls[1]);
                    split_dates_ordered.add(hour);
                    day++;
                }
            }
        }
	'''
def Alth() :
	#�õ������ �û�-��Ʒ��
	buy_user_item_dic = set() #�����¼
	with open(input_file_result_file) as csvfile : 
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	       if	AppendUseItemString(row['user_id'],row['item_id']) in buy_user_item_dic :
	           continue
	       else :
	           buy_user_item_dic.add(AppendUseItemString(row['user_id'],row['item_id']))
	
	#ͳ��3��֮�ڣ���6СʱΪ��������
	user_item_dic = set ()
	dup_item_dic = set ()
	with open(input_user_file) as csvfile : 
	    reader = csv.DictReader(csvfile)
	    for row in reader : 
	        index = AppendUseItemString(row['user_id'],row['item_id'])
	        if index in buy_user_item_dic : 
	               if index in buy_user_item_dic : 
	                   dup_item_dic.add(index)
	               else :  
	                   user_item_dic.add(index)

	buy_len = len(buy_user_item_dic)
	print 'All_buy ' + str(buy_len)
	print 'Dup Ratio ' + str(len(dup_item_dic) * 100.0 / len(buy_user_item_dic)) 


if __name__ == '__main__' :
        #GetDupRatio()
