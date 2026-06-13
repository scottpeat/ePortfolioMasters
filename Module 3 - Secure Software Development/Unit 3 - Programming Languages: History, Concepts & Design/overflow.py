# This program will throw an IndexError because the buffer has a size of 10, but the loop tries to access index 10 (which is out of bounds).
buffer=[None]*10
for i in range (0,11):
    buffer[i]=7
print(buffer)