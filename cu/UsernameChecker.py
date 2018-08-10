from threading import Thread, RLock

lock = RLock()


class AsyncChecker(Thread):
    def __init__(self, usernames, out, services, name=None):
        Thread.__init__(self)
        self.usernames = usernames
        self.out = out
        self.services = services
        self.name = name

    def runOneUsername(self, username):
        for s in self.services:
            result = self.services[s].run(username)
            if not result:
                return False

        return True

    def run(self):
        if self.name:
            print('Thread ' + self.name + ' launched')
        results = []
        for u in self.usernames:
            if self.runOneUsername(u):
                results.append(u)

        with lock:
            self.out.extend(results)

        if self.name:
            print('Thread ' + self.name + ' done')


def chunks(l, n):
    k, m = divmod(len(l), n)
    return (l[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


class UsernameChecker:
    def __init__(self, complete, debug, savedir):
        self.usernames = None
        self.services = dict()
        self.complete = complete
        self.debug = debug
        self.savedir = savedir

    def feedUsernames(self, usernames):
        self.usernames = usernames

    def feedServices(self, services):
        for s in services:
            obj = s()
            name = obj.getName()
            if self.debug:
                print('Adding service ' + name)
            self.services[name] = obj

    def runOneUsername(self, username, all=False):
        results = []
        for s in self.services:
            result = self.services[s].run(username)
            print(s + ' ' + str(result))
            if all:
                results.append(result)
            else:
                if not result:
                    return False

        if all:
            return results
        return True

    def run(self):
        results = []
        for u in self.usernames:
            res = self.runOneUsername(u, self.complete)
            if all:
                out = [u]
                out.extend(res)
                results.append(out)
            else:
                if res:
                    results.append(u)

        return results

    def runAsync(self, numThreads=50):
        out = []
        threads = []
        i = 0
        usernamesChunks = []
        tmp = []
        for c in chunks(self.usernames, numThreads):
            tmp.append(c)

        for t in tmp:
            if len(t) > 0:
                usernamesChunks.append(t)

        for c in usernamesChunks:
            t = AsyncChecker(c, out, self.services, str(i))
            i += 1
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        return out
