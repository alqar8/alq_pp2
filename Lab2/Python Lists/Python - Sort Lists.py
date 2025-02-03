thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()
print(thislist)

thislist = [100, 50, 65, 82, 23]
thislist.sort()
print(thislist)

# Customize Sort Function
#You can also customize your own function by using the keyword argument key = function.

#The function will return a number that will be used to sort the list (the lowest number first):

#Example
#Sort the list based on how close the number is to 50: #

def myfunc(n):
  return abs(n - 50)

thislist = [100, 50, 65, 82, 23]
thislist.sort(key = myfunc)
print(thislist)