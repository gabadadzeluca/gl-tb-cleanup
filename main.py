import pandas as pd
from gl_processing import process_gl
from tb_processing import process_tb
from common.cleanup import load_excel


def main(files, isGL, isBoth, filename=""):   
    tb_file, gl_file = files.tb_path, files.gl_path

    TB_OUTPUT_FILENAME = f"TB-{filename}.xlsx" if filename else "TB-cleaned.xlsx"
    GL_OUTPUT_FILENAME = f"GL-{filename}.xlsx" if filename else "GL-cleaned.xlsx"
    BOTH_OUTPUT_FILENAME = f"TB-GL-{filename}.xlsx" if filename else "TB&GL-cleaned.xlsx"

    try:
        # ---- LOAD & PROCESS ----
        tb_df = load_excel(tb_file) if tb_file else None
        gl_df = load_excel(gl_file) if gl_file else None

        if tb_df is not None and (not isGL or isBoth):
            tb_df = process_tb(tb_df)
        if gl_df is not None and (isGL or isBoth):
            gl_df = process_gl(gl_df)

        # ---- DECIDE OUTPUT FILENAME ----
        if isBoth:
            OUTPUT_FILENAME = BOTH_OUTPUT_FILENAME
        elif isGL:
            OUTPUT_FILENAME = GL_OUTPUT_FILENAME
        else:
            OUTPUT_FILENAME = TB_OUTPUT_FILENAME

        # ---- SAVE TO EXCEL ----
        with pd.ExcelWriter(OUTPUT_FILENAME, engine="openpyxl", mode="w") as writer:
            if tb_df is not None:
                tb_df.to_excel(writer, sheet_name="TB_cleaned", index=False)
            if gl_df is not None:
                gl_df.to_excel(writer, sheet_name="GL_cleaned", index=False)

        return OUTPUT_FILENAME

    except FileNotFoundError as e:
        print(e)
        return None

if __name__ == "__main__":
    main()
