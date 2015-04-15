import csv
import time

#����ģ��
#date_list_train = [('2014-11-18 00','2014-12-04 00'),('2014-11-19 00','2014-12-05 00'),('2014-11-20 00','2014-12-06 00'),\
#                   ('2014-11-21 00','2014-12-07 00'),('2014-11-22 00','2014-12-08 00'),('2014-11-23 00','2014-12-09 00'),\
#                   ('2014-11-24 00','2014-12-10 00'),('2014-11-25 00','2014-12-11 00'),('2014-11-26 00','2014-12-12 00'),\
#                   ('2014-11-27 00','2014-12-13 00'),('2014-11-28 00','2014-12-14 00'),('2014-11-29 00','2014-12-15 00'),\
#                   ('2014-11-30 00','2014-12-16 00'),('2014-12-01 00','2014-12-17 00')]
date_list_test = [('2014-12-02 00','2014-12-18 00')]
date_list_train = [('2014-11-18 00','2014-12-04 00'),('2014-11-25 00','2014-12-11 00')]


start_time = '2014-11-18 00'
last_time = '2014-12-19 00'
cut_time = '2014-12-12 00'
test_time = '2014-12-19 00'
dir = 'D:\\pythonCode\\li\\'
input_user_file = dir + 'tianchi_mobile_recommend_train_user.csv'
#input_user_file = dir + 'tainchi_train_user.csv'
input_item_file = dir + 'tianchi_mobile_recommend_train_item.csv'
#input_user_file = dir + 'G2.csv'
#input_item_file = dir + 'G1.csv'
output_train_file = dir + 'TrainSet.csv'
output_vec_file = dir + 'PredictVector.csv'
days_feature = (3, 7, 15)  #ǰ3, 7, 15�������
days_featureName = ("Sales_3","Sales_7","Sales_15")
behavior = ("","click","store","shopcar","buy")     #�û���Ϊ��title
behavior_every_day = 'behavior_every_day'
user_feature_name  = ("active_ratio","buy_ratio","buy_day")  #�û�������title
train_title  = ['target','user_item_shopchar3','user_item_buy_7',behavior[4],behavior[3],days_featureName[0],days_featureName[1],user_feature_name[0],user_feature_name[1]] #trainSet��title row
predict_title  = ['user_id','item_id','user_item_shopchar3','user_item_buy_7',behavior[4],behavior[3],days_featureName[0],days_featureName[1],user_feature_name[0],user_feature_name[1]] #PredictSet��title row

ratio = 10 # �ٷֱ��͵�������һ���Ĳ���
#########################################################################################
#ʱ���ת��������
def date2days(date):
    test_time_array = time.strptime(date,'%Y-%m-%d %H')
    days_i = int((time.mktime(test_time_array))/(3600*24))
    days_f = float((time.mktime(test_time_array))/(3600*24))
    if(days_f - days_i) > 0.66 : 
        return days_i + 1
    else:
        return days_i

#�γ� userid_itemid��������ƥ��target
def AppendUseItemString(user_id, item_id) :
    s = []
    s.append(user_id)
    s.append('-')
    s.append(item_id)
    item = ''.join(s)
    return item

#�ж������Ƿ����
def IsThatDay(target, source) :
    if target == source :
        return True
    return False
	
#���һЩ���Բ����ϵ�����
def clearNagetiveSample():
    for key in user_good.keys():
        one_user_one_good = user_good[key]
       # print one_user_one_good
        op1 = sum(one_user_one_good[behavior[1]])
        op2 = sum(one_user_one_good[behavior[2]])
        op3 = sum(one_user_one_good[behavior[3]])
        op4 = sum(one_user_one_good[behavior[4]])
        op = op1 + op2 + op3 + op4
        if op4 == 0 and (op < 3 or op3 > 5):
            user_good.pop(key)
    return

start_time_stamp = date2days(start_time)
last_time_stamp = date2days(last_time)
total_days = int(last_time_stamp - start_time_stamp)
cut_time_stamp   = date2days(cut_time)
test_time_stamp  = date2days(test_time)
user_dic = {}  #�û���Ʒ�ʵ�
good_subspace_dic = {} #�û���Ʒ�Ӽ�
good_dic = {}  #��Ʒͳ�ƴʵ�  
user_good = {}  #�û�-Ʒ�ƴʵ�
use_item_result = [{}]*total_days # ��¼ÿһ���û�-��Ʒ�������(������)
test_user_dic = {}



