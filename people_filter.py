def filter_like(comment_people_list, like_people_list):
    print("FILTER_LIKE!")
    lottery_people_list = []
    for comment_person in comment_people_list:
        print("c", comment_person)
        for i in range( len(like_people_list) ):
            like_person = like_people_list[i]
            print("l", like_person)
            if comment_person[1] == like_person[1]:
                lottery_people_list.append(comment_person)
                del like_people_list[i]
                break
    return lottery_people_list

def filter_csv(csv_data, data_index, fb_data):
    legal_list = []
    for d in fb_data:
        print(d)
        for i in range(len(csv_data)):
            c = csv_data[i]
            if d[data_index]==c:
                legal_list.append(d)
                del csv_data[i]
                break
    return legal_list