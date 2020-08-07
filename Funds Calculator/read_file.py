import json

fund_list = {}
fund_data = {}

with open("DownloadNAVHistoryReport_Po.txt", 'r') as file:
    for line in file:
        data = list(line.strip().split(';', 8)) 
        temp_dict = {}

        try:
            temp_data = data[1].split('-', 1)
            category = temp_data[0].strip()

            if category in fund_list:       
                sub_category = "{} - {}".format(data[0], temp_data[1].strip())
                fund_list[category][sub_category] = {}
                
                if sub_category in fund_list[category]:
                    fund_list[category][sub_category]['code'] = data[0]
                    fund_list[category][sub_category]['name'] = data[1]                                        
            else:
                if len(temp_data) == 1:
                    fund_list[category] = {}                 
                    fund_list[category]['code'] = data[0]
                    fund_list[category]['name'] = data[1]
                else:
                    fund_list[category] = {} 


            date = data[7].strip()
            code = data[0].strip()

            if not date in fund_data:
                fund_data[date] = {}
                fund_data[date][code] = {}
                fund_data[date][code]['name'] = data[1]
                fund_data[date][code]['net_price'] = data[4]
                fund_data[date][code]['purchase_price'] = data[5]
                fund_data[date][code]['sale_price'] = data[6]
            else:
                if not code in fund_data[date]:
                    fund_data[date][code] = {}
                fund_data[date][code]['name'] = data[1]
                fund_data[date][code]['net_price'] = data[4]
                fund_data[date][code]['purchase_price'] = data[5]
                fund_data[date][code]['sale_price'] = data[6]

        except IndexError as error:
            pass


    with open("fund_list.json", "w") as fund_list_file:
        json.dump(fund_list, fund_list_file, indent = 4) 

    # with open("fund_data.json", "w") as fund_data_file:
    #     json.dump(fund_data, fund_data_file, indent = 4) 

    # with open("fund_list.json", "r") as fund_list_file:
    #     data = json.load(fund_list_file) 
    #     print(data.get('Axis Ultra Short Term Fund').keys())

