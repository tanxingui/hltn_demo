# 题目：编写一个程序，读取一个字符串并输出一个回文字符串。如果输入字符串已经是回文，直接输出；否则，通过在字符串末尾添加最少字符，使其成为回文。
# 示例：输入：abca输出：abcba

aaa = input("输入:")
shun = len(aaa)
if aaa == aaa[::-1]:
    print(aaa)
else:
    for i in range(1,shun):
        if aaa[i:] == aaa[i:][::-1]:
            print(aaa+aaa[:i][::-1])
            break


for i in range(1, 10):
    strs = ""
    for j in range(1, i + 1):
        strs += f"{i}*{j}={i * j} "
    print(strs)