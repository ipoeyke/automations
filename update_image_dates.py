#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from datetime import datetime, timedelta
import subprocess
from typing import List, Optional, Union

# Supported image extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.heic', '.nef', '.cr2', '.arw'}

def update_image_dates(
    folder_path: str,
    start_date: Optional[Union[str, datetime]] = None,
    increment_minutes: int = 60,
    extensions: Optional[set[str]] = None
) -> None:
    """
    Update the modified date of image files in a folder based on their filename ordering.
    
    Args:
        folder_path: Path to the folder containing image files
        start_date: Starting date (defaults to current date if None)
        increment_minutes: Minutes to increment between files
        extensions: Set of file extensions to process (defaults to IMAGE_EXTENSIONS)
    """
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory")
        return
    
    if increment_minutes <= 0:
        print("Error: increment_minutes must be positive")
        return

    # Use provided extensions or default
    valid_extensions = extensions if extensions is not None else IMAGE_EXTENSIONS
    
    # Get all image files and sort them by name
    image_files: List[str] = []
    
    # Use scandir for better performance
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file() and os.path.splitext(entry.name)[1].lower() in valid_extensions:
                image_files.append(entry.path)
    
    image_files.sort()  # Sort by filename
    
    if not image_files:
        print("No image files found in the directory")
        return
    
    # Set the starting date if not provided
    if start_date is None:
        start_date = datetime.now()
    elif isinstance(start_date, str):
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD HH:MM:SS")
            return
    
    print(f"Found {len(image_files)} image files")
    print(f"Starting date: {start_date}")
    print(f"Increment: {increment_minutes} minutes")
    
    # Process each file
    current_date = start_date
    total_files = len(image_files)
    
    for i, file_path in enumerate(image_files, 1):
        # Format the date for the touch command
        date_str = current_date.strftime("%Y%m%d%H%M.%S")
        
        # Use touch command to update both access and modification times
        try:
            # Update modification and access time
            subprocess.run(['touch', '-mt', date_str, file_path], check=True)

            # Update creation time (macOS specific)
            subprocess.run(['SetFile', '-d', current_date.strftime("%m/%d/%Y %H:%M:%S"), file_path], check=True)
            
            # Print progress with percentage
            progress = (i / total_files) * 100
            print(f"[{progress:3.1f}%] Updated {os.path.basename(file_path)} to {current_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Increment the date for the next file
            current_date += timedelta(minutes=increment_minutes)
        except subprocess.CalledProcessError as e:
            print(f"Error updating {file_path}: {e}")
            if "SetFile" in str(e):
                print("Note: SetFile command not found. Make sure Xcode Command Line Tools are installed.")
                print("Install with: xcode-select --install")
                break
            return

def main() -> None:
    # Create a root window but hide it
    root = tk.Tk()
    root.withdraw()

    # Show folder selection dialog
    folder_path = filedialog.askdirectory(
        title="Select Folder with Images to Update Dates",
        initialdir=os.path.expanduser('~')  # Set default to user's home directory
    )

    # If no folder selected, exit
    if not folder_path:
        messagebox.showinfo("Info", "No folder selected. Exiting.")
        return

    # Optionally ask for start date
    start_date_str = simpledialog.askstring(
        "Start Date", 
        "Enter start date (YYYY-MM-DD HH:MM:SS) or leave blank for current date:",
        initialvalue=datetime.now().replace(hour=0, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
    )

    # Optionally ask for increment minutes
    increment_minutes = simpledialog.askinteger(
        "Increment Minutes", 
        "Enter minutes between file dates:", 
        initialvalue=1,
        minvalue=1
    )

    # If user cancels any dialog, exit
    if start_date_str is None or increment_minutes is None:
        return

    # Call update function with selected parameters
    update_image_dates(
        folder_path=folder_path, 
        start_date=start_date_str if start_date_str else None,
        increment_minutes=increment_minutes or 60
    )

if __name__ == "__main__":
    main()