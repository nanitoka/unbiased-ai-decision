import pandas as pd
import io

# Testing the data.csv content
content = """gender,approved
M,1
M,1
M,1
M,0
F,0
F,1
F,0
F,0
M,1
F,0
M,1
F,1
M,0
F,0"""

try:
    df = pd.read_csv(io.StringIO(content))
    print("Columns:", df.columns.tolist())
    print("Success")
except Exception as e:
    print("Error:", e)
