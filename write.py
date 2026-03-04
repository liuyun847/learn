from tools import bases, see, log, r, line, count_chars
from fun.language_tricks import print_flow


# 1. bases - 继承树可视化
class A: pass
class B(A): pass
class C(A): pass
class D(B,C): pass
bases(D)  # 输出漂亮的树形结构

line()
# 2. see - 对象探索
see(str, simple=1 ,translate_doc=1)  # 查看字符串的所有方法

# 3. print_flow - 打字机效果
print_flow(*["\nhelloworld\n"]*20)



# 4. @log - 递归可视化
@log
def fib(n):
    return n if n <= 1 else fib(n-1) + fib(n-2)
fib(5)  # 能看到每次调用的参数和返回值

line()
# 5. Frange - 罗马数字和浮点数范围
l1=list(r.xv)   
l2=list(r(3.5)) 
print(l1)
print(l2)
line()
# 6. count_chars - 统计文件中的字符数
count_chars(extension="py")
count_chars(extension="md")