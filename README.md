# Solitaire Game
> The famous solitaire game using python libraries for graphical environment

## Table of contents
* [General Info](#general-information)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Setup](#setup)
* [How to run](#how-to-run)
* [Acknowledgements](#acknowledgements)

## General Information
The project is an equivalent realization of the well-known game of Klondlike Solitaire using cross-platform set of Python modules for computer graphics and sound libraries. The goal is to turn the entire deck into stacks and if this is achieved, the Solitaire game is won. 
The implementation is based on 3 main axes:
1. Menu Scene
3. Other scenes (Win/Lose/Τransitional)
4. Game/Play environment

## Features
* Graphical design of components
* Introductory/final scenes
* Multimedia effects
* Hint buttons



## Prerequisites 
1. Install python[^1] environment. The instalation is easy either on Windows or Linux
2. Install pygame[^2] modules
3. Install Python IDE
    * This implementation is made in pyCharm

### Install Python (Windows)
* https://www.python.org/downloads/
* Link for the Windows installer python-XXX.msi file where XXX is the version you need to install. 
* Update the PATH variable 

### Install Python (Linux)
1. Update repositories lists and supporting softwares

```
$ sudo apt update
$ sudo apt install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt update
```

2. Install main package
```
$ sudo apt install pythonXXX
``` 

where XXX version installed[^1]

3. Verify install completion

```$ python --version```

### Install pygame (Windows)
1. On any windows shell
```
python --version
pip install pygame
```
2. Check the PyGame is working

```
import pygame
```

### Install pygame (Linux)
1. On terminal, first make sure you are using latest version of python[^3] with 

```$ python3 –version```, 

then
```
$ sudo apt-get install python3-pygame
```


2. Check PyGame is working with python

```
python 3
pygame 1.9.6
```




## How to run
### Linux
1. Open the terminal and go to home directory
`cd ~`
2. Navigate the directory of the project
3. Environment `pygame-1.9.6`
4. Run `Solitaire.py`

### PyCharm
1. Insert folder in PyCharm workshop
2. File->Settings->Project->Project Interpreter
3. Tap + and search PyGame
4. Install packages
    * pip install python
    * pip install pygame
    * pip install pyautogui
    * pip install pil (or pillow)
5. Run .py

### venv
1. Create virtual environment 
`python -m venv /Solitaire.py/venv`
2. Activate
`\Solitaire.py\venv\Scripts\activate`
3. Install packages
    * pip install python
    * pip install pygame
    * pip install pyautogui
    * pip install pil (or pillow)
4. pip install -r requirements.txt



## Setup
![12](https://user-images.githubusercontent.com/22920222/154859827-37af8072-1a45-45c3-bf6e-2b8c772f7e6a.png)








## Acknowledgements
- This project was created for the requirements of the lesson Autonomous Agents
- The implementation was influenced by [Raspigame](https://books.google.gr/books?id=RovJDQAAQBAJ&pg=PA173&lpg=PA173&dq=raspigame.py&source=bl&ots=BeWHfIuIbB&sig=ACfU3U0RK-qHlvyaiSaM7DxoRs3lI3AL5w&hl=en&sa=X&ved=2ahUKEwjv8Ku66JP2AhViSvEDHbmcDooQ6AF6BAgCEAM#v=onepage&q=raspigame.py&f=false) for creating basic games.

[^1]: Our version was Python3.8
[^2]: PyGame is only supported python 3.7.7 or higher version
[^3]: Verify you are using pip
