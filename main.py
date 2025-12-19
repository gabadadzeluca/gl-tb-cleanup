import pandas as pd
from gl_processing import process_gl
from tb_processing import process_tb
from common.cleanup import load_excel

OUTPUT_FILENAME = "Processed_output.xlsx"


def main(file_paths):

    try:

        gl_file, tb_file = file_paths
        """GL processing"""
        gl_df = load_excel(gl_file)
        print("Excel loaded successfully!")

        gl_df = process_gl(gl_df)
        
        """TB processing"""
        tb_df = load_excel(tb_file)
        tb_df = process_tb(tb_df)

        # ---- SAVE BOTH TO SAME WORKBOOK ----
        with pd.ExcelWriter(OUTPUT_FILENAME, engine="openpyxl", mode="w") as writer:
            gl_df.to_excel(writer, sheet_name="GL_cleaned", index=False)
            tb_df.to_excel(writer, sheet_name="TB_cleaned", index=False)
        return OUTPUT_FILENAME

    except FileNotFoundError as e:
        print(e)
        return None

if __name__ == "__main__":
    main()
