import FreeSimpleGUI as sg
from main import main
from models.gui_keys import GUI_KEYS
from models.files import Files


file_upload_section = sg.Column([
    [sg.Text("Select GL or TB Excel File:", size=(30,1))],
    [sg.FilesBrowse(
        "Upload File", 
        key=GUI_KEYS.FILE_PATH,
        file_types=(("Excel Files", "*.xlsx"),),  
        size=(50,1),
        enable_events=True
    )],

    [sg.Text("Uploaded Files:")],
    [sg.Listbox(values=[], size=(50,4), key=GUI_KEYS.UPLOADED_FILES, enable_events=True, no_scrollbar=True)],
    [sg.Button("Remove Selected File", key=GUI_KEYS.REMOVE_FILE)],

    [sg.Text("Company name: [Optional]", size=(30,1))],
    [sg.Input(
        key=GUI_KEYS.OUTPUT_NAME,
        size=(40, 1),
        tooltip="Leave blank to use default filename"
    )]
])
process_section = sg.Frame("Process Options", [
    [
        sg.Button("Process TB", size=(15,1), key=GUI_KEYS.PROCESS_TB), 
        sg.Button("Process GL", size=(15,1), key=GUI_KEYS.PROCESS_GL),
        sg.Button("Process Both", size=(15,1), key=GUI_KEYS.PROCESS_BOTH)
    ]
])

layout = [
    [file_upload_section],
    [process_section],
    [sg.Button("Exit", size=(10,1), key=GUI_KEYS.EXIT)]
]

window = sg.Window("LedgerPrep", layout, element_justification="center")

# to store uploaded files
uploaded_files = []

# Initialize File paths
files = Files()
files.tb_path = None
files.gl_path = None


while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, GUI_KEYS.EXIT):
        break
    
    """Handle File Removal"""
    if event == GUI_KEYS.REMOVE_FILE:
        selected_names = values[GUI_KEYS.UPLOADED_FILES]
        if selected_names:
            uploaded_files = [f for f in uploaded_files if f.split("/")[-1] not in selected_names]
            # reassign tb/gl paths if needed
            files.tb_path = next((f for f in uploaded_files if "tb" in f.lower()), None)
            files.gl_path = next((f for f in uploaded_files if "gl" in f.lower()), None)
            # update display again
            window[GUI_KEYS.UPLOADED_FILES].update([f.split("/")[-1] for f in uploaded_files])


    """Handle File Uploads"""
    if event == GUI_KEYS.FILE_PATH:
        # Split and remove empty paths
        new_files = [f.strip() for f in values[GUI_KEYS.FILE_PATH].split(";") if f.strip()]
        
        # merge the lists and remove duplicates
        for f in new_files:
            if f not in uploaded_files:
                if len(uploaded_files) < 2:
                    uploaded_files.append(f)
                else:
                    sg.popup("Only 2 files can be uploaded at a time.")
                    break

        # Assign files based on names
        for file in uploaded_files:
            print("Processing a file:", file)
            lower_file = file.lower().split("/")[-1]  # get the file name only in lowercase
            if "tb" in lower_file:
                files.tb_path = file
            if "gl" in lower_file:
                files.gl_path = file

        # Update the input field and Multiline display
        display_names = [f.split("/")[-1] for f in uploaded_files] 
        window[GUI_KEYS.UPLOADED_FILES].update(display_names)

    """Handle Processing Events"""
    if event in [GUI_KEYS.PROCESS_BOTH, GUI_KEYS.PROCESS_GL, GUI_KEYS.PROCESS_TB]:
        isBoth = False
        isGL = False

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
            isGL = (event == GUI_KEYS.PROCESS_GL)

        try:
            output_file = main(files, isGL, isBoth, output_name)
            sg.popup("Processing Complete!",
                    f"The clean Excel file is ready:\n{output_file}")
        except Exception as e:
            sg.popup("Error", f"Processing failed:\n{e}\nPlease check the uploaded file and try again.")

window.close()

# TODO Improve column name mappings - NO HARDCODING
# TODO Add progress bar for processing