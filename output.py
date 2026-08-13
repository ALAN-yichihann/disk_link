from colorama import init, Fore, Style

init() # 初始化colorama

def print_info(msg, end='\n'):
    """输出提示"""
    print(Fore.GREEN + msg + Style.RESET_ALL, end=end)
    # print(msg)

def print_warning(msg):
    """输出警告"""
    print(Fore.YELLOW + msg + Style.RESET_ALL)
    # print(msg)

def print_error(msg):
    """输出错误"""
    print(Fore.RED + msg + Style.RESET_ALL)
    # print(msg)

def input_confirm(msg):
    """加粗字体询问"""
    return input(Style.BRIGHT + msg + Style.RESET_ALL)
    # return input(msg)
