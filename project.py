#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: n0t4u
# Version: 0.2.2

# Imports
import argparse
from termcolor import colored
import ipaddress
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
            os.mkdir(os.path.join(rootDir, "tools", d))
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
    count = 0
    for root, dirs, files in os.walk(rootDir, topdown=False, followlinks=False):
        for d in dirs:
            directories.append(os.path.join(root, d))
    logging.info(colored("[INFO] Directories: ", "cyan") + str(directories))
    for d in directories:
        if len(os.listdir(d)) == 0:
            os.rmdir(d)
            count += 1
    return count


def defineScopeFile(rootDir, scope, reset):
    print("DefineScopeFile", scope, reset, sep="\t")
    scopeDict = {}
    with open(scope, "r", encoding="utf-8") as file:
        for asset in file:
            asset = asset.rstrip("\n")
            try:
                ipaddress.ip_address(asset)
            except ValueError:
                if re.search(r'^http[s]?:\/\/', asset, re.I):
                    scopeDict[asset] = "URL"
                elif re.search(r'[\S]+\.[\S]{2,}$', asset, re.I):
                    scopeDict[asset] = "domain"
                else:
                    scopeDict[asset] = "unknown"
            else:
                scopeDict[asset] = "IP"
    with open(os.path.join(rootDir, ".project_info"), 'r+') as file:
        info = json.load(file)
        if reset:
            info["scope"] = scopeDict
        else:
            info["scope"] = scopeDict | info["scope"]
        file.seek(0)
        json.dump(info, file, indent=4)
        file.truncate()
    return


def defineScope(rootDir, scope, reset):
    print("DefineScope", scope, reset, sep="\t")
    scopeDict = {}
    scope = scope.split(",")
    for asset in scope:
        try:
            ipaddress.ip_address(asset)
        except ValueError:
            if re.search(r'^http[s]?:\/\/', asset, re.I):
                scopeDict[asset] = "URL"
            elif re.search(r'[\S]+\.[\S]{2,}$', asset, re.I):
                scopeDict[asset] = "domain"
            else:
                scopeDict[asset] = "unknown"
        else:
            scopeDict[asset] = "IP"
    with open(os.path.join(rootDir, ".project_info"), 'r+') as file:
        info = json.load(file)
        if reset:
            info["scope"] = scopeDict
        else:
            info["scope"] = scopeDict | info["scope"]
        file.seek(0)
        json.dump(info, file, indent=4)
        file.truncate()
    return


def parseScope(rootDir):
    try:
        with open(os.path.join(rootDir, ".project_info"), 'r+') as file:
            info = json.load(file)
            scope = info["scope"]
    except:
        print(colored("[!] Unable to find project_info file", "red"))
        sys.exit(0)
    else:
        ips, domains, urls, unknown = [], [], [], []
        for key, value in scope.items():
            if value == "IP":
                ips.append(key)
            elif value == "domain":
                domains.append(key)
            elif value == "URL":
                urls.append(key)
            else:
                unknown.append(key)
        # print(ips, domains, urls, unknown, sep="\n")
        return ips, domains, urls, unknown


