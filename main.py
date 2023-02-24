import pandas as pd
import seaborn as sns

stores = []
storeinfo = []

# Date, Worker, Worker, Worker, Worker, Manager, Total Daily Sales, Blueberry Muffin Sales, Chocolate Muff Sales, Banana Muffin Sales
# 

with open('data.txt') as f:
    for line in f:
        if 'LOCATION' in line:
            stores.append([])
            storeinfo.append(line.split()[1])
        if 'Rent' in line:
            storeinfo.append(line.split()[1])
        if ',' in line:
            newline = line.strip().split(',')
            lineinfo = {}
            lineinfo['date'] = newline.pop(0) + newline.pop(0)
            lineinfo['banana sales'] = int(newline.pop())
            lineinfo['chocolate sales'] = int(newline.pop())
            lineinfo['blueberry sales'] = int(newline.pop())
            lineinfo['total sales'] = float((newline.pop())[2:])
            lineinfo['manager'] = newline.pop()
            lineinfo['workers'] = newline
            stores[-1].append(lineinfo)

colnames = ['date', 'banana sales', 'chocolate sales', 'blueberry sales', 'total sales', 'manager', 'workers']

# set up the new data form
newrep = {}
for i in range(4):
    name = storeinfo[i * 2] + storeinfo[i * 2 + 1]
    datadict = {}
    listrep = stores[i]
    df = pd.DataFrame()
    tempdict = {}
    for colname in colnames:
        tempcol = []
        for listing in stores[i]:
            tempcol.append(listing[colname])
        tempdict[colname] = tempcol
    for key, value in tempdict.items():
        df[key] = value
    newrep[name] = {'dataframe' : df, 'listformat' : listrep}

# find correlations b/n items in each store
for key in newrep.keys():
    newdf = newrep[key]['dataframe'].drop(columns = ['date', 'total sales', 'manager', 'workers'])
    correlations = newdf.corr(numeric_only = True)
    print(key + ' correlations\n', correlations, '\n')

# find out employee totals for each store
for key in newrep.keys():
    list_o_dicts = newrep[key]['listformat']
    employees = {}
    for entry in list_o_dicts:
        for worker in entry['workers'] + [entry['manager']]:
            if worker not in employees:
                employees[worker] = {'banana sales' : 0, 'chocolate sales' : 0, 'blueberry sales' : 0, 'days' : 0}
            for colname in ['banana sales', 'chocolate sales', 'blueberry sales']:
                employees[worker][colname] += entry[colname]
            employees[worker]['days'] += 1
    df_employee_sales = pd.DataFrame()
    temp_dict = {'names' : [], 'banana sales' : [], 'chocolate sales' : [], 'blueberry sales' : []}
    for tkey in employees.keys(): # for each employee
        temp_dict['names'].append(tkey)
        for col in ['banana sales', 'chocolate sales', 'blueberry sales']:
            temp_dict[col].append(round(employees[tkey][col] / employees[tkey]['days'], 2))
            #temp_dict[col].append(employees[tkey][col])
    for tkey in temp_dict.keys():
        df_employee_sales[tkey] = temp_dict[tkey]
    print('\n', key, '\n', df_employee_sales)

# find out stealing employee totals for each store
for key in newrep.keys():
    list_o_dicts = newrep[key]['listformat']
    employees = {}
    for entry in list_o_dicts:
        for worker in entry['workers'] + [entry['manager']]:
            if worker not in employees:
                employees[worker] = {'banana sales' : 0, 'chocolate sales' : 0, 'blueberry sales' : 0, 'total sales' : 0}
            for colname in ['banana sales', 'chocolate sales', 'blueberry sales', 'total sales']:
                employees[worker][colname] += entry[colname]
    df_employee_sales = pd.DataFrame()
    temp_dict = {'names' : [], 'banana sales' : [], 'chocolate sales' : [], 'blueberry sales' : [], 'total sales' : []}
    for tkey in employees.keys(): # for each employee
        temp_dict['names'].append(tkey)
        for col in ['banana sales', 'chocolate sales', 'blueberry sales', 'total sales']:
            temp_dict[col].append(employees[tkey][col])
    for tkey in temp_dict.keys():
        df_employee_sales[tkey] = temp_dict[tkey]
    print('\n', key, '\n', df_employee_sales)
    for index, row in df_employee_sales.iterrows():
        expected_value = row[1] * 3 + row[2] * 2.5 + row[3] * 2
        total_value = row[4]
        print(expected_value - total_value, row[0])