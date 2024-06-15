"""
This module contains functions to print messages to the console.
"""
from rich import print
# Run `python -m rich.emoji` to get a list of all emojis that are supported


def error(msg: str) -> None:
    """
    Prints an error message to the console.
    """
    print(f"[bold red]Error[/bold red] {msg}")


def info(msg: str) -> None:
    """
    Prints an info message to the console.
    """
    print(f"[bold blue]Info[/bold blue] {msg}")


def success(msg: str) -> None:
    """
    Prints a success message to the console.
    """
    print(f"[green]Success[/green] {msg}")
