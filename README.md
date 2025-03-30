# automations
Random automations (mostly single-file Python scripts) for MacOS for my own use cases.

Disclaimer: these scripts are strictly meant to fulfil my personal requirements only, and may not be tested for more general scenarios and/or edge cases. Another priority of mine is speed of development - a significant portion of code may also be AI-generated as a result of "vibe coding" (term coined by Karpathy. But of course, each line is reviewed to ensure the script works and nothing weird happens).

## List of automations
1. update_image_dates.py

Problem statement: for film photography, analog film scans done by the lab may have the same metadata contained for all images (created/modified time). Even though the scans are (usually) done chronologically which is reflected in the filenames, the user may not be able to reliably sort the images chronologically on photo viewing software (e.g. Apple Photos).

Description: this script changes the created, modified, and access times of every image file in a directory specified by the user via a simple Tkinter UI. The user may also set the date and the number of minutes to increment each image's metadata by.
