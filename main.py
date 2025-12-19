import pandas as pd
from gl_processing import process_gl
from tb_processing import process_tb
from ppe_processing import process_ppe
from common.cleanup import load_excel
from add_groupings import add_groupings

RAW_GL_FILENAME = "GL.xlsx"
RAW_TB_FILENAME = "TB.xlsx"
OUTPUT_FILENAME = "Processed_output.xlsx"


def main():

    try:
        """GL processing"""
        gl_df = load_excel(RAW_GL_FILENAME)
        print("Excel loaded successfully!")

        gl_df = process_gl(gl_df)
        gl_df = add_groupings(gl_df)
        
        """TB processing"""
        tb_df = load_excel(RAW_TB_FILENAME)
        tb_df = process_tb(tb_df)

        """PPE processing"""
        ppe_df = process_ppe(tb_df)

        # ---- SAVE BOTH TO SAME WORKBOOK ----
        with pd.ExcelWriter(OUTPUT_FILENAME, engine="openpyxl", mode="w") as writer:
            gl_df.to_excel(writer, sheet_name="GL_cleaned", index=False)
            tb_df.to_excel(writer, sheet_name="TB_cleaned", index=False)
            ppe_df.to_excel(writer, sheet_name="PPE", index=False)


    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
