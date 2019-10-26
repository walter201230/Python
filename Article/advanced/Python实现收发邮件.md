在实际开发中，当你收到一个需求的时候，比如要做一个「收发邮件」的功能。

如果你完全没有印象，没有思路，可以直接 Google 搜索的。

因为我们不可能对每个知识点都了解，不了解不可耻，但要懂得怎么去找资料了解。

强调一下，

用 Google 搜索。

用 Google 搜索。

用 Google 搜索。

恕我直言，百度搜索是真的辣鸡。

那我们怎么去找资料呢？

首先我们可以直接 Google 「Python 收发邮件」，就可以得到这么一个结果。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-10-15-065554.png)

这种常用的需求，基本只要看前几个就能知道大概的思路了。

可以看到，用 Python 实现邮件的收发，主要用到 smtplib 和 email这两个模块。


至于这些模块怎么用，直接看 [Python 官方文档](https://docs.python.org/3.7/library/smtplib.html?highlight=smtplib)

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-10-15-065957.png)

真的，没有任何教程比官方文档资料还全。

不过我们可以总结一下这些内容。

**1、SMTP 发送邮件**

Python 发送邮件主要步骤如下：

* `import smtplib` 
    - 导入 `smtplib` 模块，主要用于构造传输服务的
*  `server = smtplib.SMTP()`
    - SMTP 是 smtplib 模块中的一个类（class），实例化这个类，方便我们调用他里面的方法。
    - SMTP (Simple Mail Transfer Protocol)翻译过来是“简单邮件传输协议”的意思，SMTP 协议是由源服务器到目的地服务器传送邮件的一组规则。
*  `server.connect(host, port)`
     - 连接（connect）指定的服务器
     - host 是指定连接的邮箱服务器，你可以指定服务器的域名。
     - port 服务器的端口号
     - 这些怎么找到，好比 qq 邮箱，在「设置」那里就有相关的开关和说明。
     - ![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-10-15-090427.png)
     - 点相关的说明，你就能看到对应的服务器地址和端口号了
     - ![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-10-15-090619.png)
*  `server.login(username, password)`
    - 登录的账号密码 
* `server.sendmail(from_addr, to_addr, msg)`
    - 发送邮件，发送邮件一般是谁发给了谁，发送了什么？总结为也就是三个参数，发送者，接受者，发送邮件的内容。
    - from_addr：邮件发送地址
    - to_addr：邮件收件人地址
    - msg ： 发送邮件的内容，邮件内容需要用到 `email` 模块。通过 `email` 模块我们可以定义邮件的主题，收件人信息，发件人信息等等。
* `server.quit()`
    - 退出服务

    直接看下例子，给 QQ 邮箱发送一个邮件：
    
    

