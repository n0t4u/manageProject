# manageProject

Simple Python script to create and manage your hacking projects based on templates

## Installation
```sh
$ git clone https://github.com/n0t4u/manageProject.git
$ cd manageProject
$ python3 -m pip install -r requirements.txt
$ chmod +x project.py 

#Optional
echo 'alias project="python3 PATH/TO/FILE/project.py"' >> $HOME/.zshrc
```
## Setup
To work properly, this tool works with templates and configuration files. If it is the first time using it, you should take into account the following points:
- All the templates or files you use in every audit must be placed in the Templates folder.
- Use **$CLIENT$** and **$PROJECT$** reserved words in your file names to change the name of the client or project according to your needs.
- Modify **.config** file to define:
  - Your project tree ("mainDirs").
  - The location of every file ("files").
  - The common tools ("tools")
  - The commands to auto-generate. Reserved words:
    - **$IP$**
    - **$DOM$**
    - **$URL$**
    - **$PATH$**

## Usage
**NOTE**. The following commands are meant to be executed in the project work directory. If not, the work directory must be defined with -d/--dir option.
### Create project
```sh
$ python3 project.py --create CLIENT PROJECT
```

### Define scope
Define the scope of your audit, 
```sh
$ python3 project.py --scope <FILE> | <A1,A2,A3,...>
```

### Generate commands
Automatically generate commands that you always use in your audits and execute them easily. 
```sh
$ python3 project.py -c
```

### Clean project
When the project is done, remove empty folders, files or both things from the generated tree.
```sh
$ python3 project.py --clean <dir>|<files>|<all>
```

### Help
Check help option to se more options and information.
```sh
$ python3 project.py --help
```

## Author 
n0t4u

## License
GNU General Public License Version 3