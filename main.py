import pandas as pd

def main():
    print("Python environment is working!")

    # Try reading an Excel file (create a dummy one later if needed)
    try:
        df = pd.read_excel("raw_GL.xlsx")
        print("Excel loaded successfully!")
        print(df.head())
    except FileNotFoundError:
        print("raw_GL.xlsx not found. Place your GL file in the same folder as main.py")

if __name__ == "__main__":
    main()
