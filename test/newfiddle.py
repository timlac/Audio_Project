import queue

q = queue.Queue()

print(q.empty())

print(q.get())

for i in range(10):
    q.put(i)

print(q.empty())

size = q.qsize()

print("size:",  size)

for i in range(size):
    print(q.get())

