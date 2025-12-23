import json
import os
from rich.console import Console
from rich.panel import Panel
from .selection import select_item

console = Console()

def get_config(project_root):
    config_path = os.path.join(project_root, "config.json")
    if not os.path.exists(config_path):
        default_config = {
            "gofile_api_key": None,
            "vikingfiles_api_key": None,
            "pixeldrain_api_key": None,
            "catbox_api_key": None,
            "buzzheavier_api_key": None,
            "mixdrop_email": None,
            "mixdrop_api_key": None
        }
        save_config(project_root, default_config)
        return default_config
    with open(config_path, 'r') as f:
        return json.load(f)

def save_config(project_root, config):
    config_path = os.path.join(project_root, "config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

def handle_settings_cli(project_root):
    """Handles API key settings (CLI version)"""
    console.print(Panel("Configure API Keys", style="bold cyan", expand=False))
    
    config = get_config(project_root)
    
    try:
        services = [
            "Gofile",
            "Vikingfiles",
            "Pixeldrain",
            "Catbox",
            "Buzzheavier",
            "Mixdrop",
            "Back"
        ]
        
        selected_service, _ = select_item(
            services,
            "Select a service to configure:",
            indicator="►"
        )
        
        if selected_service == "Back":
            return

        if selected_service == "Mixdrop":
            current_email = config.get("mixdrop_email") or "Not set"
            new_email = input(f"Enter API E-Mail for Mixdrop (current: {current_email}): ").strip()
            
            current_key = config.get("mixdrop_api_key") or "Not set"
            if isinstance(current_key, str) and len(current_key) > 4:
                current_key = f"****{current_key[-4:]}"
            
            new_key = input(f"Enter API Key for Mixdrop (current: {current_key}): ").strip()

            if new_email:
                config["mixdrop_email"] = new_email
            if new_key:
                config["mixdrop_api_key"] = new_key
            
            if new_email or new_key:
                save_config(project_root, config)
                console.print(f"[bold green]✓ Settings for {selected_service} updated.[/bold green]")
            else:
                console.print("[bold yellow]⚠ No changes made.[/bold yellow]")
        else:
            api_key_name = f"{selected_service.lower()}_api_key"
            
            current_key = config.get(api_key_name) or "Not set"
            if isinstance(current_key, str) and len(current_key) > 4:
                current_key = f"****{current_key[-4:]}"

            new_key = input(f"Enter API key for {selected_service} (current: {current_key}): ").strip()

            if new_key:
                config[api_key_name] = new_key
                save_config(project_root, config)
                console.print(f"[bold green]✓ API key for {selected_service} updated.[/bold green]")
            else:
                console.print("[bold yellow]⚠ No changes made.[/bold yellow]")

    except KeyboardInterrupt:
        console.print("[bold red]\n✗ Operation cancelled.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")


def handle_settings(project_root, style):
    """Legacy function for compatibility"""
    handle_settings_cli(project_root)
