from feature_extract import featureExtract
import pickle
import sys

# ********************************************
# merge the train data and label by the koubei train file
class mergetraindata():

    train_feature = []
    train_UMLpair = []
    train_label = []

    def getTomergetraindata(self):

        ft = featureExtract()
        ft.get_user_feature('/home/wanghao/Document/tianchi/dataset/trainfrom7to10', 7, 10)
        ft.MergeMerchantFeature(7, 10)
        ft.mergeUserMerchantFeature(7, 10)
        ft.get_user_taobao_feature(7,10)

        location_merchant = {}

        train_path = '/home/wanghao/Document/tianchi/dataset/train11'
        merchant_path = '/home/wanghao/Document/tianchi/tianchi_dataset/ijcai2016_merchant_info'

        UML_pair_set = set()
        UL_set = set()
        default_use_feature = [-1] * 55
        default_merchant_feature = [-1] * 67
        default_userandmerchant_feature = [-1] * 38
        default_user_taobao_feature = [-1] * 192

        print "get the location merchants ......"

        with open(merchant_path) as f:
            for line in f:
                line = line.strip('\r\n')
                merchant, budget, locations = line.split(',')
                location = locations.split(':')
                for loc in location:
                    if not location_merchant.has_key(loc):
                        location_merchant[loc] = []
                    location_merchant[loc].append(merchant)

        print "merge train data feature......"

        count = 1

        with open(train_path) as f:
            for line in f:
                sys.stdout.write('\rtrain feature count %d' % count)
                sys.stdout.flush()
                count += 1

                line = line.strip('\r\n')
                user, merchant, location, time = line.split(',')

                if (user, location) not in UL_set:
                    UL_set.add((user, location))
                    for mer in location_merchant[location]:
                        feature_list = []
                        if (user, mer, location) not in UML_pair_set:
                            UML_pair_set.add((user, mer, location))

                            if ft.user_feature.has_key(user):
                                feature_list.extend(ft.user_feature[user])
                            else:
                                feature_list.extend(default_use_feature)

                            if ft.user_taobao_feature.has_key(user):
                                feature_list.extend(ft.user_taobao_feature[user])
                            else:
                                feature_list.extend(default_user_taobao_feature)

                            if ft.merchant_feature.has_key((mer, location)):
                                feature_list.extend(ft.merchant_feature[(mer, location)])
                            else:
                                feature_list.extend(default_merchant_feature)

                            if ft.userandmerchant_feature.has_key((user, mer)):
                                feature_list.extend(ft.userandmerchant_feature[(user, mer)])
                            else:
                                feature_list.extend(default_userandmerchant_feature)

                            self.train_UMLpair.append((user, mer, location))
                            self.train_feature.append(feature_list)

        print "\r\nUML_pair num :", len(self.train_UMLpair)

        labelpath = '/home/wanghao/Document/tianchi/dataset/train11'
        print "get (user,merchant,location) pairs......."
        label_set = set()
        count = 1
        with open(labelpath) as f:
            for line in f:
                sys.stdout.write("\rfind label count %d" % count)
                sys.stdout.flush()
                count += 1
                line = line.strip('\r\n')
                user, merchant, location, time = line.split(',')
                if (user, merchant, location) not in label_set:
                    label_set.add((user, merchant, location))

        positive_num = 0
        negative_num = 0
        print "\r\nset label..."
        count = 1
        for pair in self.train_UMLpair:
            sys.stdout.write("\rlabel count : %d" % count)
            sys.stdout.flush()
            count += 1
            if pair in label_set:
                self.train_label.append(1)
                positive_num += 1
            else:
                self.train_label.append(0)
                negative_num += 1

        print "\r\npositive label num :", positive_num
        print "negative label num :", negative_num
        print 'all nums', positive_num + negative_num


if __name__ == '__main__':

    data = mergetraindata()
    data.getTomergetraindata()

