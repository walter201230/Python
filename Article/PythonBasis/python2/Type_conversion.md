# 五、基本数据类型转换 #

Python 中基本数据类型转换的方法有下面几个。

|方法|说明|
|-----|------|
|int(x [,base ])  |       将x转换为一个整数  |
|float(x )    |           将x转换到一个浮点数  |
|complex(real [,imag ])|  创建一个复数  |
|str(x ) |                将对象 x 转换为字符串  |
|repr(x ) |               将对象 x 转换为表达式字符串  |
|eval(str )  |            用来计算在字符串中的有效 Python 表达式,并返回一个对象  |
|tuple(s )  |             将序列 s 转换为一个元组  |
|list(s )   |             将序列 s 转换为一个列表  |
|chr(x )   |              将一个整数转换为一个字符  |
|unichr(x )  |            将一个整数转换为 Unicode 字符  |
|ord(x )     |            将一个字符转换为它的整数值  |
|hex(x )     |            将一个整数转换为一个十六进制字符串  |
|oct(x )     |            将一个整数转换为一个八进制字符串  |

注：在 Python 3 里，只有一种整数类型 int，表示为长整型，没有 python2 中的 Long。

这里我们可以尝试一下这些函数方法。

比如 `int()` 函数，将符合规则的字符串类型转化为整数 。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-30-091547.png)

输出结果：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-30-091648.png)

注意这里是符合规则的字符串类型，如果是文字形式等字符串是不可以被 `int()` 函数强制转换的。

还有小数形式的字符串也是不能用  `int()`  函数转换的。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-31-064739.png)

这样转换会报错。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-31-064811.png)

但这并不是意味着浮点数不能转化为整数，而是小数形式的字符串不能强转为字符串。

浮点数还是可以通过 `int()`  函数转换的。

比如：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-31-065336.png)

输出结果：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-31-065407.png)

但是你会发现，结果是 88 ，后面小数点的 0.88 被去掉了。

这是因为  `int()`  函数是将数据转为整数。如果是浮点数转为整数，那么  `int()`  函数就会做取整处理，只取整数部分。所以输出的结果为 88 。

其余的方法就不一一列举了，只要多用，多试，这些方法都会慢慢熟悉的。还有如果是初学者，完全可以每个方法都玩一下，写一下，随便写，然后运行看结果，反正你的电脑又不会因为这样而玩坏的。










