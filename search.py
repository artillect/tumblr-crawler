import requests
import re

# Initialize variables for search
foundUsersFile = open('foundUsers.txt', '+r')
foundUsers = set(foundUsersFile.read().splitlines())
searchedUsersFile = open('searchedUsers.txt', '+r')
searchedUsers = set(searchedUsersFile.read().splitlines())

searchedLinksFile = open('searchedLinks.txt', '+r')
searchedLinks = set(searchedUsersFile.read().splitlines())

testNum = 0
testLimit = 10 # Defines an upper bound for the number of crawls to do per user

for user in foundUsers - searchedUsers:
    searchedUsers.add(user)
    testNum += 1
    currentURL = 'https://' + user + '.tumblr.com'
    for i in range(0, 10):
        newUsers = set()
        print(currentURL)
        previousURL = currentURL
        text = requests.get(currentURL).text
        possibleNextURL = re.findall('https://[^/%\d]*.tumblr.com/post/\d*', text)
        for link in possibleNextURL:
            if link not in searchedLinks:
                currentURL = link # Finds URLS of posts by same user we're currently searching
                searchedLinks.add(link)
                break

        if previousURL == currentURL:
            break

        newUsers = set(re.findall('<a rel=\"nofollow\"[\s]+[^>]+>((?:[^<][^\s](?!\<\/a\>))*.)<\/a>', text)) - foundUsers
        foundUsers = foundUsers | newUsers # Finds all usernames in page

        print(str(len(newUsers)) + ' new users found this search.')
        print(str(len(foundUsers)) + ' users found in total.')
        print(str(len(searchedLinks)) + ' URLs searched in total.')
        if len(foundUsers) == 0:
            break
    if testNum == testLimit:
        break

# File Magic, figure out how to update during runtime to prevent data loss from errors
searchedUsersFile.truncate(0)
searchedUserList = """{}""".format("\n".join(list(searchedUsers)[1:]))
searchedUsersFile.write(searchedUserList)

foundUsersFile.truncate(0)
foundUserList = """{}""".format("\n".join(list(foundUsers)[1:]))
foundUsersFile.write(foundUserList)

searchedLinksFile.truncate(0)
searchedLinksList = """{}""".format("\n".join(list(searchedLinks)[1:]))
searchedLinksFile.write(foundUserList)
