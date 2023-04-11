# class MyRange(object):
#     def __init__(self, start, stop):
#         self.start = start
#         self.stop = stop
#
#     def __iter__(self):  # __iter__方法必须放回self
#         return self
#
#     def __next__(self):  # __next__方法必须返回下一个值，当我们所有的元素都迭代完毕后，再执行next方法时就会出现StopIteration异常。
#         if self.start >= self.stop - 1:
#             raise StopIteration
#         self.start += 1
#         return self.start
#
#
# for i in MyRange(0, 3):  # for语句的迭代，会忽略StopIteration异常
#     print(i)  # 输出：0 1 2