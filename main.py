import pandas as pd
from gl_processing import process_gl
from tb_processing import process_tb
from common.cleanup import load_excel


def main(file_path, isGL, filename=""):   
    #Optional file (comapny name)     
    gl_file, tb_file = None, None
    OUTPUT_FILENAME = f"TB-{filename}.xlsx"

    try:
        if(isGL):
            """GL processing"""
            gl_file = file_path
            gl_df = load_excel(gl_file)
            gl_df = process_gl(gl_df)
            OUTPUT_FILENAME = f"GL-{filename}.xlsx"
        else:
            """TB processing"""
            tb_file = file_path
            tb_df = load_excel(tb_file)
            tb_df = process_tb(tb_df)

        # ---- SAVE TO WORKBOOK ----
        with pd.ExcelWriter(OUTPUT_FILENAME, engine="openpyxl", mode="w") as writer:
            if isGL:
                gl_df.to_excel(writer, sheet_name="GL_cleaned", index=False)
            else:
                tb_df.to_excel(writer, sheet_name="TB_cleaned", index=False)

        return OUTPUT_FILENAME

    except FileNotFoundError as e:
        print(e)
        return None

if __name__ == "__main__":
    main()
