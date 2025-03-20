from colorama import Fore, Style
from langgraph.graph.state import CompiledStateGraph
import os

class Console:
    def __init__(self, graph: CompiledStateGraph):
        self.graph = graph
        self.user_input = ''

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):    
        self.clear_terminal()

        print(Fore.GREEN +"""
        ==================================================================
             █████╗ ██████╗██████████╗   ██████████╗     █████╗  ██╗
            ██╔══████╔════╝██╔════████╗  ██╚══██╔══╝    ██╔══██╗ ██║
            █████████║  ████████╗ ██╔██╗ ██║  ██║       ███████║ ██║
            ██╔══████║   ████╔══╝ ██║╚██╗██║  ██║       ██╔══██║ ██║
            ██║  ██╚██████╔█████████║ ╚████║  ██║       ██║  ██████║
            ╚═╝  ╚═╝╚═════╝╚══════╚═╝  ╚═══╝  ╚═╝       ╚═╝  ╚═╚═╚═╝
        ==================================================================
        """ + Style.RESET_ALL)

        while True:
            self.user_input = input("Você: ")
            output = self.graph.invoke({"user_input": self.user_input})
            print("Chat: " + output["final_response"])