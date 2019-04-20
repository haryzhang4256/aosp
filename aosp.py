import xml.dom.minidom
import os
import sys
from subprocess import call
import argparse
from multiprocessing.dummy import Pool as ThreadPool 
cmd_git = 'git '
cmd_branch = 'branch '

url = "https://aosp.tuna.tsinghua.edu.cn/"
dot_git = ".git" 


class Config(object):
    def __init__(self):
        self.pair = {}


def readConfig(path) :
    '''
    读取manifest目录下面的default.xml文件
    1. branch 或者tag信息
    2. name 和path 信息
    '''
    print('read config file : ' + path)
    dom = xml.dom.minidom.parse(path)
    root = dom.documentElement
    if not os.path.exists(path):  
        print(path + 'is not find')
        return
    config = Config()    
    for node in root.getElementsByTagName('default'):
        revision = node.getAttribute('revision')
        last = revision.rfind("/")
        config.branch = revision if last == -1 else revision[last+1:]
    for node in root.getElementsByTagName("project"):  
        config.pair[node.getAttribute("name")] = node.getAttribute("path")
    return config       

def init():
    #1. mkdir init & cd init
    print(os.getcwd())
    temp_path = 'repo'
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    os.chdir(temp_path)
    if not os.path.exists('manifest'):
        call('git clone https://aosp.tuna.tsinghua.edu.cn/platform/manifest.git'.split())
    os.chdir('manifest')
    call('git pull'.split())
    path =  os.path.join(os.getcwd() , 'default.xml')
    print(path)
    return path

def filter(config, args):
    test = ['test', 'cts', 'pathtools/testdata']
    apps = ['packages/apps']
    build = ['build', 'device', 'hardware', 'prebuilts']
    core = 'frameworks'

    justCore = False
    deletekeys = []

    if args.all:
        # exclude test folder
        exclude = test
    elif  args.build :
        # exclude test and apps
        exclude = test + apps
    elif args.main :
        # exclude test and apps and build
        exclude = test + apps + build 
    else :
        justCore = True  


    if justCore:
        print('get only framework source code')
        for url in config.pair:
            if not config.pair[url].startswith(core):
                deletekeys.append(url)
    else :
        exclude = test + apps + build
        print(exclude)
        for key in exclude:
            for url in config.pair:
                if config.pair[url].startswith(key):
                    deletekeys.append(url)
                    continue
    

    for url in deletekeys:
        print('del ', config.pair[url])
        del config.pair[url]
        

    return config


def process(item):
    print(item)
    call(item.split())

def fetch(config):
    pullCmds = []
    for key in config.pair:
        path = config.branch + '/' + config.pair[key]
        cmd = 'git clone ' + url + key + '.git ' + path + ' -b ' + config.branch + ' --depth 1'

        if os.path.exists(path):
            print(config.pair[key], ' exists')
        else :
            print(cmd)
            pullCmds.append(cmd)

    pool = ThreadPool()
    pool.map(process, pullCmds)
    pool.close()
    pool.join()
    print(os.getcwd())        
        

def aosp_pull(args):
    print('aosp_pull')
    xmlPath = init()
    os.chdir('../..')
    print(os.getcwd())
    print('path :' + xmlPath)
    config = readConfig(xmlPath)
    if not config:
        print('read xml failed')
    else:
        print('branch : ' + config.branch)
        if not os.path.exists(config.branch) :
            os.makedirs(config.branch)
        # for key in config.pair:
        #     print('name:' + key + " path: " + config.pair[key])
        fetch(filter(config, args))

def aosp_checkout(args):
    print(args.branch)
    print(args.remote)
   
    init()

    if args.remote:
        cmd = 'git checkout -b ' + args.branch + ' origin/' + args.branch 
    else :
        cmd = 'git checkout ' + args.branch 

    print(cmd)     
    call(cmd.split())
    os.chdir('../..')  

def aosp_init(args):
    init()
    os.chdir('../..')

def aosp_branch(args):
    print(args)
    print('aosp_branch')
    init()
    if args.all:
       cmd = 'git branch --all'
    else :
       cmd = 'git branch'
    call(cmd.split())
    os.chdir('../..')

if __name__ == "__main__":
 
    parser = argparse.ArgumentParser(description='this tools can fast get android source code')

    subParsers = parser.add_subparsers(help='pull android source code')

    parser_pull = subParsers.add_parser('pull', help='pull just only framework source code, if you want pull build/extenal code you should use arg -build, or if you want pull other main code(exclude apps and test) you should use arg -main, if you want pull all source code you should use arg -all')
    parser_pull.set_defaults(func=aosp_pull)
    parser_pull.add_argument("-all", "--all", help="pull all android source code, exclude test repo",
                    action="store_true")
    parser_pull.add_argument("-main", "--main", help="pull main android source code, exclude test and apps and build repo",
                    action="store_true")
    parser_pull.add_argument("-build", "--build", help="pull build android source code, exclude test and apps repo",
                    action="store_true")                


    parser_branch = subParsers.add_parser('branch', help='show current branch, also can show remote all branch or tag with argument -all')
    parser_branch.set_defaults(func=aosp_branch)
    parser_branch.add_argument("-all", "--all", help="show remote repo all branch",
                    action="store_true")

    parser_checkout = subParsers.add_parser('checkout', help='checkout branch, also can checkout remote branch with argument -r')
    parser_checkout.set_defaults(func=aosp_checkout)
    parser_checkout.add_argument("branch", type=str, help="checkout local branch")
    parser_checkout.add_argument("-r", "--remote", help="checkout remote branch", action="store_true") 


    parser_init = subParsers.add_parser('init', help='if you want checkout specified branch, you should first init repo, thren checkout branch , pull the code the end') 
    parser_init.set_defaults(func=aosp_init)                        
   

    args = parser.parse_args()
    args.func(args)


    
