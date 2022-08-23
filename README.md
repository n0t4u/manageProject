# manageProject

Simple Python script to create and manage your hacking projects :ghost: based on templates

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
1. Place all the templates and the files you use in every audit in the Templates folder (by default) or in another folder (must be specify everytime a project is created).
2. Use **`CLIENT`** and **`PROJECT`** reserved words in your file names to change the name of the client or project according to your needs. For example, PROJECT_CLIENT_report.docx.
3. Modify **.config** file to define:
   - Your project tree ("mainDirs"). **Important!!** Do not change tools directory as it is used in other functions of the program.
   - The location of every file ("files").
   - The common tools ("tools")
   - The commands to auto-generate. Reserved words:
     - **`$IP$`**
     - **`$DOM$`**
     - **`$URL$`**
     - **`$PATH$`**
     - **`$OTHER$`**

(This might sound a little bit tricky, you have a.config example file in the repository ;))

## Usage
**NOTE**. The following commands are meant to be executed in the project work directory. If not:
- The work directory must be defined with -d/--dir option.
- The config file must be defined with --config option.
- The templates directory must be defined with the -t/--templates option.

### Create project
```sh
$ python3 project.py --create CLIENT PROJECT
```

### Define scope
Define the scope of your audit, 
```sh
$ python3 project.py --scope <FILE> | <A1,A2,A3,...> [--reset]
```

### Generate commands
Automatically generate commands that you always use in your audits and execute them easily.
Using the --reset option you can add new commands or remove previous ones.
```sh
$ python3 project.py -c [--reset]
```

### Clean project
When the project is done, remove empty folders, files or both things from the generated tree.
```sh
$ python3 project.py --clean <dir>|<files>|<all>
```

### Remove project
Removes all the structure created for a project and all the files inside it. Ask for confirmation before execution,
```sh
$ python3 project.py --remove <project_directory>
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