from colorama import Fore, Style
from langgraph.graph.state import CompiledStateGraph
import os
from rich.console import Console
from rich.markdown import Markdown

class AgentConsole:
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

        rich_console = Console(soft_wrap=True)
        while True:
            self.user_input = input("Você: ")
            output = self.graph.invoke({"user_input": self.user_input})
            response = output["final_response"]
            print('----------------------------------------------------------------------------------------')
            rich_console.print(Markdown("**Chatbot:**\n"))
            rich_console.print(Markdown(response))
