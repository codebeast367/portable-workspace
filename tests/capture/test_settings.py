from pathlib import Path
import json
import shutil

from workspace.capture.settings import capture_settings


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SAMPLE_DIR = PROJECT_ROOT / "tests" / "capture" / "sample_settings"
OUTPUT_DIR = PROJECT_ROOT / "tests" / "capture" / "captured_settings"


def create_sample_settings():
    if SAMPLE_DIR.exists():
        shutil.rmtree(SAMPLE_DIR)

    SAMPLE_DIR.mkdir(parents=True)

    vscode = SAMPLE_DIR / "vscode"
    git = SAMPLE_DIR / "git"
    terminal = SAMPLE_DIR / "terminal"

    vscode.mkdir()
    git.mkdir()
    terminal.mkdir()

    (vscode / "settings.json").write_text(
        json.dumps(
            {
                "editor.fontSize": 14,
                "editor.tabSize": 4
            },
            indent=4
        ),
        encoding="utf-8"
    )

    (vscode / "keybindings.json").write_text(
        json.dumps(
            [
                {
                    "key": "ctrl+k",
                    "command": "workbench.action.files.openFile"
                }
            ],
            indent=4
        ),
        encoding="utf-8"
    )

    (git / "gitconfig").write_text(
        "[user]\nname=Test User\nemail=test@example.com\n",
        encoding="utf-8"
    )

    (terminal / "terminal.json").write_text(
        '{"fontSize": 12}\n',
        encoding="utf-8"
    )


def main():
    create_sample_settings()

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    sources = {
        "vscode": SAMPLE_DIR / "vscode",
        "git": SAMPLE_DIR / "git",
        "terminal": SAMPLE_DIR / "terminal",
    }

    captured = capture_settings(sources, OUTPUT_DIR)

    print("Captured:", captured)
    print()
    print("Captured settings:")

    for path in OUTPUT_DIR.rglob("*"):
        if path.is_file():
            print(path.relative_to(OUTPUT_DIR))


if __name__ == "__main__":
    main()