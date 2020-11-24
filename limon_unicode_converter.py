#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:46:48 2019

@author: danhhong
"""
import pandas as pd
import numpy as np

# split paragraph
def ParagraphSplit(text):
    toList = []
    for i in text.split("\n"):
        toList.append(i)
    return toList

limon_unicode = {}
unicode_limon = {}

fields = ['Unicode', 'Limon']
data_path = 'data/unicode_limon.csv'
data = pd.read_csv(data_path, skipinitialspace=True, usecols=fields)

unicode_array = np.asarray(data.Unicode).reshape(-1)
limon_array = np.asarray(data.Limon).reshape(-1)

for i in range(len(data)):
    limon_unicode[limon_array[i]] = unicode_array[i]
    
for i in range(len(data)):
    unicode_limon[unicode_array[i]] = limon_array[i]
    
# replace_all function
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

# Limon font classify
leftvowels = ['e','E','é']

CoengRo = ['®','R']

shipters = [':','‘']

subscripts = ['á','ç','Á','Ç','¶','©','ä','¢','Ä','Ø','þ',
              'æ','Ð','Æ','Ñ','þ','ß','Þ','§','ñ',',','ö',
              '<','Ö','µ','ü','ø','V','S','ð','¥']

cons = ['k','x','K','X','g','c','q','C','Q','j','d','z','D',
        'Z','N','t','f','T','F','n','b','p','B','P','m','y',
        'r','l','v','s','h','L','G',')']

more_dic = {'R':'្រ',')':'ប','ú':'ុ',',':'្ប','Ú':'ូ','>':'.','°':'%',
            '´':'ខ្ញុំ','¬':'(','¦':')'}

def swap(text, ch1, ch2):
    text = text.replace(ch1+ch2,ch2+ch1)
    return text

def VowelSwap(String):   
    for i, c in enumerate(String[:]):
        if c in leftvowels and String[i+1] in cons:
            #print(String[i+1] + c)
            String = swap(String, String[i], String[i+1])
            #print(String)
        else:
            continue
    return String

def RoSubSwap(String):
    for i, c in enumerate(String[:]):
        if c in CoengRo and String[i+1] in cons:
            String = swap(String, String[i], String[i+1])
    return String

def SecondSwap(String):
    for i, c in enumerate(String[:-1]):
        if c in leftvowels and String[i+1] in subscripts:
            String = swap(String, String[i], String[i+1])
        elif c in leftvowels and String[i+1] in shipters:
            String = swap(String, String[i], String[i+1])
        elif c in CoengRo and String[i+1] in subscripts:
            String = swap(String, String[i], String[i+1])
        elif c in CoengRo and String[i+1] in shipters:
            String = swap(String, String[i], String[i+1])
    return String

def RoSubVowelSwap(String):
    for i, c in enumerate(String[:]):
        if c in leftvowels and String[i+1] in CoengRo:
            String = swap(String, String[i], String[i+1])
    return String

class Converter:
    def Limon2Unicode(string):
        paralist = ParagraphSplit(string)
        new_string = ''
        for i in paralist:
            #new_string = replace_all(string,first_dic)
            firstString = RoSubSwap(i)
            #print(firstString)
            secondString = VowelSwap(firstString)
            thirdString = SecondSwap(secondString)
            #print(thirdString)
            fourString = RoSubVowelSwap(thirdString)
            #print(fourString)
            uniString = replace_all(fourString, limon_unicode)
            finalString = replace_all(uniString,more_dic)

            new_string += finalString + '\n'
        return new_string
    
    def Unicode2Limon(string):
        new_text = replace_all(string, unicode_limon)
        LimonText = new_text.replace('u002c',',')
        for i, c in enumerate(LimonText[:-1]):
            if c in subscripts and LimonText[i+1] in leftvowels:
                LimonText = swap(LimonText, LimonText[i], LimonText[i+1])
        for i, c in enumerate(LimonText[:-1]):
            if c in cons and LimonText[i+1] in leftvowels:
                LimonText = swap(LimonText, LimonText[i], LimonText[i+1])
        return LimonText

if __name__ == "__main__":
    
    # example of Limon text to Unicode text
    limon_text = "-eRbgsMagcMnYn 83>460lIRt	=326>013>000`"
    newstring = Converter.Limon2Unicode(limon_text)
    print(newstring)

