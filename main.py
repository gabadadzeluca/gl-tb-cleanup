from gl_processing import load_excel, process_gl

RAW_GL_FILENAME = "GL.xlsx"


def main():

    try:
        df = load_excel(RAW_GL_FILENAME)
        print("Excel loaded successfully!")

        df = process_gl(df)

        print(df.head())

    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
