from time import sleep
import threading

def myFunction(i):
    counter=0
    while (counter<4):
        print ("thread {0}:{1}".format(i,counter))
        counter+=1
        sleep(1)


t=threading.Thread(target=myFunction,args=(1,))
t.start()
print("Main 1")
print("Main 2")
t=threading.Thread(target=myFunction,args=(2,))
t.start()
print("Main 3")
print("Main 4")
