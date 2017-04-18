# -*- coding: utf-8 -*-
import re

text = [u"Māsa mani kaitināja ļķī ēŗtāņw","Māsa mani kaitināja ļķī ēŗtāņw"]
def split_string(poem):
    string = " ".join(text)
    word_list = []
    for x in range(len(text.split())):
        word_list = re.findall(r'(?u)\w+', string)[x].encode('utf-8')
        print word_list

split_string(text)

