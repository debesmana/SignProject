# -*- coding: utf-8 -*-
import re

text = u"Māsa mnūŗš ļķī ēŗtāņw"
def split_string(string):
    word_list = []
    for x in range(len(text.split())):
        word_list = re.findall(r'(?u)\w+', string)[x].encode('utf-8')
        print word_list

split_string(text)

