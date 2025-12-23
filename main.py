#!/usr/bin/env python3
"""DEMUX - Download & Upload File Manager"""

import os
from rich.console import Console
from rich.panel import Panel
from modules.selection import select_item

console = Console()

DEMUX_LOGO = """
 ██████╗ ███████╗███╗   ███╗██╗   ██╗██╗  ██╗
 ██╔══██╗██╔════╝████╗ ████║██║   ██║╚██╗██╔╝
 ██║  ██║█████╗  ██╔████╔██║██║   ██║ ╚███╔╝
 ██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║ ██╔██╗
 ██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗
 ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝
"""

MENU_ITEMS = [
    ("download", "Download"),
    ("upload", "Upload"),
    ("settings", "Settings"),
    ("exit", "Exit"),
]


def show_menu():
    """Display main menu with Rich panel and colored pick selection"""
    console.print(Panel(DEMUX_LOGO, style="bold yellow", expand=False))
    
    menu_labels = [item[1] for item in MENU_ITEMS]
    
    selected, index = select_item(
        menu_labels,
        "What would you like to do?",
        indicator="►"
    )
    
    return MENU_ITEMS[index][0]


def main():
    """Main application loop"""
    from modules.downloader import handle_download_cli
    from modules.uploader.core import handle_upload_cli
    from modules.settings import handle_settings_cli
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    while True:
        try:
            action = show_menu()
            
            if action == "exit":
                console.print("\n[bold red]Exiting DEMUX.[/bold red]")
                break
            elif action == "download":
                handle_download_cli(project_root)
            elif action == "upload":
                handle_upload_cli(project_root)
            elif action == "settings":
                handle_settings_cli(project_root)
            
            input("\nPress Enter to return to menu...")
        
        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting DEMUX.[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]")
            input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    main()
