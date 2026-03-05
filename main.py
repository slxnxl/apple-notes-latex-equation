import os

# Fix PyInstaller resetting MPLCONFIGDIR to a temp dir on every launch,
# which forces matplotlib to rebuild the font cache every time.
_mpl_cache = os.path.join(os.path.expanduser("~"), ".latex2clipboard", "mpl")
os.makedirs(_mpl_cache, exist_ok=True)
os.environ["MPLCONFIGDIR"] = _mpl_cache

from matplotlib.mathtext import math_to_image
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from io import BytesIO
from Foundation import NSData
from AppKit import NSPasteboard, NSPasteboardTypeString, NSPasteboardTypePNG, NSPasteboardTypeTIFF
from argparse import ArgumentParser # https://docs.python.org/3/howto/argparse.html#argparse-tutorial

def get_text_from_clipboard() -> str:
    """
    https://stackoverflow.com/a/8317794 (Updated for python3)
    """
    pasteboard = NSPasteboard.generalPasteboard()
    text = pasteboard.stringForType_(NSPasteboardTypeString)
    return text.strip()

def get_formula_from_text(text: str) -> str:
    if text.startswith("$") and text.endswith("$"):
        return text
    return f"${text}$"

def get_formula_from_input() -> str:
    text = input()
    return get_formula_from_text(text)

def get_formula_from_clipboard() -> str:
    text = get_text_from_clipboard()
    return get_formula_from_text(text)

def save_formula_as_image(formula: str, file_path: str) -> str:
    buf = BytesIO()
    math_to_image(formula, buf, dpi=300, format='png')
    buf.seek(0)

    # Embed LaTeX source into PNG metadata
    img = Image.open(buf)
    metadata = PngInfo()
    metadata.add_text("latex", formula)
    img.save(file_path, pnginfo=metadata)

    return file_path

def copy_image_to_clipboard(file_path: str) -> bool:
  """
  https://stackoverflow.com/a/76159627
  """
  filename = "formula.png"  # set this to filepath where img is saved
  pasteboard = NSPasteboard.generalPasteboard()
  image_data = NSData.dataWithContentsOfFile_(filename)
  pasteboard.clearContents()
  return pasteboard.setData_forType_(image_data, NSPasteboardTypePNG)

def init_argparse() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "-t",
        "--text",
        type=str,
        help="latex formula given as argument"
    )
    parser.add_argument(
        "-c",
        "--clipboard",
        action="store_true",
        help="latex formula given inside clipboard"
    )
    parser.add_argument(
        "-e",
        "--extract",
        type=str,
        help="extract latex formula from a PNG file"
    )
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    if args.extract:
        img = Image.open(args.extract)
        latex = img.text.get("latex")
        if latex:
            print(latex)
        else:
            print("No LaTeX metadata found in this image.")
        return

    if args.text:
        formula = get_formula_from_text(args.text)
    elif args.clipboard:
        formula = get_formula_from_clipboard()
    else:
        formula = get_formula_from_input()
    save_formula_as_image(formula, "formula.png")
    copy_image_to_clipboard("formula.png")

if __name__ == "__main__":
   main()
