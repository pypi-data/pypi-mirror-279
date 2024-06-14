import os
import time 
import inspect
import types


class IllegalArgumentError(ValueError):
    pass

class MenuOption:
    pass

class MenuOption:
    def __init__(self, title: str):
        self.back_arg_set = False
        self.title = title
        self.menu_options = {}

    def add_menu_option(self, menu_option: MenuOption) -> None:
        if not isinstance(menu_option, MenuOption):
            raise IllegalArgumentError("Argument must be of type 'CLIMenu'")
        self.menu_options[len(self.menu_options) + 1] = menu_option

    def add_func(self, functionality, title: str):
        if not isinstance(functionality, types.FunctionType) and not (str(type(functionality)) == "<class 'method'>"):
            raise IllegalArgumentError("Argument must be of type 'Function'")
        self.menu_options[len(self.menu_options) + 1] = [title, functionality]

    def __add_back_option(self):
        def go_back():
            return
        if not self.back_arg_set:
            self.add_func(go_back, "Back")
            self.back_arg_set = True

    def run(self, back_stmt, clear_screen = True):
        if back_stmt:
            self.__add_back_option()
        if clear_screen:
            os.system("cls" if os.name == "nt" else "clear")
        print(f"--- {self.title} ---")
        for key, val in self.menu_options.items():
            if isinstance(val, MenuOption):
                print(f"[{key}] {val.title}")
            else:
                print(f"[{key}] {val[0]}")
        choice = int(input(": "))
        if choice not in self.menu_options.keys():
            print("Not a valid option")
            return
        chosen_option = self.menu_options[choice]
        if isinstance(chosen_option, MenuOption):
            chosen_option.run(clear_screen)
        else:
            if inspect.getfullargspec(chosen_option[1]).args:
                print("--- Args ---")
                args_list = []
                for arg in inspect.getfullargspec(chosen_option[1]).args:
                    given_arg = input(f"{ arg }: ")
                    if int(given_arg):
                        given_arg = int(given_arg)
                    elif float(given_arg):
                        given_arg = float(given_arg)
                    args_list.append(given_arg)
                print("------------")
                chosen_option[1](*args_list)
            else:
                chosen_option[1]()
            time.sleep(1)


class CLIMenu:
    def __init__(self, title, quit_stmt = True):
        self.quit_stmt = quit_stmt
        self.menu_options = {}
        self.title = title

    def add_menu_option(self, menu_option: MenuOption) -> None:
        if not isinstance(menu_option, MenuOption):
            raise IllegalArgumentError("Argument must be of type 'CLIMenu'")
        self.menu_options[len(self.menu_options) + 1] = menu_option

    def add_func(self, functionality, title: str):
        if not isinstance(functionality, types.FunctionType) and not (str(type(functionality)) == "<class 'method'>"):
            raise IllegalArgumentError("Argument must be of type 'Function'")
        self.menu_options[len(self.menu_options) + 1] = [title, functionality]

    def run(self, clear_screen = True) -> None:
        if self.quit_stmt:
            self.menu_options[len(self.menu_options) + 1] = ("Quit", "")
            _quit = self.quit_stmt
            while _quit:
                if clear_screen:
                    os.system("cls" if os.name == "nt" else "clear")
                print(f"--- {self.title} ---")
                for key, val in self.menu_options.items():
                    if isinstance(val, MenuOption):
                        print(f"[{key}] {val.title}")
                    else:
                        print(f"[{key}] {val[0]}")
                choice = int(input(": "))
                if choice not in self.menu_options.keys():
                    print("Not a valid option")
                    _quit = False
                chosen_option = self.menu_options[choice]
                if isinstance(chosen_option, MenuOption):
                    chosen_option.run(self.quit_stmt ,clear_screen)
                elif isinstance(chosen_option, tuple):
                    print("Quitting")
                    _quit = False
                else:
                    if inspect.getfullargspec(chosen_option[1]).args:
                        print("--- Args ---")
                        args_list = []
                        for arg in inspect.getfullargspec(chosen_option[1]).args:
                            given_arg = input(f"{ arg }: ")
                            if int(given_arg):
                                given_arg = int(given_arg)
                            elif float(given_arg):
                                given_arg = float(given_arg)
                            args_list.append(given_arg)
                        print("------------")
                        chosen_option[1](*args_list)
                    else:
                        chosen_option[1]()
                    time.sleep(1)

        else:
            if clear_screen:
                os.system("cls" if os.name == "nt" else "clear")
            print(f"--- {self.title} ---")
            for key, val in self.menu_options.items():
                if isinstance(val, MenuOption):
                    print(f"[{key}] {val.title}")
                else:
                    print(f"[{key}] {val[0]}")
            choice = int(input(": "))
            if choice not in self.menu_options.keys():
                print("Not a valid option")
                return
            chosen_option = self.menu_options[choice]
            if isinstance(chosen_option, MenuOption):
                chosen_option.run(self.quit_stmt, clear_screen)
            elif isinstance(chosen_option, tuple):
                print("Quitting")
                return
            else:
                if inspect.getfullargspec(chosen_option[1]).args:
                    print("--- Args ---")
                    args_list = []
                    for arg in inspect.getfullargspec(chosen_option[1]).args:
                        given_arg = input(f"{ arg }: ")
                        if int(given_arg):
                            given_arg = int(given_arg)
                        elif float(given_arg):
                            given_arg = float(given_arg)
                        args_list.append(given_arg)
                    print("------------")
                    chosen_option[1](*args_list)
                else:
                    chosen_option[1]()
                time.sleep(1)

