from threading import Thread, RLock

lock = RLock()


class AsyncChecker(Thread):
    def __init__(self, usernames, out, services, complete, debug, name=None):
        Thread.__init__(self)
        self.usernames = usernames
        self.out = out
        self.services = services
        self.complete = complete
        self.debug = debug
        self.name = name

    def runOneUsername(self, username):
        results = dict()
        for s in self.services:
            tmp = self.services[s].run(username)
            if self.complete:
                results[s] = tmp
            else:
                if not tmp:
                    return False

        if self.complete:
            return results
        return True

    def run(self):
        if self.name and self.debug:
            print('Thread ' + self.name + ' launched')

        if self.complete:
            results = dict()
        else:
            results = []

        for u in self.usernames:
            res = self.runOneUsername(u)
            if self.complete:
                results[u] = res
            else:
                if res:
                    results.append(u)

        with lock:
            if not self.complete:
                self.out.extend(results)
            else:
                for r in results:
                    self.out[r] = results[r]

        if self.name and self.debug:
            print('Thread ' + self.name + ' done')


def chunks(l, n):
    k, m = divmod(len(l), n)
    return (l[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


class UsernameChecker:
    def __init__(self, complete, debug, savedir, json, progress):
        self.usernames = None
        self.services = dict()
        self.complete = complete
        self.debug = debug
        self.savedir = savedir
        self.json = json
        self.progress = progress

    def feedUsernames(self, usernames):
        self.usernames = usernames

    def feedServices(self, services):
        for s in services:
            obj = s()
            name = obj.getName()
            if self.debug:
                print('Adding service ' + name)
            self.services[name] = obj

    def runOneUsername(self, username):
        results = dict()
        for s in self.services:
            tmp = self.services[s].run(username)
            if self.complete:
                results[s] = tmp
            else:
                if not tmp:
                    return False

        if self.complete:
            return results
        return True

    def run(self):
        if self.complete:
            results = dict()
        else:
            results = []

        if self.progress:
            from tqdm import tqdm
            for u in tqdm(self.usernames):
                res = self.runOneUsername(u)
                if self.complete:
                    results[u] = res
                else:
                    if res:
                        results.append(u)

        else:
            for u in self.usernames:
                res = self.runOneUsername(u)
                if self.complete:
                    results[u] = res
                else:
                    if res:
                        results.append(u)

        return results

    def runAsync(self, numThreads=50):
        if self.complete:
            out = dict()
        else:
            out = []

        threads = []
        i = 1
        usernamesChunks = []
        tmp = []
        for c in chunks(self.usernames, numThreads):
            tmp.append(c)

        for t in tmp:
            if len(t) > 0:
                usernamesChunks.append(t)

        if self.debug:
            print('Creating ' + str(len(usernamesChunks)) + ' chunks of ' +
                  str(len(self.usernames) / len(usernamesChunks)) + ' usernames')

        for c in usernamesChunks:
            t = AsyncChecker(c, out, self.services, self.complete, self.debug, str(i))
            i += 1
            t.start()
            threads.append(t)

        if self.progress:
            from tqdm import tqdm
            for t in tqdm(threads):
                print(' ')

                t.join()
        else:
            for t in threads:
                t.join()

        return out