def showCommands(commandList, ips, domains, urls, unknown, reset):
    print(colored("[*] Unit commands", "blue"))
    # print(commandList, scope, sep="\n")
    ipsString = ' '.join(ips)
    unitCommands = []
    groupCommands = []
    for command in commandList:
        if re.search(r'^#',command):
            logging.info(colored("[INFO] Command '%s' commented. Skipping." %command, "cyan"))
            continue
        if re.search(r'\$IP\$', command):
            for ip in ips:
                c = re.sub(r'\$IP\$', ip, command)
                print(c)
                unitCommands.append(c)
            if len(ips) > 1:
                groupCommand = "for $ip in %s; do %s;done" % (' '.join(ips), re.sub(r'\$IP\$', '$ip', command))
                groupCommands.append(groupCommand)
        elif re.search(r'\$DOM\$', command):
            for dom in domains:
                c = re.sub(r'\$DOM\$', dom, command)
                print(c)
                unitCommands.append(c)
            if len(domains) > 1:
                groupCommand = "for $dom in %s; do %s;done" % (' '.join(domains), re.sub(r'\$DOM\$', '$dom', command))
                groupCommands.append(groupCommand)
        elif re.search(r'\$URL\$', command):
            for url in urls:
                c = re.sub(r'\$URL\$', url, command)
                print(c)
                unitCommands.append(c)
            if len(urls) > 1:
                groupCommand = "for $url in %s; do %s;done" % (' '.join(urls), re.sub(r'\$URL\$', '$url', command))
                groupCommands.append(groupCommand)
        else:
            unitCommands.append(command)
            print(command)
    print(colored("[*] Group commands", "blue"))
    print('\n'.join(groupCommands))
    print(unitCommands, groupCommands)
    with open(os.path.join(rootDir, ".project_info"), 'r+') as file:
        info = json.load(file)
        if reset:
            info["commands"]["unit"] = unitCommands
            info["commands"]["group"] = groupCommands
        else:
            try:
                info["commands"]["unit"] = info["commands"]["unit"].extend(unitCommands)
                info["commands"]["group"] = info["commands"]["group"].extend(groupCommands)
            except:
                info["commands"]["unit"] = unitCommands
                info["commands"]["group"] = groupCommands
        file.seek(0)
        json.dump(info, file, indent=4)
        file.truncate()
    return


# Main
parser = argparse.ArgumentParser(description="Management tool for audit projects.")
optionGroup = parser.add_mutually_exclusive_group(required=True)
optionGroup.add_argument("--create", dest="create", help="Creates the structure of directories", nargs=2,
                         metavar=('CLIENT', 'PROJECT'))
optionGroup.add_argument("--clean", dest="clean", help="Removes empty files and/or directories", nargs=1,
                         choices=["dir", "files", "all"])
optionGroup.add_argument("--scope", dest="scope", help="Defines the scope of the audit.", nargs=1)
optionGroup.add_argument("-c", "--commands", dest="commands", help="Suggest commands based on the project",
                         action="store_true")

parser.add_argument("-d", "--dir", dest="rootDir",
                    help="Root directory to work. If not provided, current directory is used.", nargs=1)
parser.add_argument("--config", dest="config", help="Path to different configuration file.", nargs=1)
parser.add_argument("-v", "--verbose", dest="verbose", help="Verbose mode.", action="store_true")
parser.add_argument("--reset", dest="reset", help="Resets scope", action="store_true")

args = parser.parse_args()

if __name__ == '__main__':
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    rootDir = args.rootDir[0] if args.rootDir else os.getcwd()
    logging.info(colored("[INFO] Working on %s" % rootDir, "cyan"))
    configFile = args.config[0] if args.config else "%s/.config" % os.getcwd()
    logging.info(colored("[INFO] Configuration file path %s" % configFile, "cyan"))
    file = open(configFile, "r", encoding="utf-8")
    try:
        config = json.load(file)
    except json.decoder.JSONDecodeError as e:
        print(colored("[ERROR] Unable to parse configuration file. Use -v option for more information.", "red"))
        logging.info(e)
        sys.exit(0)

    logging.info(colored("[INFO] Configuration file: ", "cyan") + str(config))
    if args.create:
        print(colored("[*] Creating project structure ...", "blue"))
        try:
            createStructure(rootDir, config["mainDirs"], config["tools"])
        except KeyError:
            tools = []
            createStructure(rootDir, config["mainDirs"], tools)
        finally:
            copyFiles(rootDir, args.create[0], args.create[1], config["files"])
    elif args.clean:
        print(colored("[*] Cleaning project ...", "blue"))
        clean(rootDir, args.clean[0])
    elif args.scope:
        print(colored("[*] Setting project scope ...", "blue"))
        print(args.scope)
        if os.path.isfile(args.scope[0]):
            defineScopeFile(rootDir, args.scope[0], args.reset)
        else:
            defineScope(rootDir, args.scope[0], args.reset)
    elif args.commands:
        print(colored("[*] Showing commands for this project ...", "blue"))
        ips, domains, urls, unknown = parseScope(rootDir)
        showCommands(config["commands"], ips, domains, urls, unknown, args.reset)
    else:
        print("Doing nothing!")
        sys.exit(0)
