def stack():
    stack = []
    global counter 
    counter = 0
    def puch_operation(n):
        global counter
        if len(stack)==n:
            print("\nStack is full\nYou may choose another operation ! ")
        else:
            element = int(input("\nenter the element at {} index:".format(counter)))
            stack.append(element)
            print("\n{} has been inserted in stack".format(element))
            print("\nand the elements are :",stack)
            counter+=1
    def pop_operation():
        if stack == []:
            print("\nStack is empty\nYou may exit now or do other task ! ")
        else:
            e = stack.pop()
            print("\n{} has been removed from the stack\n".format(e))
            print("and the remaining elements are :",stack)
    n = int(input("\nenter the limit of the stack:"))
    while True:
        print("\nselect the operation 1. puch 2. pop 3. exit")
        choice = int(input("\nenter your choice:"))
        if choice==1:
            puch_operation(n)
        elif choice==2:
            pop_operation()
        elif choice==3:
            print("\nsuccessfully exit...!")
            break
        else:
            print("\nPlease enter valid choice")
            

def add_list_index_element():	
    ls = []
    sum = 0
    index = 0
    sum_of_index_element = []
    size = int(input("enter the limit of list :"))
    for i in range(0,size):
        ls.append(int(input("enter the element at {} index:".format(i))))

    print()
    print("the original list are :",ls)

    for j in range(len(ls)):
        sum = 0
        while ls[j]!=0:
            rem = ls[index]%10
            sum = sum+rem
            ls[index] = ls[index]//10	
        sum_of_index_element.append(sum)
        index+=1

    print()
    print("After adding the digits of each element , the list is:",sum_of_index_element)


def find_postive_and_negative():
    lim = int(input("enter the limit of list : "))
    ls = []
    for i in range(lim):
        el = int(input("enter the element at {} index : ".format(i)))
        ls.append(el)
    i = 0
    positive = []
    sum = 0
    negative = []
    sum1 = 0
    while i<lim:
        if ls[i]>0:
            positive.append(ls[i])
            sum = sum+ls[i]
        elif ls[i]<0:
            negative.append(ls[i])
            sum1 = sum1+ls[i]
        i+=1
    print()
    print("the original list are :",ls)
    print()
    if positive == []:
        print("you are not insert any positve number")
    else:
        print(positive)
        print("\nthe total positive items are : ",sum)
    print()
    if negative == []:
        print("you are not insert any negative number")
    else: 
        print(negative)
        print("\nthe total negative items are : ",sum1)

    

def factor_finder():
    number = int(input("enter any number:"))
    print()
    i = 1
    sum = 0
    print("the factor of {} are as below".format(number))
    print()
    while i<=number:
        if number%i==0:
            print("\t",i)
            sum = sum+i
        i+=1
    print()
    print("the total factor of {} is : {}".format(number,sum))


def count_vowel_and_spaces():
    text = input("enter some text : ")
    ls = ['a','e','i','o','u','A','E','I','O','U']
    vowel = []
    count_vowel = 0
    count_spaces = 0
    for i in text:
        if i == " ":
            count_spaces+=1
        if i not in ls:
            continue
        else:
            vowel.append(i)
            count_vowel+=1

    print() 
    print("the original text is : ",text)
    print()
    print("the total number of vowels present in text is {} and the vowels are : {} ".format(count_vowel,vowel))
    print() 
    print("the total number of spaces present in text is : {}".format(count_spaces))


def prime_finder():
    num = int(input("enter any number to check whether a given number is prime or not : "))
    if num<2:
        print("the given number {} is not a prime number".format(num))
    else:
        i = 2
        while i < num:
            if num%i==0:
                print("the given number {} is not a prime".format(num))
                break
            i+=1
        else:
            print("the given number {} is a prime".format(num))


def even_and_odd():
    lim = int(input("enter the limit of list : "))
    lst = []
    for i in range(lim):
        el = int(input("enter the element at {} index : ".format(i)))
        lst.append(el)
    even = []
    odd = []

    for item in lst:
        if item%2!=0:
            continue
        else:
            even.append(item)
    else:

        for item in lst:
            if item%2==0:
                continue
            else:
                odd.append(item)
    print()
    if even == []:
        print("even number is not given by the user in this list")
    else:
        print("List of even numbers are : ",even)
    print()
    if odd == []:
         print("odd number is not given by the user in this list")
    else:
        print("List of odd numbers are : ",odd)


def fibonacci_series():
    n = int(input("enter how many term you want in this series : "))
    first = 0
    seccond = 1
    for i in range(n):
        print(first,end=' ')
        temp = first
        first = seccond
        seccond+=temp


