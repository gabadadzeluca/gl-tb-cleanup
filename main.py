import pandas as pd
from gl_processing import process_gl
from tb_processing import process_tb
from common.cleanup import load_excel


def main(files, isGL, isBoth, filename=""):   
    tb_file , gl_file = files.tb_path, files.gl_path
    TB_OUTPUT_FILENAME = f"TB-{filename}.xlsx" if filename else "TB-cleaned.xlsx"
    GL_OUTPUT_FILENAME = f"GL-{filename}.xlsx" if filename else "GL-cleaned.xlsx"
    
    try:
        if(isGL):
            """GL processing"""
            gl_df = load_excel(gl_file)
            gl_df = process_gl(gl_df)
            OUTPUT_FILENAME = GL_OUTPUT_FILENAME
        elif(not isBoth):
            """TB processing"""
            tb_df = load_excel(tb_file)
            tb_df = process_tb(tb_df)
            OUTPUT_FILENAME = TB_OUTPUT_FILENAME
        else:
            """Both processing"""
            tb_df = load_excel(tb_file)
            gl_df = load_excel(gl_file)

            tb_df = process_tb(tb_df)
            gl_df = process_gl(gl_df)
            OUTPUT_FILENAME = f"TB-GL-{filename}.xlsx" if filename else "TB-GL-cleaned.xlsx"

        # ---- SAVE TO WORKBOOK ----
        with pd.ExcelWriter(OUTPUT_FILENAME, engine="openpyxl", mode="w") as writer:
            if isGL:
                gl_df.to_excel(writer, sheet_name="GL_cleaned", index=False)
            elif not isBoth:
                tb_df.to_excel(writer, sheet_name="TB_cleaned", index=False)
            else:
                tb_df.to_excel(writer, sheet_name="TB_cleaned", index=False)
                gl_df.to_excel(writer, sheet_name="GL_cleaned", index=False)

        return OUTPUT_FILENAME

    except FileNotFoundError as e:
        print(e)
        return None

if __name__ == "__main__":
    main()
