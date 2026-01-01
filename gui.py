import FreeSimpleGUI as sg
from main import main
from gui_keys import GUI_KEYS

layout = [
    [sg.Text("Select GL or TB Excel File:", size=(30,1))],
    [sg.FilesBrowse(
        "Upload File", 
        key=GUI_KEYS.FILE_PATH,
        file_types=(("Excel Files", "*.xlsx"),),  
        size=(50,1)
    )],
    [sg.Text("File (Company) name: [Optional]", size=(30,1))],
    [sg.Input(
        key=GUI_KEYS.OUTPUT_NAME,
        size=(40, 1),
        tooltip="Leave blank to use default filename"
    )],
    [sg.Frame("Process Options", [
        [sg.Button("Process TB", size=(15,1), key=GUI_KEYS.PROCESS_TB), sg.Button("Process GL", size=(15,1), key=GUI_KEYS.PROCESS_GL)]
    ])],
    [sg.Button("Exit", size=(10,1), key=GUI_KEYS.EXIT)]
]

window = sg.Window("Excel Processor", layout,  background_color="")

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, GUI_KEYS.EXIT):
        break

    if event == GUI_KEYS.PROCESS_TB or event == GUI_KEYS.PROCESS_GL:
        # Split and remove empty paths
        file_path = values[GUI_KEYS.FILE_PATH].split(";")[0] if values[GUI_KEYS.FILE_PATH] else None

        if len(file_path) == 0:
            sg.popup("Please select at least one Excel file.")
            continue

        isGL = event == GUI_KEYS.PROCESS_GL
        isTB = event == GUI_KEYS.PROCESS_TB
        """ADD A BOTH BUTTON"""
        # isBoth = event == GUI_KEYS.PROCESS_RECON

        # Get optional file name
        output_name = values[GUI_KEYS.OUTPUT_NAME].strip()
        output_name = output_name if output_name else None

        try:
            output_file = main(file_path, isGL, isTB, output_name)
            sg.popup("Processing Complete!",
                    f"The clean Excel file is ready:\n{output_file}")
        except Exception as e:
            sg.popup("Error", f"Processing failed:\n{e}\nPlease check the uploaded file and try again.")

window.close()
