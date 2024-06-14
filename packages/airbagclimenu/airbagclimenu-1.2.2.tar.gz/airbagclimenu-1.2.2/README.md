# AirBag CLI Menu
CLI menu module for python3 by AirBag65

## Getting started
To use the module you should be working within a virtual environment, or ```venv``` for short. If you don't already have one set up you can run one of these commands:

Windows: 
```Bash
python -m venv <name-of-venv>
```
MacOS / Linux: 
```Bash
python3 -m venv <name-of-venv>
```

When your ```venv``` is ready, you enter it with the following command:

Windows:
```bat
<name-of-venv>\Scripts\activate
```
MacOS / Linux: 
```Bash
source <name-of-venv>/bin/activate
```

When you have activated the virtual environment and running from within it, you can install ```airbagclimenu```, with one of the following commands: 

Windows:
```bat
pip3 install airbagclimenu
```
MacOS / Linux: 
```Bash
pip install airbagclimenu
```

## Usage
Make sure to use this exact ```import``` statement for the following to work:
```Python
from airbagclimenu import Menu
```
To create and run the menu, you do as follows:
```Python
menu = Menu.CLIMenu("Title")
menu.run()
```
The construcor for the menu takes one mandatory argument to act as the title of the menu. You can see an example of this at the bottom of this page. It does also take  
an optional argument ```quit_stmt``` which is ```True``` by default. It provides an option to quit the menu that you don't have to add yourself. 
When the quit option is present, the menu will run indefinitly, meaning you don't have to restart it for each time after choosing an option. This loop is however not present if 
the quit statement is not there. If you which not to have the quit statement, you simply pass the argument ```False``` into the construcor when creating the object.


Additionally, when there is an active quit statement all added submenus will also have the option to go back to the previous page. See example at the bottom of this page.


The ```run``` method also takes an optional argument ```clear_screen```, which determines whether the screen should clear after each option. It's default value is
```True``` but can easily be switched of by giving the argument ```False``` to the ```run``` method.


To add alternatives in the menu you have two options. You can add a function that will execute when that option is chosen, or you can add a submenu, which reveals more options when chosen. 
### add_menu_option(menu_option: MenuOption)
This method takes one parameter which should be of type ```MenuOption```. See example usecase below:
```Python
menu = Menu.CLIMenu("Title")
# You can add a submenu directly by creating it as a parameter like this
menu.add_menu_option(Menu.MenuOption("Submenu 1"))
# Or you can create it as a variable and use the variable as the parameter
option2 = Menu.MenuOption("Submenu 2")
menu.add_menu_opntion(option2)
```
The second option is recommended in order to be able to add even more submenus and functions to the submenu.

### add_func(functionality, title: str)
This method takes two parameters. The first paramter is a function object, and the second is the title that will be displayed in the menu. See usecase below:
```Python
menu = Menu.CLIMenu("Title")
def greet():
    print("Hello There!")

menu.add_func(greet, "Say Hello")
```
As of version 1.1.0 the function used does now support parameters. If the function does not take arguments, it will just run it directly. If it however does take arguments, you will
be prompted to enter these when you try to run the function via the menu. It will look like this: 
```
--- Args ---
argument_1: <value of arugment>
argument_2: <value of argument>
------------ 
```
> The name of the argument will be displayed instead of ```argument_1``` etc.

## Example Program
```Python
from airbagclimenu import Menu
import random

menu = Menu.CLIMenu("Example Menu")

def roll_die():
    val = random.randint(1,6)
    print(f"You rolled a {val}")

def greet1():
    print("Hello There!")

def greet_all():
    print("Hello, World!")

menu_op = Menu.MenuOption("Greetings")
menu_op.add_func(greet1, "Greet person")
menu_op.add_func(greet_all, "Greet everyone")

menu.add_menu_option(menu_op)
menu.add_func(roll_die, "Roll A Die")
menu.run()
```
The output of this program will be the following:
```
--- Example Menu ---
[1] Greetings
[2] Roll A Die
[3] Quit
: 1
```
The 1st option was chosen here so the program enters this state:
```
--- Greetings ---
[1] Greet person
[2] Greet everyone
[3] Back
: 1
Hello There!
```

### If you like my work
Feel free to send a small donation via the [GitHub page](https://github.com/Airbag65/CLI-Menu) if you like my work! But by all means, DO NOT feel presured to do so!!
![paypal qr code](https://github.com/Airbag65/CLI-Menu/blob/main/qrcode.png)
