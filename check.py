import concurrent.futures
import subprocess
from pathlib import Path
import typer


def run_script(file_path: str) -> tuple[str, int]:
    result = subprocess.run(["python", file_path], capture_output=True)
    return file_path, result.returncode


def main(folder_path: str, threads: int = typer.Option(None, "-p", "--parallel")):
    folder = Path(folder_path)
    python_files = sorted([file for file in folder.glob("p*.py") if file.name != 'p00.py'])

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for file, return_code in executor.map(run_script, python_files):
            icon = ["❌", "✅"][return_code == 0]
            print(f"{file} {icon}")


if __name__ == "__main__":
    typer.run(main)
