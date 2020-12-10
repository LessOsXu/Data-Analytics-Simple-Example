import numpy
import pandas
"""
Read data.xls and find the units in 'GOODS_NAME' column which contain 'PRO' or 'pro'.
Add a new column 'GOODS_TYPE'
"""

data = pandas.read_excel('data.xlsx', index_col=0)
condition = data['GOODS_NAME'].str.contains('PRO') | data['GOODS_NAME'].str.contains('pro')
x, y = [], []
for i in condition:
    x.append('PRO')
    y.append('Other')
result = numpy.where(condition, x, y)
writer = pandas.ExcelWriter('temp.xlsx')
df = pandas.DataFrame(data={'GOODS_NAME': data['GOODS_NAME'].tolist(), 'GOODS_TYPE': result.tolist()}, index=None)
df.to_excel(writer, 'Sheet1')
writer.save()

