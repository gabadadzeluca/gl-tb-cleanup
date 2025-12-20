import FreeSimpleGUI as sg
from main import main

layout = [
    [sg.Text("Select GL or TB Excel File:", size=(30,1))],
    [sg.FilesBrowse(
        "Upload File", 
        key="file_path", 
        file_types=(("Excel Files", "*.xlsx"),),  
        size=(50,1)
    )],
    [sg.Text("File (Company) name: [Optional]", size=(30,1))],
    [sg.Input(
        key="output_name",
        size=(40, 1),
        tooltip="Leave blank to use default filename"
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
        file_path = values["file_path"].split(";")[0] if values["file_path"] else None

        if len(file_path) == 0:
            sg.popup("Please select at least one Excel file.")
            continue

        isGL = event == "process_gl"
        
        # Get optional file name
        output_name = values["output_name"].strip()
        output_name = output_name if output_name else None

        try:
            output_file = main(file_path, isGL, output_name)
            sg.popup("Processing Complete!",
                    f"The clean Excel file is ready:\n{output_file}")
        except Exception as e:
            sg.popup("Error", f"Processing failed:\n{e}\nPlease check the uploaded file and try again.")

window.close()
