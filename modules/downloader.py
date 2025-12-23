import os
import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn

console = Console()

def handle_download_cli(project_root):
    """Handles the file download flow (CLI version)"""
    console.print(Panel("Download File", style="bold cyan", expand=False))
    
    try:
        url = input("\nEnter the direct URL of the file to download: ").strip()
        if not url:
            console.print("[bold red]✗ URL cannot be empty.[/bold red]")
            return

        default_filename = os.path.basename(url.split('?')[0]) or "downloaded_file"
        custom_filename = input(f"Enter custom filename (or press Enter for '{default_filename}'): ").strip()
        
        output_path = custom_filename if custom_filename else None
        download_file(project_root, url, output_path)

    except KeyboardInterrupt:
        console.print("[bold red]\n✗ Operation cancelled by user.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")


def download_file(project_root, url, output_path=None):
    download_dir = os.path.join(project_root, "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    if output_path is None:
        filename = os.path.basename(url.split('?')[0]) or "downloaded_file"
        output_path = os.path.join(download_dir, filename)
    elif not os.path.isabs(output_path):
        output_path = os.path.join(download_dir, output_path)

    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with Progress(
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            task = progress.add_task(f"[cyan]Downloading {os.path.basename(output_path)}", total=total_size)
            
            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        progress.update(task, advance=len(chunk))
        
        console.print(f"\n[bold green]✓ File downloaded successfully[/bold green]")
        console.print(f"[bold white]Location: {output_path}[/bold white]")
        
    except requests.exceptions.Timeout:
        console.print("[bold red]✗ Error: Request timeout[/bold red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]✗ Error downloading file: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]✗ An unexpected error occurred: {e}[/bold red]")


# Keep old function for compatibility
def handle_download(project_root, style):
    """Legacy function for compatibility"""
    handle_download_cli(project_root)
