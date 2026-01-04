import FreeSimpleGUI as sg
from main import main
from models.gui_keys import GUI_KEYS
from models.files import Files
from theme import *

# Kinda like global styles
sg.theme_background_color(BG_MAIN)
sg.theme_element_background_color(BG_COLUMN)
sg.theme_text_color(TEXT_PRIMARY)
sg.theme_button_color(BTN_EXIT)

def show_styled_popup(title, message, is_error=True):
    """
    Displays a themed popup. 
    is_error=True (1): Uses Red theme
    is_error=False (0): Uses Green theme
    """
    # Determine style based on the is_error boolean
    btn_color = BTN_REMOVE if is_error else BTN_PROCESS_SINGLE
    
    sg.popup(
        message,
        title=title,
        background_color=BG_MAIN,
        text_color=TEXT_PRIMARY,
        button_color=btn_color,
        font=FONT_TEXT,
        no_titlebar=False,
        keep_on_top=True,
        line_width=60,
        any_key_closes=True,
        icon=None
    )


file_upload_section = sg.Column([
    [sg.Text("Select GL or TB Excel File:", font=(FONT_TEXT[0], 12, 'bold'), text_color=TEXT_PRIMARY, background_color=BG_COLUMN)],
    [sg.FilesBrowse(
        "Upload File", 
        key=GUI_KEYS.FILE_PATH,
        file_types=(("Excel Files", "*.xlsx"),),  
        size=(45,1),
        font=FONT_BUTTON,
        button_color=BTN_UPLOAD,
        enable_events=True,
        pad=(0, (10, 20))
    )],

    [sg.Text("Uploaded Files:", font=FONT_TEXT, text_color=TEXT_PRIMARY, background_color=BG_COLUMN)],
    [sg.Listbox(
        values=[], size=(45,2), key=GUI_KEYS.UPLOADED_FILES, enable_events=True,
        no_scrollbar=True,
        font=FONT_INPUT,
        background_color=BG_LISTBOX,
        text_color=TEXT_PRIMARY,
        pad=(0, (5, 10)),
    )],
    [sg.Push(background_color=BG_COLUMN), sg.Button("Remove Selected", key=GUI_KEYS.REMOVE_FILE, font=("Segoe UI", 9), button_color=BTN_REMOVE, size=(15, 1))],
    
    # Visual break
    [sg.HSeparator(pad=(0, 20))],

    [sg.Text("Company name: [Optional]", font=FONT_TEXT, text_color=TEXT_PRIMARY, background_color=BG_COLUMN)],
    [sg.Input(
        key=GUI_KEYS.OUTPUT_NAME,
        size=(46, 1),
        font=FONT_INPUT,
        pad=(0, (5, 15)),
        background_color=BG_LISTBOX,
        text_color=TEXT_PRIMARY
    )]
], pad=PAD_SECTION, background_color=BG_COLUMN)

process_section = sg.Frame(
    " Process Options ", [
        [
            sg.Button("Process TB", size=(12,2), key=GUI_KEYS.PROCESS_TB, font=FONT_BUTTON, button_color=BTN_PROCESS_SINGLE),
            sg.Button("Process GL", size=(12,2), key=GUI_KEYS.PROCESS_GL, font=FONT_BUTTON, button_color=BTN_PROCESS_SINGLE),
            sg.Button("Process Both & Reconcile", size=(12,2), key=GUI_KEYS.PROCESS_BOTH, font=FONT_BUTTON, button_color=BTN_PROCESS_BOTH)
        ]
    ],
    pad=(0, 20), 
    title_color=TEXT_SECONDARY,
    background_color=BG_COLUMN
)

layout = [
    [file_upload_section],
    [process_section],
    [# Note for the 3rd option 
        sg.Text(
            "Note: Include 'TB' & 'GL' in filenames for the 'Process Both' option", 
            font=(FONT_TEXT, 7, 'italic'), 
            background_color=BG_COLUMN,
            text_color=TEXT_SECONDARY, 
        )
    ],
    [sg.Button("Exit", size=(10,1), key=GUI_KEYS.EXIT, font=FONT_BUTTON, border_width=0, button_color=BTN_EXIT, pad=(0, 10))]
]

window = sg.Window(
    "LedgerPrep",
    layout,
    element_justification="center",
    margins=(20,20),
    resizable=True,
    background_color=BG_MAIN,
    font=FONT_TEXT
)
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
                    show_styled_popup("File Capacity Reached", "Only 2 files can be uploaded at a time.")
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
                show_styled_popup("Missing Files", "Please upload both TB and GL files to process both.")
                continue
        else:
            """ Single processing """
            isBoth = False
            isGL = (event == GUI_KEYS.PROCESS_GL)

        try:
            output_file = main(files, isGL, isBoth, output_name)
            show_styled_popup("Processing Complete!", f"The clean Excel file is ready:\n{output_file}", is_error=False)
        except Exception as e:
            show_styled_popup("Error", f"Processing failed:\n{e}\nPlease check the uploaded file and try again.")

window.close()