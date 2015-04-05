import csv
import time
print time.time()

#���ݶ���
start_time = '2014-11-13'
test_time = '2014-12-19'

import time
start_time_array = time.strptime(start_time,"%Y-%m-%d")
start_time_stamp = int(time.mktime(start_time_array))
start_time_stamp = int(start_time_stamp/3600)
print start_time_stamp

import time
test_time_array = time.strptime(test_time,"%Y-%m-%d")
test_time_stamp = int(time.mktime(test_time_array))
test_time_stamp = int(test_time_stamp/3600)
print test_time_stamp

user_dic = {}  #�û���Ʒ�ʵ�
category_dic = {}  #��Ʒͳ�ƴʵ�
with open('test_ali_data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        user_id = row['user_id']
        item_id = row['item_id']
        behavior_type = row['behavior_type']
        b_time = row['time']
        item_category = row['item_category']
        
        import time
        time_array = time.strptime(b_time,"%Y-%m-%d %H")
        time_stamp = int(time.mktime(time_array))
        b_time = int(time_stamp/3600)
        #�洢��Ʒͳ����Ϣ
        if category_dic.has_key(item_category) == True:
            one_category = category_dic[item_category]
            if one_category.has_key(item_id) == True:
                one_category_one_good = one_category[item_id]
                if one_category_one_good.has_key(behavior_type) == True:
                    one_category_one_good[behavior_type] = one_category_one_good[behavior_type] + 1
                else:
                    one_category_one_good[behavior_type] = 1
            else:
                one_category[item_id] = {behavior_type:1}
        else:
            category_dic[item_category] = {item_id:{behavior_type:1}}
        #�洢�û���Ʒ��Ϣ
        if user_dic.has_key(user_id) == True:
            one_user = user_dic[user_id]
            if one_user.has_key(item_id) == True:
                one_user_one_good = one_user[item_id]
                if one_user_one_good.has_key(behavior_type) == True:
                    one_user_one_good_one_behavior = one_user_one_good[behavior_type]
                    one_user_one_good_one_behavior = one_user_one_good_one_behavior + [b_time]
                else:
                    one_user_one_good[behavior_type] = [b_time]
            else:
                one_user[item_id] = {behavior_type:[b_time]}
        else:
            user_dic[user_id] = {item_id:{behavior_type:[b_time]}}
print "read ok"
import time
print time.time()
csvfile.close()
#����ת������Ҫ�����Ʒ����Ϊ�������ת���ʣ��û�����Ʒ��Ϊʱ���ϵ�����

predict_result = []
user_result_dic = {}
for user in user_dic:
    one_user = user_dic[user]
    good_list = []
    for good in one_user:
        one_user_one_good = one_user[good]
        if one_user_one_good.has_key('4') == True:
           # good_list = good_list + [good]
            predict_result = predict_result + [(user,good)]
    #user_result_dic[user] = good_list
    #if good_list != []:
    #    print user,
    #    print "\t",
    #    print good_list
#2014-11-23 20
import csv
csvfile = file('t_predict_result.csv','wb')
writer = csv.writer(csvfile)
writer.writerow(['user_id','item_id'])
writer.writerows(predict_result)
csvfile.close()
