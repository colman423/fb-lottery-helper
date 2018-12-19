def run(csv_data, data_index, fb_data):
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
            
