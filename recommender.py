# Jason Fukumoto, 23445294
# CSc 110, Autumn 2017
# This program reads through a file and recommends the user for similar books
# of other users by their ratings. Extensive use of lists, tuples,
# and dictionaries.

# Global for the top tree similarities.
SIMILARITY = 3

# Opens and reads through a file with ratings for books of different users.
# Returns the dictionary and the list of books and the list of tuples before
# the while loop.
# Program stops when the user types in 'quit'.
def main():
    file = open('ratings.txt').readlines()
    book_dict, book_set = beginning(file)
    list_tuple = averages(book_dict, book_set)
    task = intro()
    print(book_dict)
    while task != 'quit':
        if task == 'averages':
            for i in range(len(list_tuple) - 1, -1, - 1):
                print(list_tuple[i][1], list_tuple[i][0])
        elif task == 'recommend':
            recommendations(book_dict, book_set, list_tuple)
        print()
        task = input('next task? ')

# Creating a set and then casting it to a list to exclude the same book.
# Stripping every time we iterate through the file.
# Creating a new list when the name is not in the dictionary.
# If book is in the list, then the value of the name is going to be the
# rating at the same index of the original list of books.
# Returns the dictionary and the book of lists.
def beginning(file):
    book_set = set()
    book_dict = {}
    for i in range(1, len(file), 3):
        file[i] = file[i].strip()
        book_set.add(file[i])
    book_set = list(book_set)
    for i in range(0, len(file), 3):
        file[i] = file[i].strip()
        if file[i] not in book_dict:
            book_dict[file[i]] = [0] * len(book_set)
        file[i + 2] = file[i + 2].strip()
        file[i + 1] = file[i + 1].strip()
        if file[i + 1] in book_set:
            book_dict[file[i]][book_set.index(file[i + 1])] = int(file[i + 2])


    return book_dict, book_set

# Returns task for the while loop in main.
def intro():
    print('Welcome to the CSC110 Book Recommender. Type the word in the '
          '\nleft column to do the action on the right.')
    print('recommend : recommend books for a particular user')
    print('averages  : output the average ratings of all books in the system')
    print('quit      : exit the program')
    task = input('next task? ')

    return task

# Creates list of tuples that averages each book from every user in the file.
# Sorts the rating from highest to lowest.
# Returns the list of tuples
def averages(book_dict, book_set):
    list_tuple = []
    for i in range(len(book_set)):
        sum = 0
        count = 0
        for values in book_dict.values():
            sum += values[i]
            if values[i] != 0:
                count += 1
        if count > 0:
            average = sum / count
        else:
            average = 0
        tuple = (average, book_set[i])
        list_tuple.append(tuple)
    list_tuple.sort()

    return list_tuple

# Asks the user to input a name to search through the dictionaries to
# recommend the user for the top three similar books.
# Dot product for each list to get a scalar product and appends to a list.
# Sorts lists and then removes the inputted name, then reverses the list.
# Loops through to find the top three users to compute the average so the
# program can recommend books that are similar to the inputted name.
# If the input name is not in the dictionary, the averages are outputted.
def recommendations(book_dict, book_set, list_tuple):
    name = input('user? ')
    sum_list = []
    if name in book_dict:
        for key in book_dict.keys():
            sum = 0
            for i in range(len(book_dict[key])):
                sum += int(book_dict[name][i]) * int(book_dict[key][i])
            similar_tuple = (sum, key)
            sum_list.append(similar_tuple)
        sum_list.sort()
        sum_list.remove(sum_list[-1])
        sum_list.reverse()
        average_list = [0] * len(book_set)
        sums = [0] * len(book_set)
        counts = [0] * len(book_set)
        for i in range(SIMILARITY):
            temp_list = book_dict[sum_list[i][1]]
            for j in range(len(temp_list)):
                if int(temp_list[j]) != 0:
                    sums[j] += temp_list[j]
                    counts[j] += 1
            for k in range(len(average_list)):
                if int(counts[k]) != 0:
                    average_list[k] = sums[k] / counts[k]
                else:
                    average_list[k] = 0
        recommend_list = []
        for i in range(len(average_list)):
            if average_list[i] > 0:
                recommend_tuple = (average_list[i], book_set[i])
                recommend_list.append(recommend_tuple)
        recommend_list.sort()
        for i in range(len(recommend_list) - 1, - 1, - 1):
            print(recommend_list[i][1], recommend_list[i][0])
    else:
        for i in range(len(list_tuple) - 1, -1, - 1):
            print(list_tuple[i][1], list_tuple[i][0])


main()

