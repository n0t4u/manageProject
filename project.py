#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: n0t4u
# Version: 0.2.1

# Imports
import argparse
from termcolor import colored
import json
import logging
import os
import re
import shutil
import sys


# Variables

# Functions

def createStructure(rootDir, dirs, tools):
    print(rootDir, dirs, tools)
    os.makedirs(rootDir) if not os.path.exists(rootDir) else None
    for d in dirs:
        try:
            os.mkdir(os.path.join(rootDir, d))
        except FileExistsError as e:
            logging.info(colored("[INFO] %s. Skipping..." % e, "cyan"))
    os.makedirs(os.path.join(rootDir, "tools")) if not os.path.exists(os.path.join(rootDir, "tools")) else None
    for d in tools:
        try:
            os.mkdir(os.path.join(rootDir,"tools", d))
        except FileExistsError as e:
            logging.info(colored("[INFO] %s. Skipping..." % e, "cyan"))
    return


def copyFiles(rootDir, client, project, files):
    logging.info(colored("[INFO] Client: %s\tProject: %s" % (client, project), "cyan"))
    logging.info(colored("[INFO] Files: %s" % files, "cyan"))
    src = os.path.join("templates", ".project_info")
    dst = os.path.join(rootDir, ".project_info")
    print(src, dst, sep="\t")
    shutil.copy2(src, dst)
    with open(dst, 'r+') as f:
        info = json.load(f)
        info["client"] = client
        info["project"] = project
        f.seek(0)
        json.dump(info, f, indent=4)
        f.truncate()
    for folder, file in files.items():
        for f in file:
            src = os.path.join("templates", f)
            newName = re.sub(r'CLIENT', client, f, re.I)
            newName = re.sub(r'PROJECT', project, newName, re.I)
            dst = os.path.join(rootDir, folder, newName)
            try:
                shutil.copy2(src, dst)
            except FileNotFoundError as e:
                print(colored("[!] File %s not found on templates folder" % f, "yellow"))
                logging.info(colored("[INFO] %s" % e, "cyan"))
            print(folder, file)

    return


def clean(rootDir, option):
    filesCleaned = 0
    dirCleaned = 0
    if option == "all":
        filesCleaned = cleanFiles(rootDir)
        dirCleaned = cleanDirs(rootDir)
    elif option == "dir":
        dirCleaned = cleanDirs(rootDir)
    elif option == "files":
        filesCleaned = cleanFiles(rootDir)
    else:
        sys.exit(0)
    print(colored("[»] Project cleaned. %d directories and %d empty files were removed." % (dirCleaned, filesCleaned),
                  "green"))
    return


def cleanFiles(rootDir):
    allFiles = []
    count = 0
    for root, dirs, files in os.walk(rootDir, topdown=False, followlinks=False):
        for file in files:
            allFiles.append(os.path.join(root, file))
    logging.info(colored("[INFO] Files: ", "cyan") + str(allFiles))
    for file in allFiles:
        if os.path.getsize(file) == 0:
            os.remove(file)
            count += 1
    return count


def cleanDirs(rootDir):
    directories = []
    count=0
    for root, dirs, files in os.walk(rootDir, topdown=False, followlinks=False):
        for d in dirs:
            directories.append(os.path.join(root,d))
    logging.info(colored("[INFO] Directories: ","cyan") + str(directories))
    for d in directories:
        if len(os.listdir(d)) == 0:
            os.rmdir(d)
            count += 1
    return count


def defineScope(scope):
    return


def showCommands():
    return


# Main
parser = argparse.ArgumentParser(description="Management tool for audit projects.")

optionGroup = parser.add_mutually_exclusive_group(required=True)
optionGroup.add_argument("--create", dest="create", help="Creates the structure of directories", nargs=2,
                         metavar=('CLIENT', 'PROJECT'))
optionGroup.add_argument("--clean", dest="clean", help="Removes empty files and/or directories", nargs=1,
                         choices=["dir", "files", "all"], default="directories")
optionGroup.add_argument("--scope", dest="scope", help="Defines the scope of the audit.", nargs=1)
optionGroup.add_argument("-c", "--commands", dest="commands", help="Suggest commands based on the project",
                         action="store_true")

parser.add_argument("-d", "--dir", dest="rootDir",
                    help="Root directory to work. If not provided, current directory is used.", nargs=1)
parser.add_argument("--config", dest="config", help="Path to different configuration file.", nargs=1)
parser.add_argument("-v", "--verbose", dest="verbose", help="Verbose mode.", action="store_true")

args = parser.parse_args()

if __name__ == '__main__':
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    rootDir = args.rootDir[0] if args.rootDir else os.getcwd()
    logging.info(colored("[INFO] Working on %s" % rootDir, "cyan"))
    configFile = args.config[0] if args.config else "%s/.config" % os.getcwd()
    logging.info(colored("[INFO] Configuration file path %s" % configFile, "cyan"))
    file = open(configFile, "r", encoding="utf-8")
    config = json.load(file)
    logging.info(colored("[INFO] Configuration file: ", "cyan") + str(config))
    if args.create:
        try:
            createStructure(rootDir, config["mainDirs"], config["tools"])
        except KeyError:
            tools=[]
            createStructure(rootDir, config["mainDirs"], tools)
        finally:
            copyFiles(rootDir, args.create[0], args.create[1], config["files"])
    elif args.clean:
        clean(rootDir, args.clean[0])
    elif args.scope:
        defineScope()
    elif args.commands:
        showCommands()
    else:
        sys.exit(0)
