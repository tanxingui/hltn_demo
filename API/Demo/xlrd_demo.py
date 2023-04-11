import xlrd
import os

parent_path = os.path.dirname(__file__)
excel_path = os.path.join(parent_path, 'tttt.xls')

# 根据行名跟列名拿到对应单元格数据
def get_excel_data(rowdata, coldata):
    workbook = xlrd.open_workbook(excel_path)
    sheet = workbook.sheet_by_name('Sheet1')
    col_index = None
    row_index = None
    # nrow = sheet.nrows    #获取行数
    ncol = sheet.ncols    # 获取列数
    workcol = sheet.col_values(1)    # 获取第一列
    for i in range(ncol):
        if (sheet.cell_value(0, i) == coldata):
            col_index = i  # 获取列标
            break
    for i in workcol:
        if rowdata == i:
            row_index = workcol.index(rowdata)  # 获取行号
            break
    data = sheet.cell_value(row_index, col_index)
    return data


print(get_excel_data('登陆成功', 'data'))


