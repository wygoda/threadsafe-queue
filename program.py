#! /usr/bin/python3
from threadsafe_queue import Threadsafe_queue
from threading import Thread, current_thread
from random import randint
from time import sleep

def generate_data(target_queue):
    for i in range(50):
        data = randint(0,10)
        target_queue.push(data)

def consume_data(target_queue):
    for i in range(3):
        for j in range(5):
            target_queue.try_pop()
        sleep(0.03) #30ms

def be_overly_curious(target_queue):
    for i in range(3):
        print("{}: {}".format(current_thread().name, target_queue))
        sleep(0.03)

tq = Threadsafe_queue()

data_generators = [Thread(target=generate_data, args=(tq,)) for i in range(2)]
data_consumers = [Thread(target=consume_data, args=(tq,)) for i in range(2)]
overly_curious_readers = [Thread(target=be_overly_curious, args=(tq,)) for i in range(1)]

for t in data_generators:
    t.start()

for t in data_consumers:
    t.start()

for t in overly_curious_readers:
    t.start()


for t in data_generators:
    t.join()

for t in data_consumers:
    t.join()

for t in overly_curious_readers:
    t.join()
