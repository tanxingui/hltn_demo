def subject():
    while True:
        try:
            choice  = int(input("请输入：(1)-->表达 (2)-->益智 (3)-->魔力耳朵 (4)魔力剑桥 (5)所有学科"))
            if 1 <= choice <= 5:
                    if choice == 5:
                        return ["表达", "益智", "魔力耳朵", "魔力剑桥"]
                    else:
                        return [["表达", "益智", "魔力耳朵", "魔力剑桥"][choice - 1]]
            else:
                print("请输入一个数字1~5获取正确的学科")
        except ValueError:
            print("输入错误，请输入数字")

aaa = ["表达", "益智", "魔力耳朵", "魔力剑桥"]
print(aaa[2])
print(subject())
print(list(subject()))