# aosp
a fast get android source code util. support windows and mac platform.

### aosp command

```
usage: aosp.py [-h] {pull,branch,checkout,init} ...

this tools can fast get android source code

positional arguments:
  {pull,branch,checkout,init}
                        pull android source code
    pull                pull just only framework source code, if you want pull
                        build/extenal code you should use arg -build, or if
                        you want pull other main code(exclude apps and test)
                        you should use arg -main, if you want pull all source
                        code you should use arg -all
    branch              show current branch, also can show remote all branch
                        or tag with argument -all
    checkout            checkout branch, also can checkout remote branch with
                        argument -r
    init                if you want checkout specified branch, you should
                        first init repo, thren checkout branch , pull the code
                        the end
```

### aosp pull command:

```
usage: aosp.py pull [-h] [-all] [-main] [-build]

pull android source code , default clone only frameworks repo code .

optional arguments:
  -h, --help       show this help message and exit
  -all, --all      pull all android source code, exclude test repo
  -main, --main    pull main android source code, exclude test and apps and
                   build repo
  -build, --build  pull build android source code, exclude test and apps repo

```

### aosp branch command:

```
usage: aosp.py branch [-h] [-all]

show local android source branch, with arg --all will show all remote repo branch . 

optional arguments:
  -h, --help   show this help message and exit
  -all, --all  show remote repo all branch

```

### aosp checkout command:

```
usage: aosp.py checkout [-h] [-r] branch

checkout local repo branch, with arg -r will checkout and retrack to specfic branch .

positional arguments:
  branch        checkout local branch

optional arguments:
  -h, --help    show this help message and exit
  -r, --remote  checkout remote branch  

```  