# 对实例化的反射

# hasattr
# 判断对象中是否有这个方法或变量
class Person(object):
    def __init__(self,name):
        self.name = name
    def talk(self):
        print("%s正在交谈"%self.name)

p = Person("laowang")
print(hasattr(p,"talk"))    # True。因为存在talk方法
print(hasattr(p,"name"))    # True。因为存在name变量
print(hasattr(p,"abc"))     # False。因为不存在abc方法或变量

# getattr
# 获取对象中的方法或变量的内存地址
class Person(object):
    def __init__(self,name):
        self.name = name
    def talk(self):
        print("%s正在交谈"%self.name)
p = Person("laowang")

n = getattr(p,"name")   # 获取name变量的内存地址
print(n)                # 此时打印的是:laowang

f = getattr(p,"talk")   # 获取talk方法的内存地址
f()                     # 调用talk方法
# 我们发现getattr有三个参数，那么第三个参数是做什么用的呢?
s = getattr(p,"abc","not find")
print(s)                # 打印结果：not find。因为abc在对象p中找不到，本应该报错，属性找不到，但因为修改了找不到就输出not find

# setattr
# 为对象添加变量或方法
def abc(self):
    print("%s正在交谈"%self.name)

class Person(object):
    def __init__(self,name):
        self.name = name

p = Person("laowang")
setattr(p,"talk",abc)   # 将abc函数添加到对象中p中，并命名为talk
p.talk(p)               # 调用talk方法，因为这是额外添加的方法，需手动传入对象
setattr(p,"age",30)     # 添加一个变量age,复制为30
print(p.age)            # 打印结果:30

# delattr
# 删除对象中的变量。注意：不能用于删除方法
class Person(object):
    def __init__(self,name):
        self.name = name
    def talk(self):
        print("%s正在交谈"%self.name)

p = Person("laowang")
delattr(p,"name")       # 删除name变量
# print(p.name)           # 此时将报错

# 对类的反射
class A:

    country = "中国"
    area = "深圳"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def func(self):
        print(666)

# 获取类 A 的静态属性 country
print(getattr(A, "country"))    # 中国
# 获取类 A 的静态属性 area
print(getattr(A, "area"))       # 深圳

# 获取类A 的动态方法并执行
getattr(A, "func")(23)          # 666

# 对本文件的反射
import sys

def func():
    print(666)

ret = input("请输入: ").strip()
obj = sys.modules[__name__]
getattr(obj, ret)()
# 运行结果：只有输入 func 才不会报错
# 请输入: func
# 666


# 对其他py文件的反射
# 假设有个 test02.py 文件，内容如下
flag = True

def func(a):
    return a + 3


class B:

    name_list = ["aaa", "bbb", "ccc"]

    def __init__(self, name, sex):
        self.name = name
        self.sex = sex

    def func(self):
        print(666)
# 2. 在本 py 文件中，不用反射的操作方法
# import test02
#
# # 获取 test02 包中的 flag 变量对应的值
# print(getattr(test02, "flag"))          # True
#
# # 执行 test02 包中的 func 方法
# ret = getattr(test02, "func")(10)
# print(ret)                              # 13
#
# # 获取 test02 包中的类 B
# print(getattr(test02, "B"))             # <class 'test02.B'>
#
# # 获取 test02 包中的类 B 的 name_list 属性的方式：
# # 方式一：
# print(getattr(test02, "B").name_list)   # ['aaa', 'bbb', 'ccc']
# # 方式二：
# print(getattr(test02.B, "name_list"))   # ['aaa', 'bbb', 'ccc']
#
# # 执行 test02 包中的类 B 的 func 方法（同上两种方式)
# getattr(test02, "B").func(111)          # 666
# getattr(test02.B, "func")(1)            # 666
#
# # 实例化对象
# obj = getattr(test02, "B")("小明", "男")
#
# # 获取实例化对象的属性 name
# print(obj.name)                         # 小明
#
# # 通过实例化对象获取到类 B 中的共享数据之静态属性： name_list
# print(obj.name_list)                    # ['aaa', 'bbb', 'ccc']
#
# # 通过实例化对象执行类 B 中的共享数据之动态方法： func()
# obj.func()


# 本py文件的反射操作：反射的主体是本文件
# import test02
#
# print(test02.flag)          # True
#
# ret = test02.func
# print(ret(10))              # 13
#
# print(test02.B.name_list)   # ['aaa', 'bbb', 'ccc']
#
# obj = test02.B("barry", "男")
# print(obj.name_list)        # ['aaa', 'bbb', 'ccc']
#
# # 在本文件调用所有的函数
# def func1():
#     print("in func1")
#
# def func2():
#     print("in func2")
#
# def func3():
#     print("in func3")
#
# l1 = [func1, func2, func3]
# for i in l1:
#     i()
# 运行结果：
# in func1
# in func2
# in func3
# 要是有100个就不能这样了
# import sys
#
# l1 = ["func%s" % i for i in range(1, 4)]
# print(l1)  # ['func1', 'func2', 'func3']
# obj = sys.modules[__name__]
# for i in l1:
#     getattr(obj, i)()
# 运行结果：
# in func1
# in func2
# in func3

# 在web中的应用
#
def run():
    inp = input("请输入您想访问页面的url：  ").strip()
    modules, func = inp.split("/")
    obj = __import__("lib." + modules, fromlist=True)  # 注意fromlist参数
    if hasattr(obj, func):
        func = getattr(obj, func)
        func()
    else:
        print("404")


if __name__ == '__main__':
    run()







