import pandas as pd
import glob
import os

# Thư mục chứa file Excel
path = r"d:\Mon_hoc\NCKH\AccModel\SVM\Summary"

# Lấy tất cả file Excel/CSV trong thư mục
all_files = glob.glob(os.path.join(path, "*seeds0_nRep1.xlsx")) + glob.glob(os.path.join(path, "*.xls")) + glob.glob(os.path.join(path, "*.csv"))


# đọc từng Files 
dfs = []
for file in all_files:
    try:
        if file.endswith(".xlsx"):
            df = pd.read_excel(file, engine="openpyxl")
        elif file.endswith(".xls"):
            df = pd.read_excel(file, engine="xlrd")
        else:
            df = pd.read_csv(file)

        df["source_file"] = os.path.basename(file)  # lưu tên file gốc
        dfs.append(df)

    except Exception as e:
        print(f"❌ Lỗi khi đọc {file}: {e}")
print(dfs)