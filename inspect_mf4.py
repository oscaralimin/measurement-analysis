from asammdf import MDF
from tkinter import filedialog
from pathlib import Path

def inspect_mf4():
    # Open file dialog to select MF4 file
    file_path = filedialog.askopenfilename(
        title="Select MF4 file to inspect",
        filetypes=[("MF4 files", "*.mf4")]
    )
    
    if not file_path:
        print("No file selected")
        return
        
    # Load and inspect file
    mdf = MDF(file_path)
    print(f"\nFile: {Path(file_path).name}")
    print(mdf.info())
    print("\nChannel Information:")
    print("-" * 50)
    
    for channel in mdf.iter_channels():
        print(f"Channel name: {channel.name}")
        print(f"Unit: {channel.unit}")
        print("-" * 50)

if __name__ == "__main__":
    inspect_mf4()