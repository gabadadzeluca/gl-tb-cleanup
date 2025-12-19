import FreeSimpleGUI as sg
from main import main

layout = [
    [sg.Text("Select GL and TB Excel Files:", size=(30,1))],
    [sg.Input(key="file_paths", enable_events=True, size=(50,1)), sg.FilesBrowse("Browse")],
    [sg.Button("Process", size=(10,1)), sg.Button("Exit", size=(10,1))]
]

window = sg.Window("Excel Processor", layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break

    if event == "Process":
        file_paths = values["file_paths"].split(";")  # split string into list
        if len(file_paths) != 2:
            sg.popup("Please select exactly 2 files: GL and TB Excel files.")
            continue

        output_file = main(file_paths)
        if output_file:
            sg.popup("Processing Complete!", f"The combined Excel file is ready: {output_file}")
        else:
            sg.popup("Error", "Processing failed. Check your files.")

window.close()
