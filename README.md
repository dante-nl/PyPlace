# PyPlace
## Manage your Python files

PyPlace is a simple tool that you can use to open and install your Python files. PyPlace has a built-in store that allows you to easily install new applications with ease. It also has support for an updater, which allows you to easily update the apps that you have installed via the updater.

It has been desgined to be very easy to use so it is great to use for everyone, it doen't matter if you are a beginner or a long time user of Python.

## Installation

It can be easily installed one simple command that you can paste in to the Terminal (macOS/Linux) or Command Prompt (Windows). This will make a new directory called "PyPlace" and it will install the latest version from [the website](https://pyplace.dantenl.com/pyplace-latest.py).

> **NOTE:** You must have Python 3.x.x installed! You can do that via [the Python website](https://python.org)

If you are using **macOS or Linux** use the following command:

```
mkdir PyPlace && cd PyPlace && curl -o pyplace.py https://pyplace.dantenl.com/pyplace-latest.py
```

If you are on **Windows** use the following command:
```
mkdir PyPlace ; cd PyPlace ; (New-Object System.Net.WebClient).DownloadFile("https://pyplace.dantenl.com/pyplace-latest.py", "pyplace.py")
```

After you have installed it, simply run eithern `python3 pyplace.py` or `python pyplace.py`
## How to install applications?

When you start up PyPlace, you will be at a menu that looks something like this (might be different in your language):
```
[1] Open a PyPlace app
[2] Add a PyPlace app
[3] Check for app updates
[4] Open settings
[e] Exit PyPlace
```

To install an app, you press `[2] Add a PyPlace app` and that will bring you to another menu, that will look similar to this:
```
[1] Link to Python file
[2] Download from PyPlace Store
[3] Download experiment
[4] Add local file
[c] Cancel
```

If you already have a direct link to your file, just enter `1` and enter this here! Note that the URL must end with .py otherwise it will not recognise it as a valid Python file. 

You can also download from the PyPlace store, this is the easiest. Just enter `2` to download it from the PyPlace Store. This will give you a list of free applications that you can install for PyPlace! All these apps support the built-in updater as well, so you can easily access the latest version of them.

The third option is to download experiments. To access it, enter `3` and it will show some experiments. This feature is largely unused but it was used as a way to kind of test some beta functions. You can still download an old version of PyPlace though.

The fourth and last option is used to add a local file in the current directory to PyPlace. This does not install anything, it just adds that app to the files that PyPlace can open.

There is one other way that can be used to install an application, and that is to use parameters. You can install this simple "Hello world" program from [this URL](https://raw.githubusercontent.com/dante-nl/PyPlace/main/Testing%20Files/hw.py). It is very easy to install a program from parameters.

1. Open Terminal or Command Prompt and navigate to your PyPlace folder with `cd`
2. Depending on what command you use for Python, it might either be `python` or `python3`. You should execute PyPlace like this `<python command> pyplace.py https://raw.githubusercontent.com/dante-nl/PyPlace/main/Testing%20Files/hw.py`. You may need to replace `pyplace.py` if your PyPlace file is called something else.
3. Confirm that you want to install this file and you're done!
