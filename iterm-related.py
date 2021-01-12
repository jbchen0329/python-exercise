class Foo:
    def __getitem__(self, item):
        print("getitem")
        return self.__dict__[item]

    def __setitem__(self, key, value):
        print("setitem")
        self.__dict__[key]=value

    def __delitem__(self, key):
        print("delitem")
        self.__dict__.pop(key)

f1=Foo()
print(f1.__dict__)
# f1.name="egon"
f1['name']="egon"
f1["age"]="20"

print(f1.__dict__)

del f1["name"]
print(f1.__dict__)

f1['age']
print(f1['age'])

#点的方式操作的属性与getattr相关,中括号操作的属性与item相关#item方法注意是通过下标来访问字典,getattr通过.号访问实例属性,__getitem__方法只有当self的属性存在时通过下标访问时才会触发,__getattr__当访问self的属性不存在时候触发