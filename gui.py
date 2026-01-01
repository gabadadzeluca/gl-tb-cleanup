import FreeSimpleGUI as sg
from main import main
from models.gui_keys import GUI_KEYS
from models.files import Files

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
        [
            sg.Button("Process TB", size=(15,1), key=GUI_KEYS.PROCESS_TB), 
            sg.Button("Process GL", size=(15,1), key=GUI_KEYS.PROCESS_GL),
            sg.Button("Process Both", size=(15,1), key=GUI_KEYS.PROCESS_BOTH)
        ]
    ])],
    [sg.Button("Exit", size=(10,1), key=GUI_KEYS.EXIT)]
]

window = sg.Window("LedgerPrep", layout,  background_color="")

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, GUI_KEYS.EXIT):
        break

    if event in [GUI_KEYS.PROCESS_BOTH, GUI_KEYS.PROCESS_GL, GUI_KEYS.PROCESS_TB]:
        # Initialize File paths
        files = Files()
        files.tb_path = None
        files.gl_path = None
        
        # Split and remove empty paths
        if values[GUI_KEYS.FILE_PATH]:
            filepaths = values[GUI_KEYS.FILE_PATH].split(";")
            
            if(len(filepaths) == 0):
                sg.popup("Error", "No file selected. Please upload an Excel file.")
                continue
            elif(len(filepaths) > 1):
                # temporary assignments tb 1, gl 2
                files.tb_path = filepaths[0]
                files.gl_path = filepaths[1]
            elif(len(filepaths) == 1):
                """ Single file uploaded TEMPORARILY ASSIGN TO TB ONLY """
                files.tb_path = filepaths[0]

        # Get optional file name
        output_name = values[GUI_KEYS.OUTPUT_NAME].strip()
        output_name = output_name if output_name else None

        if(event == GUI_KEYS.PROCESS_BOTH):
            """ Both processing """
            isBoth = True
            isGL = False
            # error check so that both files are uploaded
            if(not files.tb_path or not files.gl_path):
                sg.popup("Error", "Please upload both TB and GL files to process both.")
                continue
        else:
            """ Single processing """
            isBoth = False
            if(event == GUI_KEYS.PROCESS_GL):
                isGL = True

        try:
            output_file = main(files, isGL, isBoth, output_name)
            sg.popup("Processing Complete!",
                    f"The clean Excel file is ready:\n{output_file}")
        except Exception as e:
            sg.popup("Error", f"Processing failed:\n{e}\nPlease check the uploaded file and try again.")

window.close()
