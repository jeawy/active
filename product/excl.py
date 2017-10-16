# -*- encoding: utf-8 -*-
import xlrd
import xlwt 
import itertools

import pdb
import sys

h1 = xlwt.easyxf(
    'font:name Arial, bold on,height 300; borders: bottom thin, top thin, right thin, left thin; align: vert centre, horz center')

text = xlwt.easyxf(
    'font:name Arial, bold off,height 220; borders: bottom thin, top thin, right thin, left thin;  align: vert centre, horz left')


text_centre = xlwt.easyxf(
    'font:name Arial, bold off,height 220; borders: bottom thin, top thin, right thin, left thin; align: vert centre, horz centre')

text_right = xlwt.easyxf(
    'font:name Arial, bold off,height 220; borders: bottom thin, top thin, right thin, left thin; align: vert centre, horz right')
 
def write_attendecies(**kwargs):
    f = xlwt.Workbook(encoding = 'utf-8')
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
    col_width_t = 256*30
    col_width_b = 256*20
    col_width_s = 256*6
    col_width_m = 256*12
     
    try:
        for i in itertools.count():
            sheet1.col(i).width = col_width_m
    except ValueError:
        pass
    sheet1.col(1).width = col_width_t
    sheet1.col(2).width = col_width_b
    sheet1.col(3).width = col_width_t   
  
    sheet1.row(0).height_mismatch = True
    sheet1.row(0).height = 21*20 
    row4  = [ u'序号', u'姓名', u'电话',  ]

    for item in range(0, len(row4)):
        sheet1.write(0, item, row4[item], text_centre)
    i = 1
    j = 1
    total = 0
    text_centre.alignment.wrap = 1 
    if kwargs['attendencies'] : 
        for in_item in kwargs['attendencies']: 
            sheet1.write(i, 0, j, text_centre)
            sheet1.write(i, 1, in_item.name, text_centre)
            sheet1.write(i, 2, in_item.quantity, text_centre) 
             
            i += 1
            j += 1            
    try:
        f.save(kwargs['filename']) #保存文件
    except IOError, e:
        print e