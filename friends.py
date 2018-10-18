'''
File: friends.py
Author: Jason Fukumoto, 23445294
Purpose: Code that uses methods from the linked_list file that outputs the 
names that the two names have in common.
'''

from linked_list import *
import sys

'''
Except block to see if file exist. Creates a linkedlist object that adds 
nodes. Each node will contain a linkedlist of friends. Returns the 
linkedlist object
'''
def organize_ll():
    try:
        file_name = input('Input file: ')
        file = open(file_name)
    except FileNotFoundError:
        print('ERROR: Could not open file ' + file_name)
        sys.exit(1)
    ll = LinkedList()
    for line in file:
        line = line.strip().split()
        name = line[0]
        friend = line[1]
        ll.add_name(name, friend) #X to Y
        ll.add_name(friend, name) #Y to X
    return ll
'''
Returns friends linkedlist to compare
'''
def find_names(ll, name):
    return ll.find_friends(name)

'''
Prints out all the friends in common.
'''
def print_friends(ll, name1_f, name2_f):
    ll.search_match(name1_f, name2_f)

def main():
    ll = organize_ll()
    name1 = input('Name 1: ')
    name2 = input('Name 2: ')
    name1_f = find_names(ll, name1)
    name2_f = find_names(ll, name2)
    print_friends(ll, name1_f, name2_f)

main()