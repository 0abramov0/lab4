from time import time

from main_task import do_task as main_task
from add_task_1 import do_task as add_task_1
from add_task_2 import do_task as add_task_2
from add_task_3 import do_task as add_task_3

def timer(func, repeat_count=1):
    start_time = time()
    for i in range(repeat_count):
        func()
    end_time = time()
    return f"Исполнения фунции {repeat_count} раз занало: {end_time - start_time} секунд"


print(timer(main_task, repeat_count=1000))
print(timer(add_task_1, repeat_count=1000))
print(timer(add_task_2, repeat_count=1000))
print(timer(add_task_3, repeat_count=1000))
