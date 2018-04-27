#coding=utf-8
import numpy
import pandas as pd
from pandas import Series,DataFrame


x = DataFrame(numpy.arange(9).reshape((3, 3)),
                columns = ['A','B','C'],
                index = ['a', 'b', 'c'])
y = DataFrame(numpy.arange(12).reshape((4, 3)),
                columns = ['A','B','C'],
                index = ['a', 'b', 'c', 'd'])
print x + y
print '对x/y的不重叠部分填充，结果填充NaN'
print x.add(y, fill_value = 0) # x不变化



print '重新指定索引及NaN填充值'
x = Series([4, 7, 5], index = ['a', 'b', 'c'])
y = x.reindex(['a', 'b', 'c', 'd'])
print y
print x.reindex(['a', 'b', 'c', 'd'], fill_value = 0)
# fill_value 指定不存在元素NaN的默认值

print '重新指定索引并指定填充NaN的方法'
x = Series(['blue', 'purple'], index = [0, 2])
print x.reindex(range(4), method = 'ffill')



a= numpy.array([[1, 2, 3 , 4], [4, 5, 6, 7]])
print numpy.reshape(a, 8)




print '重新指定索引及NaN填充值'
x = Series([4, 7, 5], index = ['a', 'b', 'c'])
y = x.reindex(['a', 'b', 'c', 'd'])
print y
'''
a    4.0
b    7.0
c    5.0
d    NaN
dtype: float64
'''
print x.reindex(['a', 'b', 'c', 'd'], fill_value = 0)
# fill_value 指定不存在元素NaN的默认值
'''
a    4
b    7
c    5
d    0
dtype: int64
'''

print '重新指定索引并指定填充NaN的方法'
x = Series(['blue', 'purple'], index = [0, 2])
print x.reindex(range(4), method = 'ffill')#前向填充
'''
0      blue
1      blue
2    purple
3    purple
dtype: object
'''

print '对DataFrame重新指定行/列索引'
x = DataFrame(numpy.arange(9).reshape(3, 3),
                  index = ['a', 'c', 'd'],
                  columns = ['A', 'B', 'C'])
print x
'''
   A  B  C
a  0  1  2
c  3  4  5
d  6  7  8
'''
x =  x.reindex(['a', 'b', 'c', 'd'],method = 'bfill')#后向填充
print x
'''
   A  B  C
a  0  1  2
b  3  4  5
c  3  4  5
d  6  7  8
'''

print '重新指定column'
states = ['A', 'B', 'C','D']
x =  x.reindex(columns = states,fill_value = 0)
print x
'''
   A  B  C  D
a  0  1  2  0
b  3  4  5  0
c  6  7  8  0
d  3  4  5  0
'''
print x.ix[['a', 'b', 'd', 'c'], states]
'''
   A  B  C  D
a  0  1  2  0
b  3  4  5  0
d  6  7  8  0
c  3  4  5  0
'''