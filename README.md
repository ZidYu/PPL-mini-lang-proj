# Mini Language Interpreter

Mini is a small interpreter project with variables, numbers, strings, booleans,
conditionals, loops, functions, returns, and `print`.

## Requirements

- Windows 10 or newer
- Python 3.10 or newer

Check Python from `cmd.exe` or PowerShell:

```powershell
python --version
```

## Setup

Download or clone this project, then open a terminal in the project folder.

You can run Mini directly from the project folder with `mini.cmd` or
`.\mini.ps1`. To make the command available anywhere for the current terminal
session, add this folder to `PATH`.

From `cmd.exe`:

```cmd
set "PATH=%CD%;%PATH%"
```

From PowerShell:

```powershell
$env:Path = "$PWD;$env:Path"
```

After that, run Mini as:

```cmd
mini examples\hello.mini
```

## Run From Cmd

Open `cmd.exe` in this project folder.

Start the interactive interpreter:

```cmd
mini.cmd
```

Run a file:

```cmd
mini.cmd examples\hello.mini
```

Run code directly:

```cmd
mini.cmd -c "print(1 + 2)"
```

Open Mini in its own new Command Prompt window:

```cmd
mini-shell.cmd
```

## Run From PowerShell

Open PowerShell in this project folder.

Start the interactive interpreter:

```powershell
.\mini.ps1
```

Run a file:

```powershell
.\mini.ps1 .\examples\hello.mini
```

Run code directly:

```powershell
.\mini.ps1 -c "print(1 + 2)"
```

Open Mini in its own new Command Prompt window:

```powershell
.\mini-shell.ps1
```

If PowerShell blocks local scripts, run this once for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Compile For Windows

The interpreter can be packaged into a Windows executable with PyInstaller. The
build script installs PyInstaller if it is missing, so the first build needs an
internet connection.

From PowerShell:

```powershell
.\build_windows.ps1
```

From `cmd.exe`:

```cmd
build_windows.cmd
```

The default build creates:

```text
dist\mini\mini.exe
```

For a single executable file:

```powershell
.\build_windows.ps1 -OneFile
```

That creates:

```text
dist\mini.exe
```

After compiling, the launchers automatically use the compiled executable when it
exists:

```cmd
mini.cmd examples\hello.mini
```

## Language Example

```text
let x = 5
let name = "Jasmin"

print("Hello " + name)

while x < 8:
    print(x)
    x = x + 1
end

function add(a, b):
    return a + b
end

print(add(5, 3))
```

## Notes

- Use `let name = value` to create a variable.
- Use `name = value` to update an existing variable.
- Blocks use `:` and close with `end`.
- Comments start with `#`.

