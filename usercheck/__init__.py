import unicodedata
import argparse

from usercheck.UsernameChecker import UsernameChecker

# Services
from usercheck.services.Twitter import Twitter
from usercheck.services.Reddit import Reddit
from usercheck.services.Github import Github
from usercheck.services.Instagram import Instagram


def remove_accents(input_str):
    return ''.join((c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn'))


def isFullAvailable(src):
    for s in src:
        if not src[s]:
            return False

    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("usernameOrFilename", help="Username or filename to check")
    parser.add_argument("-f", "--file", help="File mode", default=False, action='store_true')
    parser.add_argument("-n", "--num_threads", help="Max num threads", default=0)
    parser.add_argument("-a", "--async", help="Async", default=False, action='store_true')
    parser.add_argument("-d", "--debug", help="Debug messages", default=False, action='store_true')
    parser.add_argument("-c", "--complete", help="Dont stop on first false", default=False, action='store_true')
    parser.add_argument("-s", "--savedir", help="Save dir")
    parser.add_argument("-j", "--json", help="Output as JSON", action='store_true', default=False)
    parser.add_argument("-p", "--progress", help="Progress bar", action='store_true', default=False)

    args = parser.parse_args()

    usernames = []

    if args.file:
        file = args.usernameOrFilename
        usernames = [line.rstrip('\n') for line in open(file)]
        usernames = list(filter(lambda a: a != '', usernames))

    else:
        usernames = [args.usernameOrFilename]

    UC = UsernameChecker(args.complete, args.debug, args.savedir, args.json, args.progress)

    UC.feedUsernames(usernames)

    UC.feedServices([Twitter, Reddit, Github, Instagram])

    if args.async:
        if args.num_threads:
            r = UC.runAsync(int(args.num_threads))
        else:
            r = UC.runAsync()

    else:
        r = UC.run()

    json_output = None

    if args.json:
        import json

        json_output = json.dumps(r, indent=4)

        print(json_output)

    else:
        for u in r:
            if not args.complete:
                print(u)
            else:
                if isFullAvailable(r[u]):
                    print('\033[92m' + u + '\033[0m')
                else:
                    print('\033[91m' + u + '\033[0m')

                for s in r[u]:
                    space = ' ' * (15 - len(s))
                    if r[u][s]:
                        print('\033[92m' + '\t' + s + space + str(r[u][s]) + '\033[0m')
                    else:
                        print('\033[91m' + '\t' + s + space + str(r[u][s]) + '\033[0m')


if __name__ == '__main__':
    main()