def ReadItemFile():  #����ɸѡ�û���������Ʒ�Ƿ�����Ʒ�Ӽ���
    with open(input_item_file) as item_csv_file:
        item_reader = csv.DictReader(item_csv_file)
        for row in item_reader :
            good_subspace_dic[row['item_id']] = 1
    return

def ReadUserFile():  #�������ɴ洢�����ݽṹ
 #�û� && �û�-Ʒ�� ��Ϣ��ͳ��
    user_count = 0
    whole_count = 0
    with open(input_user_file) as csvfile :
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row['user_id']
            item_id = row['item_id']
            behavior_type = behavior[int(row['behavior_type'])]
            b_time = date2days(row['time'])
            item_category = row['item_category']
            user_count = user_count + 1
            if user_count %100000 == 0:
                print user_count
            if good_subspace_dic.has_key(item_id) == False:
                continue
            whole_count = whole_count + 1
            
            #������Ʒͳ�ƴʵ䣨ֻͳ�Ƴ��ֹ�����Ʒ/δ������Ʒ��ʱ���˵���#####################
            date_order = int(b_time - start_time_stamp)
            if good_dic.has_key(item_id) == False :  #����������ȴ���һ����ֵ,�洢��Ʒÿ����Ϊÿ��Ĳ���
                good_dic[row['item_id']] = { 'category': row['item_category'],\
                                             'geohash': row['user_geohash'],\
                                             behavior[1]: [0]*total_days,\
                                             behavior[2]: [0]*total_days,\
                                             behavior[3]: [0]*total_days,\
                                             behavior[4]: [0]*total_days
                                            }                    
            one_good = good_dic[item_id]
            one_good[behavior_type][date_order] = one_good[behavior_type][date_order] + 1
   
            
                
            #�����û�ͳ�ƴʵ�##########################################
            if user_dic.has_key(user_id) == False :  #��������ڼ�ֵ���ȴ���һ����ֵ,�洢�û���Ϊÿһ��Ĳ�����
                user_dic[user_id] = { behavior[1]: [0]*total_days,\
                                      behavior[2]: [0]*total_days,\
                                      behavior[3]: [0]*total_days,\
                                      behavior[4]: [0]*total_days
                                    }			    
            #�����û�����
            one_user = user_dic[user_id]
            one_user[behavior_type][date_order] = one_user[behavior_type][date_order] + 1
                      
            #�����û�-Ʒ������ ���ȴ���ӣ�#############################################
            use_good_id = AppendUseItemString(user_id, item_id)
            if user_good.has_key(use_good_id) == False :   #��������ڼ�ֵ���ȴ���һ����ֵ
                user_good[use_good_id] = { behavior[1]: [0]*total_days,\
                                           behavior[2]: [0]*total_days,\
                                           behavior[3]: [0]*total_days,\
                                           behavior[4]: [0]*total_days
                                         }
            user_good[use_good_id][behavior_type][date_order] = user_good[use_good_id][behavior_type][date_order] + 1
                
            #����ָ��ʱ���tag
            #���out_put_type  == 0 ��trainSet��,����cut_time����Ľ�����֮ǰ��TrainSet��tag
            result = False
            if behavior_type == 'buy' :
                result = True
                use_item_result[date_order][AppendUseItemString(user_id, item_id)] = result
    csvfile.close()
    print "read ok"
    print 'whole : ' + str(whole_count)
    return
#������Ҫ�Ĵ������������ļ�

def GenerateOneGoodFeature(one_good,start_date_order,cut_date_order):
    #����һ����Ʒ����Ϣ
    good_f1 = 0  #������
    good_f2 = 0  #�ܼ��빺�ﳵ��
    good_f3 = 0  #���3������
    good_f4 = 0  #���7������
    for date_temp in range(start_date_order,cut_date_order):
        good_f1 = one_good[behavior[4]][date_temp] + good_f1
        good_f2 = one_good[behavior[3]][date_temp] + good_f2
        if (cut_date_order - date_temp) < days_feature[0]:
            good_f3 = good_f3 + one_good[behavior[4]][date_temp]
        if (cut_date_order - date_temp) < days_feature[1]:
            good_f4 = good_f4 + one_good[behavior[4]][date_temp]
    return [good_f1,good_f2,good_f3,good_f4]

