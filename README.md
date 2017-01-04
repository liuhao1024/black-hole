# black-hole


## 一、概览
black-hole延伸于[sandglass](https://github.com/kzczencode/sandglass)，由于该项目已经停止维护。于是我就拿过来维护了，就有了这个项目。

black-hole对时间对象datetime.datetime进行了增强，让时间的格式化输出、转换使用起来更加友好。

## 二、安装

1. `easy_install black-hole`
2. `pip install black-hole`



## 三、用法
### Blackhole对象
在black-hole中，核心对象是 Blackhole对象，通过这个对象，可以方便的获取各个时间属性和操作。
```
    >> bh = Blackhole.now()
    >> bh
    <blackhole object (2016-01-01 20:20:20)>
    >> bh.year, bh.month, bh.day, bh.hour, bh.minute, bh.second, bh.microsecond
    (2016, 1, 1, 20, 20, 20, 962902)
    >> bh.timestamp
    1451650820

    # 获取常用的sql格式
    >> bh.sql  
    '2016-01-01 20:20:20'
    >> bh.sqldate
    '2016-01-01'
    >> bh.sqltime
    '20:20:20'

    # 进行增量变换(shift是原地操作，而shifted返回一个新对象)
    >> bh.shifted(day=1, minute=-2)
    <Blackhole object (2016-01-02 20:18:20.962902)>
    >> bh.hour = 21
    >> bh
    <Blackhole object (2016-01-01 21:20:20.962902)>

    # 获取指定时间层级的最小和最大时间
    >> bh.floor('hour'), bh.ceil('hour')
    (<Blackhole object (2016-01-01 21:00:00)>, <Blackhole object (2016-01-01 21:59:59.999999)>)
    >> bh.floor('year'), bh.ceil('year')
    (<Blackhole object (2016-01-01 00:00:00)>, <Blackhole object (2016-12-31 23:59:59.999999)>)
 
    # 重载符号
    >> bh1 = Blackhole(year=2016, month=1, day=1, hour=0)
    >> bh2 = Blackhole(year=2016,month=2,day=2,hour=0)
    >> bh1 == bh2
    False
    >> bh1 < bh2
    True
    >> bh1 > bh2
    False
    >> bh2 - bh1
    datetime.timedelta(32)

    # mock当前时间，这样就测试的时候就不用改时间，直接mock给当前时间加上个偏移量就行了
    # 比如我要把时间往后推一天
    >> bh = Blackhole.now()
    <blackhole object (2016-01-01 20:20:20.113000)>
    >> Blackhole.mock(day=1)
    >> Blackhole.now()
    <blackhole object (2016-01-02 20:20:20.113000)>
    >> Blackhole.unmock()
    >> Blackhole.now()
    <blackhole object (2016-01-01 20:20:20.113000)>

    #其它
    >> bh = Blackhole.now()
    <blackhole object (2016-01-01 20:20:20.113000)>
    >> bh.raw()
    datetime.datetime(2016, 1, 1, 20, 20, 20)
    >> bh.clone()  # 复制一个新对象
    <blackhole object (2016-01-01 20:20:20.113000)>
    >> bh.replace(day=2)  # 替换指定时间单位的值
    >> bh
    <blackhole object (2016-01-02 20:20:20.113000)>
    >> bh.days_in_month  # 获取当月的最大天数
    31
    >> bh.is_today()  # 判断时间是否在今天
    False
    >> bh.is_past_date()  # 判断时间是否为过去时
    True
    >> bh.is_future_date()  # 判断时间是否为将来时
    False
    >> bh.strftime('%Y/%m/%d')  # 格式化输出时间
    '2013/01/02'
    >> blackhole.strptime('20130203','%Y%m%d')  # 根据指定格式将时间转换为Blackhole对象
    <blackhole object (2013-02-03 00:00:00)>
```

### ben方法
我们可以使用**ben()** 函数来获取Blackhole对象。
```
    不带参数默认是当前时间
    >> ben()  # 参数是时间戳，等同于blackhole.now()
    >> ben(timestamp)
    >> ben(timestr)  # 参数是时间字符串
    >> ben(datetime)  # 参数是datetime对象
    >> ben(blackhole)  # 参数是Blackhole对象
    >> ben('2013-01-01','%Y-%m-%d')  # 显式指明格式
    >> ben(year=2013,month=2,day=8,hour=7)  # datetime-like的构造器
```
基本上能描述时间的，ben()都可以把他转化成Blackhole对象。
需要注意的是，ben(timestr)中使用词法解析来对传入参数进行解析，如果缺少某些参数，就会自动按既定规则进行填充。
补充规则：
1. 缺少年月日信息，默认用当前时间的年月日填充
2. 缺少时分秒信息，默认是0填充
```
    >> ben('2016,1,1') == ben('2016-01,01') == ben('2016 1 01') == ben('2016-01-01 00:00:00')
    True
    >> ben('2016,1,1 20:20') == ben('2016-01-01 20:20:00')
    True
    >> now = datetime.now()
    >> ben('20:20').year == now.year
    True
    >> ben('20:20').month == now.month
    True
    >> ben('20:20').day == now.day
    True
```

### tslice方法
tslice方法用来获取一个时间序列，使用方法和内置的xrange方法类似。
```
    格式：
        tslice(unit, start=ben(), end=None, step=1, count=float(inf)) -> generator of blackhole object
    参数：
        unit   范围: 'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond'
        start  默认为当前时间
        end    默认不设为不限制结束时间
        step   跨度，正负均可
        count  总的次数

    范例：
    >> list(tslice('minute',start='2016-01-01',count=3))
    [<Blackhole object (2016-01-01 00:00:00)>, <Blackhole object (2016-01-01 00:01:00)>, <Blackhole object (2016-01-01 00:02:00)>]
    
    >> list(tslice('day', '2016-01-01', '2016-01-03'))
    [<Blackhole object (2016-01-01 00:00:00)>, <Blackhole object (2016-01-02 00:00:00)>]

    >> list(tslice('day','2016-01-05','2016-01-01', step=-1))
    [<Blackhole object (2016-01-05 00:00:00)>, <Blackhole object (2016-01-04 00:00:00)>, <Blackhole object (2016-01-03 00:00:00)>, <Blackhole object (2016-01-02 00:00:00)>]

    >> list(tslice('day', '2016-01-10', '2016-01-20', step=2, count=3))
    [<Blackhole object (2016-01-10 00:00:00)>, <Blackhole object (2016-01-12 00:00:00)>, <Blackhole object (2016-01-14 00:00:00)>]

    >> list(tslice('month', start='2001-01-01', count=3))
    [<Blackhole object (2001-01-01 00:00:00)>, <Blackhole object (2001-02-01 00:00:00)>, <Blackhole object (2001-03-01 00:00:00)>]
```

### cronwalk对象
crontab对象用于对crontab表达式进行计算，获取下一个执行的时间。
```
    格式：
        cronwalk(expr,base=None)  # 如果base为空，默认是当前时间。
    
    范例:
    >> cw = iter(cronwalk('0 6 * * *',base='2016-01-01'))
    >> next(cw)
    <Blackhole object (2016-01-01 06:00:00)>
    >> next(cw)
    <Blackhole object (2016-01-01 06:00:00)>

    >> cw = iter(cronwalk('0 23-7/2 * * *',base='2016-08-08 20:30:00'))
    >> next(cw)
    <Blackhole object (2016-08-08 23:00:00)>
    >> next(cw)
    <Blackhole object (2016-08-09 01:00:00)>
```