###########################################################################################
#
# FeynmAGI V0.1
# Imed MAGROUNE
# 2024-06
#
#########################################################################################

import threading
from queue import PriorityQueue

# Create the priority queue
task_queue = PriorityQueue()

def add_task(priority, function, *args, **kwargs):
    """Add a task to the queue with specified priority, function, and arguments."""
    print(" === )) task added")
    task_queue.put((priority, (function, args, kwargs)))

def thread_task(function, args, kwargs):
    """Function wrapper to execute tasks from the queue."""
    function(*args, **kwargs)

def thread_manager():
    """Manage and execute threads based on the tasks in the queue."""
    while not task_queue.empty():
        priority, (function, args, kwargs) = task_queue.get()
        thread = threading.Thread(target=thread_task, args=(function, args, kwargs))
        thread.start()
        thread.join()  # Wait for the task to complete
        task_queue.task_done()
       

