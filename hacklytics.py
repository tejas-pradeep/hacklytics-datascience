import requests
def organize_Country():
    s = "C:/Users/rptej/Desktop/Code/Python/Data Science/global_power_plant_database.csv"
    result =open(s‪,'r')
    data = result.readlines()
    data = data[1::]
    dic = {}
    lis = []
    for i in data:
        lis = i.split(' ,')
        try:
            dic[lis[0]] +=1
        except:
            dic[lis[0]] +=1
    for i in dic.keys():
        print(dic[i])

