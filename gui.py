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
    [sg.Frame("Process Options", [
        [sg.Button("Process TB", size=(15,1), key="process_tb"), sg.Button("Process GL", size=(15,1), key="process_gl")]
    ])],
    [sg.Button("Exit", size=(10,1), key="exit_btn")]
]

window = sg.Window("Excel Processor", layout,  background_color="")

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "exit_btn"):
        break

    if event == "process_tb" or event == "process_gl":
        # Split and remove empty paths
        file_path = [p for p in values["file_paths"].split(";") if p.strip()]

        if len(file_path) == 0:
            sg.popup("Please select at least one Excel file.")
            continue

        try:
            output_file = main(file_path)
            sg.popup("Processing Complete!",
                    f"The clean Excel file is ready:\n{output_file}")
        except Exception as e:
            sg.popup("Error", f"Processing failed:\n{e}")


window.close()
