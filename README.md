# Use LaTeX formula in Apple Notes

## Usage

![Demo](media/demo.gif)

- Write LaTeX equation
- Select LaTeX equation
- Press shortcut
- Paste LaTeX equation as image

## Installation

### Option 1: Pre-built binary (recommended)

Download `latex2clipboard` from the releases page. No Python required.

First run will take ~30 seconds to build the font cache. Subsequent runs are instant (~0.5s).

### Option 2: Build from source

```bash
python3 -m venv .venv --upgrade-deps
. .venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onedir -y main.py --name latex2clipboard
```

The binary will be at `dist/latex2clipboard/latex2clipboard`.

## Setting up Shortcuts

- Create new shortcut in the Shortcuts App
- Add `Run Shell Script` action
- Set **Input** to `Shortcut Input`, **Pass Input** as `as arguments`
- Set the shell script to:
  ```
  /path/to/latex2clipboard -t "$1"
  ```

![Shortcut: Create new shortcut](media/shortcuts-new-shortcut.png)

### Method 1: Recommended

- Go to shortcut
- Click on details (up-right)
- Checkmark `Menu services`
- Open System Settings
- Navigate to Keyboard > Keyboard Shortcuts > App Keyboard Shortcuts
- Click on +
- Choose Apple Notes App
- Enter `Apple Notes LaTeX Equation`
- Choose a prefered keyboard shortcut
![Method 1](media/method-1.png)
![Method 1 System Settings](media/method-1-system-settings.png)

### Method 2: Keyboard-shortcut all apps

- Go to shortcut
- Click on details (up-right)
- Click on add keyboard shortcut

This method is not recommended because the keyboard shortcut will work on all apps.

## CLI Options

```
-t, --text       LaTeX formula as argument
-c, --clipboard  Read LaTeX formula from clipboard
-e, --extract    Extract LaTeX source from a PNG file
```

LaTeX source is embedded in the PNG metadata, so you can recover it later:
```bash
./latex2clipboard --extract formula.png
```

## Changes from the original

This is a fork of [esatbayhan/apple-notes-latex-equation](https://github.com/esatbayhan/apple-notes-latex-equation) with the following changes:

### New features
- **LaTeX metadata in PNG** — the LaTeX source is embedded in the image metadata, so you can extract it later with `--extract`
- **`--extract` flag** — recover LaTeX source from a previously rendered PNG
- **PyInstaller support** — can be built as a standalone binary, no Python installation needed

### Fixes & optimizations
- **Fixed double-dollar wrapping** — formulas already wrapped in `$...$` are no longer double-wrapped
- **~90x faster startup** with PyInstaller — fixed `MPLCONFIGDIR` being reset to a temp directory on every launch, which forced matplotlib to rebuild the font cache every time
- **Lightweight rendering** — replaced `pylab.figure()` with `matplotlib.mathtext.math_to_image()` for faster imports and simpler code
- **Relaxed dependency versions** — `matplotlib>=3.8.0` and `pyobjc>=10.0` for Python 3.13 compatibility

## Resources

- https://support.apple.com/de-de/guide/shortcuts-mac/apd163eb9f95/mac
