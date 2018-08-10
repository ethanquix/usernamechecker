import sys
import unicodedata
import argparse

from cu.UsernameChecker import UsernameChecker

# Services
from cu.services.Twitter import Twitter
from cu.services.Reddit import Reddit
from cu.services.Github import Github
from cu.services.Instagram import Instagram


def remove_accents(input_str):
    return ''.join((c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("usernameOrFilename", help="Username or filename to check")
    parser.add_argument("-f", "--file", help="File mode", default=False, action='store_true')
    parser.add_argument("-n", "--num_threads", help="Max num threads", default=0)
    parser.add_argument("-a", "--async", help="Async", default=False, action='store_true')
    parser.add_argument("-d", "--debug", help="Debug messages", default=False, action='store_true')
    parser.add_argument("-c", "--complete", help="Dont stop on first false", default=False, action='store_true')
    parser.add_argument("-s", "--savedir", help="Save dir")
    args = parser.parse_args()
    print(args.file)
    print(args.usernameOrFilename)

    usernames = []

    if args.file:
        file = args.usernameOrFilename
        usernames = [line.rstrip('\n') for line in open(file)]

    else:
        usernames = [args.usernameOrFilename]

    UC = UsernameChecker(args.complete, args.debug, args.savedir)

    UC.feedUsernames(usernames)

    UC.feedServices([Twitter, Reddit, Github, Instagram])

    if args.async:
        if args.num_threads:
            r = UC.runAsync(int(args.num_threads))
        else:
            r = UC.runAsync()

    else:
        r = UC.run()

    for u in r:
        print(u)
