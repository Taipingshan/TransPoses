import openpyxl


i = 1
def pretty_print_sensor_data(sensor_data):
    data = sensor_data
    
    workbook = openpyxl.load_workbook('./lpresearch/data.xlsx')
    worksheet1 = workbook.active
    global i
    worksheet1._current_row = i
    worksheet1.append(data)
    workbook.save(filename='./lpresearch/data.xlsx')
    workbook.close()
    i += 1


for i in range(1,100):

    sensor_data =i
    pretty_print_sensor_data(sensor_data)