def GenerateOneUserFeature(one_user,start_date_order,cut_date_order):
    #����һ���û�����Ϣ
    ratio = 1
    user_f1 = 0  #�û��������Ʒ������������ʱ��
    user_f2 = 0
    op4 = 0
    op_total = 0
    op4_day_count = 0
    for date_temp in range(start_date_order,cut_date_order):
        if one_user[behavior[4]][date_temp] > 0:
            op4_day_count = op4_day_count + 1
        op4 = op4 + one_user[behavior[4]][date_temp]
        op_total = op_total + one_user[behavior[4]][date_temp] + one_user[behavior[3]][date_temp] + \
                   one_user[behavior[2]][date_temp] + one_user[behavior[1]][date_temp]
    if op_total == 0:    #˵���û�����Щ��û�й������Ʒ
        return False
    user_f1 = float(op_total) * 1.0 * ratio / (cut_date_order - start_date_order)
    if user_f1 < 0.01:
        return False
    user_f2 = float(op4) / op_total
    return [user_f1,user_f2]

def GenerateOneGoodOneUser(one_user_one_good,start_date_order,cut_date_order):
    good_user_f1 = 0
    good_user_f2 = 0
    for date_temp in range(start_date_order,cut_date_order):
        if (cut_date_order - date_temp) < days_feature[0]:
            good_user_f1 = good_user_f1 + one_user_one_good[behavior[3]][date_temp]
        if (cut_date_order - date_temp) < days_feature[1]:
            good_user_f2 = good_user_f2 + one_user_one_good[behavior[4]][date_temp]    
    return[good_user_f1,good_user_f2]

def JudgeResult(user_good_key,use_item_result,cut_date,cut_date2):
    for date_temp in range(cut_date,cut_date2):
        if use_item_result[date_temp].has_key(user_good_key) == True:
            return True
    return False

def GenerateFeature(out_put_type) :
    #ȷ������       
    if out_put_type == 0 :
        Title = train_title
        output_file = output_train_file
        date_list = date_list_train
    elif out_put_type == 1 :
        Title = predict_title
        output_file = output_vec_file
        date_list = date_list_test
    csvfile = file(output_file,'wb')
    writer = csv.writer(csvfile)
    writer.writerow(Title)
    
    for date_array in date_list:
        print date_array
        start_date = date2days(date_array[0]) - start_time_stamp
        cut_date = date2days(date_array[1]) - start_time_stamp
        count = 0;
       # if out_put_type == 0 :
       #     user_good_list = use_item_result
       # elif out_put_type == 1 :
       #     user_good_list = user_good

        for user_good_key in user_good :
            array = user_good_key.split('-')
            user = array[0]
            good = array[1]
            if (user_dic.has_key(user) is True) and (good_dic.has_key(good) is True) :
                # û��������Ϊ�� && ����һЩ �������߽������� ���޳���

                user_feature = GenerateOneUserFeature(user_dic[user],start_date,cut_date)   #������Ʒ����
                if user_feature == False:    #�û���ѡ��ʱ����û�в�������Ʒ�����Ժ��Ժ�������
                    continue
                good_feature = GenerateOneGoodFeature(good_dic[good],start_date,cut_date)   #�����û�����
                good_user_feature = GenerateOneGoodOneUser(user_good[user_good_key],start_date,cut_date)
                #δ����������������
                feature = []
                if out_put_type == 0 :
                    result = JudgeResult(user_good_key,use_item_result,cut_date,cut_date + 3) #result��cut_date������������
                    if result == True:
                        feature = [1] + good_user_feature + good_feature + user_feature
                    else:
                        feature = [0] + good_user_feature + good_feature + user_feature
                elif out_put_type == 1 :
                    feature = [user] + [good] + good_user_feature + good_feature + user_feature
                writer.writerow(feature)
    print 'generate over'
    csvfile.close()
    return   
def GenerateFeatureALL(out_put_type):
    ReadItemFile()
    ReadUserFile()
    clearNagetiveSample()
    GenerateFeature(out_put_type)
    
if __name__ == '__main__' :
    #GenerateFeature(0)
    GenerateFeatureALL(1)
