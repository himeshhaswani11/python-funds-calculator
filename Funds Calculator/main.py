from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    # with open("fund_list.json", "r") as fund_list_file:
    #     data = json.load(fund_list_file)

    # code = []

    # category = list(data.keys())
    # for rec in category:
    #     if data.get(rec).get('code'):
    #         code.append("{} - {}".format(data.get(rec).get('code'), data.get(rec).get('name')))

    #     else:
    #         sub_category = data.get(rec).keys()
    #         for sub_rec in sub_category:
    #             if data.get(rec).get(sub_rec).get('code'):
    #                 code.append("{} - {}".format(data.get(rec).get(sub_rec).get('code'), data.get(rec).get(sub_rec).get('name')))
    return render_template('main.html')

    # return render_template('main.html', category=category[1:], code=code)

@app.route('/temp', methods=['GET','POST'])
def temp():
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

                    return render_template('main.html')
            except IndexError as error:
                pass

        with open("fund_list.json", "w") as fund_list_file:
            json.dump(fund_list, fund_list_file, indent = 4) 

        with open("fund_data.json", "w") as fund_data_file:
            json.dump(fund_data, fund_data_file, indent = 4)

@app.route('/get/sub/category', methods=['POST'])
def get_sub_category():
    category = request.json['category']

    with open("fund_list.json", "r") as fund_list_file:
        data = json.load(fund_list_file)

        if len(data.get(category).keys()) == 2:
            if data.get(category).get('code'):
                return {'status' : 1, 'sub_category':["{} - {}".format(data.get(category).get('code'), data.get(category).get('name'))]}
            else:
                return {'status' : 1, 'sub_category':list(data.get(category).keys())}
        else:
            return {'status' : 1, 'sub_category':list(data.get(category).keys())}

@app.route('/get/current/value', methods=['POST'])
def get_current_value():
    fund_name = request.json['fund_name']
    amount = float(request.json['amount'])
    date = request.json['date']

    month = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', 
             '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}

    date = "{}-{}-{}".format(date[0:2], month.get(date[3:5]), date[6:10])
    with open("fund_data.json", "r") as fund_list_file:
        data = json.load(fund_list_file)

    old_net_price = float(0.00)
    new_net_price = float(0.00)
    total_units = float(0.00)
    new_price = float(0.00)

    cur_day = "03-Aug-2020"

    try:
        if data.get(date):
            if data.get(date).get(fund_name[0:6]):
                old_net_price = float(data.get(date).get(fund_name[0:6]).get('net_price'))
                total_units = amount/old_net_price
        if data.get(cur_day):
            if data.get(cur_day).get(fund_name[0:6]):
                new_net_price = float(data.get(cur_day).get(fund_name[0:6]).get('net_price'))
                new_price = total_units * new_net_price

        if new_price == 0.00:
            return{'status':0, 'data': 'Record Not Found.'}
        else:
            return{'status':1, 'data': '%.2f'%new_price}

    except Exception as e:
        return{'status':2, 'data': 'Technical Issue.'}

if __name__ == '__main__':
    app.run()