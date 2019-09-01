# 三、Python 的基本数据类型 #

## 1、字符串 ##

字符串英文 string ，是 python 中随处可见的数据类型，字符串的识别也非常的简单，就是用「引号」括起来的。

引号包括单引号 `' '` ，双引号 `" "` 和 三引号 `''' '''` ，比如 `'abc'` ，`"123"` 等等。

这里请注意，单引号 `''`  或双引号 `""`  本身只是一种表示方式，不是字符串的一部分，因此，字符串 `'abc'` 只有 a，b，c 这 3 个字符。

如果善于思考的你，一定会问？

为什么要有单引号 `' '` ，双引号 `" "` 和 三引号 `''' '''` 啊，直接定死一个不就好了，搞那么麻烦，那么多规则表达同一个东西干嘛？

对，一般来说一种语法只用一个规则来表示是最好的，竟然现在字符串有三种不同的表示，证明是有原因的。

那么我们先来看下这三种方式，来定义同样内容的字符串，再把它打印出来，看看是怎样的。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-071320.png)

打印出来的结果是一样的。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-071403.png)

那如果我们的字符串不是 `两点水`，是 `两'点'水` 这样呢？

这样就直接报错了。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-071800.png)

但是要注意，用单引号 `' '` 不行，用双引号 `" "` 是可以的。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-072459.png)

打印的结果也跟预想的一样：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-072523.png)

至于三引号，也是一样的，如果字符串内容里面含有双引号，也是会报同样的错误的。那么这时候你就可以用三引号了。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-072701.png)

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-072829.png)

那么用单引号，双引号定义的字符串就不能表示这样的内容吗？

并不是的，你可以使用转义字符。

比如单引号，你可以使用 `\'` 来表示，双引号可以使用 `\"`  来表示。

注意，这里的是反斜杠 `\`, 不是斜杆 `/` 。

了解了之后，直接程序测试一下：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-073544.png)

运行结果如下：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-073601.png)

最后，也提一下， 三引号 `''' '''` 是直接可以分行的。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-074157.png)

运行结果：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-074209.png)






## 2、整数 ##

整数英文为 integer 。代码中的整数跟我们平常认识的整数一样，包括正整数、负整数和零，是没有小数点的数字。

Python 可以处理任意大小的整数，例如：`1`，`100`，`-8080`，`0`，等等。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-075017.png)

运行结果：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-075046.png)

当然，要注意了，如果数字你用引号括起来了，那就属于字符串，而不属于整数。比如 `'100'` , 这 100 是字符串，不是整数。

在现实世界中，整数我们通常会做计算，因此代码世界也是一样，整数可以直接加减乘除。

比如：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-075748.png)

程序运行结果：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-29-075806.png)

这里提示下大家，看看上面的例子，有没有发现什么？

看下 `int4` 打印出来的结果，是 `0.5` , 是一个小数。

而我们上面对整数的定义是什么？

是没有小数点的数字。

因此 `int4` 肯定不是整数。

这里我们可以使用 `type()` 函数来查看下类型。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-30-032745.png)

结果如下：

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-30-032826.png)

可以看到 `int4` 是 float 类型，而 `int1` ,`int2`,`int3` 都是 int 整数类型。

那么 float  是什么类型呢？

float 是浮点数类型，是我们下面会说到的。

在说浮点数之前，各位可以看下 Python 的算术运算符有哪些，有个印象。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-30-034538.png)





## 3、浮点数 ##

浮点数的英文名是 float ，是指带小数的数字。

浮点数跟整数有很多类似的地方，但是浮点数是最折磨人的，也是最难让人捉摸透的。

就好比世界级的大佬 Herb Sutter 说的：「世上的人可以分为3类：一种是知道自己不懂浮点运算的；一种是以为自己懂浮点运算的；最后一种是极少的专家级人物，他们想知道自己是否有可能，最终完全理解浮点运算。」

为什么这么说呢？

看下面的例子 ，像整数一样，只是基本的浮点数加法运算。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-30-081702.png)

可是运算结果，对于初学者来说，可能会接受不了。

![](http://twowaterimage.oss-cn-beijing.aliyuncs.com/2019-08-30-081922.png)

对于第一个还好，`0.55+0.41` 等于 0.96 ，运算结果完全一致。可是后面两个，你会发现怎么出现了那么多个零。

这是因为计算机对浮点数的表达本身是不精确的。保存在计算机中的是二进制数，二进制对有些数字不能准确表达，只能非常接近这个数。

所以我们在对浮点数做运算和比较大小的时候要小心。




## 4、布尔值 ##

布尔值和布尔代数的表示完全一致，一个布尔值只有 `True` 、 `False `两种值，要么是 `True`，要么是 `False`，在 Python 中，可以直接用 True、False 表示布尔值（请注意大小写），也可以通过布尔运算计算出来。

布尔值可以用 `and`、`or` 和 `not` 运算。

`and` 运算是与运算，只有所有都为 True，and 运算结果才是 True。

`or` 运算是或运算，只要其中有一个为 True，or 运算结果就是 True。

`not` 运算是非运算，它是一个单目运算符，把 True 变成 False，False 变成 True。



## 5、空值 ##

基本上每种编程语言都有自己的特殊值——空值，在 Python 中，用 None 来表示







