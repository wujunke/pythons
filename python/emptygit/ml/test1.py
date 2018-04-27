#coding=utf-8
import numpy
# L1 = ['Hello', 'World', 18, 'Apple', None]
# L2 = []
# for item in L1:
#    if isinstance(item, str) and item != None:
#        L2.append(item.lower())
# print L2



# 输出杨辉三角
# def triangles():
#     L = [1]
#     n = 1
#     while n < 10:
#         yield L
#         L.append(0)
#         L = [L[i-1] + L[i] for i in range(len(L))]
#
#         n+=1
# a = triangles()
# for item in a:
#     print item




# L1 = ['adam', 'LISA', 'barT']
#
#
# def normalize(args):
#
#     item1 = args[0].upper()
#     item2 = args[1:].lower()
#     return item1 + item2
#
#
# L2 = list(map(normalize, L1))
# print(L2)



# def prod(L):
#     return reduce(lambda x,y:x * y,L)
#
#
#
# print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
# if __name__ == '__main__' :
#
#     str = 'hello world'
#
#     print str.strip( 'hello' )     #' world'
#
#     print str.strip( 'hello' ).strip()  #'world'
#
#     print str.strip( ' heldo ' )    #'helloworld'
#
#     stt = 'h1h1h2h3h4h'
#
#     print stt.strip( ' h1' )                #'h2h3h4h'
#
#     s = '123459947855aaaadgat123458sfewewrf77877898798l79'
#
#     print s.strip( '0123456789a' )         #'123459947855aaaadgat134f8sfewewrf7787789879879'

def count():
    fs = []
    for i in range(1, 3):
        def f():
             return i*i
        fs.append(f)
    return fs
f1, f2=count()
print f1(),f2()
def count2():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1, 3):
        fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
    return fs

f3, f4=count2()
print f3(),f4()

def count3():
    def f(j):
        return lambda:j * j
    fs = []
    for i in range(1, 3):
        fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
    return fs

f5=count3()
print list(f5)


import functools
# 装饰器：decorator
# 带参数的decorator
def log1(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
@log1('1234')
def now1():
    print('2015-3-25')

# 不带参数的decorator
def log2(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
@log2
def now2():
    print('2015-3-25')
now1()  #1234 now1():
        #2015-3-25
now2()  #call now2():
        #2015-3-25


import functools
# a, b,d = 1, 2,3
# # c = a>b and [a] or [b]
# c = d if a<b else a
# print c

# 带不带参数都可以的装饰器
# 装饰器不能改变原函数的结果
def log(arg_of_func):
    def decorator(func):
        @functools.wraps(func)
        def warpper(*args, **kw):
            print('begin call: log%s(%s)' % ('' if callable(func) else "('%s')" % arg_of_func, func.__name__))
            result = func(*args, **kw)
            print('end call: return %s' % (result))
            return result
        return warpper
    return decorator(arg_of_func) if callable(arg_of_func) else decorator

int2 = functools.partial(int, base=7)
# int2=functools.partial(int,'111')
print int2('16')