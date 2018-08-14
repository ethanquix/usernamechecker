# User Checker

> Check if your username is already taken !


## User Checker CLI
`usage: usercheck [-h] [-f] [-n NUM_THREADS] [-a] [-d] [-c] [-s SAVEDIR] [-j] [-p]
              usernameOrFilename`

```
positional arguments:
  usernameOrFilename            Username or filename to check

optional arguments:
  -h, --help                    show this help message and exit
  -f, --file                    File mode
  -n NUM_THREADS                Max num threads (default=50)
  --num_threads   NUM_THREADS   Max num threads (default=50)
  -a, --async                   Async
  -d, --debug                   Debug messages
  -c, --complete                Dont stop on first false
  -j, --json                    Output as JSON
  -p, --progress                Progress bar

```

## Sample

Basic
```
$ usercheck ethanquix
# Output nothing because at least one service return False

$ usercheck random_goodbaguette_croissant
random_goodbaguette_croissant
```

Complete
```
$ usercheck ethanquix -c
ethanquix
	twitter        False
	reddit         False
	github         False
	instagram      False

$ usercheck ethanqx -c
ethanquix
	twitter        False
	reddit         False
	github         True
	instagram      True
```

File
```
$ cat data/samples.txt
jack
this_pseudo_dont_existWEEUFHG
gooogle

$ usercheck data/samples.txt -f
this_pseudo_dont_existWEEUFHG

$ usercheck data/samples.txt -fc
jack
	twitter        False
	reddit         False
	github         False
	instagram      False
this_pseudo_dont_existWEEUFHG
	twitter        True
	reddit         True
	github         True
	instagram      True
gooogle
	twitter        False
	reddit         False
	github         False
	instagram      False
```

Json
```
$ usercheck ethanquix -cj
{
    "ethanquix": {
        "twitter": false,
        "reddit": false,
        "github": false,
        "instagram": false
    }
}

$ usercheck data/samples.txt -fj
[
    "this_pseudo_dont_existWEEUFHG"
]

$ usercheck data/samples.txt -fcj
{
    "jack": {
        "twitter": false,
        "reddit": false,
        "github": false,
        "instagram": false
    },
    "this_pseudo_dont_existWEEUFHG": {
        "twitter": true,
        "reddit": true,
        "github": true,
        "instagram": true
    },
    "gooogle": {
        "twitter": false,
        "reddit": false,
        "github": false,
        "instagram": false
    }
}

```

Async (work only for file)
```
$ cat data/samples_medium.txt | wc -l
21

$ time `usercheck data/samples_medium.txt -fc > /dev/null`
real	1m9.380s

$ time `usercheck data/samples_medium.txt -fca > /dev/null`
real	0m6.827s
```

Num Threads

The list of username of size `N` is divided in `X` chunks each of size `N / num_threads`.\
Default is 50
```
$ time usercheck data/samples_medium.txt -fcad
Creating 20 chunks of 1.0 usernames
[...]
real	0m6.146s

$ time usercheck data/samples_medium.txt -fcad -n 4
Creating 4 chunks of 5.0 usernames
[...]
real	0m19.618s
```

Progress
```
$ usercheck data/samples_medium.txt -fcap
  0%|                                                                                           | 0/20 [00:00<?, ?it/s]
  5%|████▏                                                                              | 1/20 [00:04<01:31,  4.81s/it]
 45%|█████████████████████████████████████▎                                             | 9/20 [00:05<00:06,  1.77it/s]
100%|██████████████████████████████████████████████████████████████████████████████████| 20/20 [00:05<00:00,  3.92it/s
```

## Services
- Twitter
- Reddit
- Github
- Instagram

## Use in python

## TODO
> More services\
> Random user agent\
> Move services from __init__ to class\
> Option to select services\
> Option to save to file