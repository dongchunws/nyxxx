import os
from .services import gofile
from .services import vikingfiles
from .services import pixeldrain
from .services import catbox
from .services import buzzheavier
from .services import mixdrop
from ..settings import get_config
from ..selection import select_item, select_multiple
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn

console = Console()

def handle_upload_cli(project_root):
    """Handles the file upload flow (CLI version)"""
    console.print(Panel("Upload File", style="bold cyan", expand=False))
    
    try:
        download_dir = os.path.join(project_root, "downloads")
        
        # Get files from downloads directory
        files_in_downloads = []
        if os.path.exists(download_dir) and os.path.isdir(download_dir):
            files_in_downloads = sorted([f for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))])
        
        # File selection with arrow keys
        file_options = []
        
        if files_in_downloads:
            for f in files_in_downloads:
                file_size = os.path.getsize(os.path.join(download_dir, f))
                size_str = format_file_size(file_size)
                file_options.append((f, f"{f} ({size_str})"))
        
        file_options.append(("browse", "Browse for another file..."))
        
        if not file_options:
            console.print("[bold red]✗ No files available.[/bold red]")
            return
        
        selected_file, _ = select_item(
            [opt[1] for opt in file_options],
            "Select a file to upload:",
            indicator="►"
        )
        
        selected_idx = next(i for i, opt in enumerate(file_options) if opt[1] == selected_file)
        
        if file_options[selected_idx][0] == "browse":
            file_to_upload_path = input("Enter path to file: ").strip()
        else:
            file_to_upload_path = os.path.join(download_dir, file_options[selected_idx][0])
        
        if not file_to_upload_path or not os.path.exists(file_to_upload_path):
            console.print("[bold red]✗ Error: File not found.[/bold red]")
            return

        # Service selection with arrow keys
        available_services = ["Gofile", "Vikingfiles", "Pixeldrain", "Catbox", "Buzzheavier", "Mixdrop"]
        
        selected_services_raw = select_multiple(
            available_services,
            f"Select services to upload '{os.path.basename(file_to_upload_path)}' (Space to select, Enter to confirm):",
            indicator="►"
        )
        
        selected_services = selected_services_raw
        
        if not selected_services:
            console.print("[bold yellow]⚠ No services selected.[/bold yellow]")
            return

        config = get_config(project_root)
        results = []

        for service in selected_services:
            console.print(f"[bold]→ Uploading to {service}...[/bold]")
            success, message = (False, "Service not implemented or unknown error.")
            
            if service == "Gofile":
                success, message = gofile.upload(file_to_upload_path, config.get("gofile_api_key"))
            elif service == "Vikingfiles":
                success, message = vikingfiles.upload(file_to_upload_path, config.get("vikingfiles_api_key"))
            elif service == "Pixeldrain":
                success, message = pixeldrain.upload(file_to_upload_path, config.get("pixeldrain_api_key"))
            elif service == "Catbox":
                success, message = catbox.upload(file_to_upload_path, config.get("catbox_api_key"))
            elif service == "Buzzheavier":
                success, message = buzzheavier.upload(file_to_upload_path, config.get("buzzheavier_api_key"))
            elif service == "Mixdrop":
                mixdrop_email = config.get("mixdrop_email")
                mixdrop_api_key = config.get("mixdrop_api_key")
                success, message = mixdrop.upload(file_to_upload_path, mixdrop_email, mixdrop_api_key)
            
            results.append({"service": service, "success": success, "message": message})

        # Print summary table
        console.print(Panel("Upload Summary", style="bold yellow", expand=False))
        
        if results:
            table = Table(show_header=True, header_style="bold white")
            table.add_column("Service", style="cyan", width=15)
            table.add_column("Status", style="magenta", width=10)
            table.add_column("Result", style="white", width=50)
            
            for res in results:
                status = "✓ Success" if res['success'] else "✗ Failed"
                status_style = "green" if res['success'] else "red"
                msg = res['message'][:50] + "..." if len(res['message']) > 50 else res['message']
                table.add_row(res['service'], status, msg, style=status_style)
            
            console.print(table)
        
        console.print("[bold green]✓ All uploads complete.[/bold green]")

    except KeyboardInterrupt:
        console.print("[bold red]\n✗ Operation cancelled by user.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")


def format_file_size(bytes_size):
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f}TB"


def handle_upload(project_root, style):
    """Legacy function for compatibility"""
    handle_upload_cli(project_root)
