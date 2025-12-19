import FreeSimpleGUI as sg
from main import main

layout = [
    [sg.Text("Select GL and/or TB Excel Files:", size=(30,1))],
    [sg.FilesBrowse(
        "Upload Files", 
        key="file_paths", 
        file_types=(("Excel Files", "*.xlsx"),),  
        size=(50,1)
    )],
    [sg.Text("", key="status", size=(50,1), text_color="green")],  # optional status line
    [sg.Frame("Process Options", [
        [sg.Button("Process TB & GL", size=(15,1), key="process_both")],
        [sg.Button("Process TB", size=(15,1), key="process_tb"), sg.Button("Process GL", size=(15,1), key="process_gl")]
    ])],
    [sg.Button("Exit", size=(10,1), key="exit_btn")]
]

window = sg.Window("Excel Processor", layout,  background_color="")

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "exit_btn"):
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
