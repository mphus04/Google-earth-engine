import pandas as pd
import glob
import os

# Thư mục chứa file Excel
path = r"d:\Mon_hoc\NCKH\AccModel\SVM\Summary"

# Lấy tất cả file Excel/CSV trong thư mục
all_files = glob.glob(os.path.join(path, "SVM_grid_kfold_*.xlsx")) + glob.glob(os.path.join(path, "*.xls")) + glob.glob(os.path.join(path, "*.csv"))
# print(all_files)

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
        
# print(dfs)
# Gộp dữ liệu
if dfs:
    all_data = pd.concat(dfs, ignore_index=True)

    # Giữ lại các cột liên quan tới tham số tối ưu
    keep_cols = ["gamma", "cost", "source_file"]
    # keep_cols = [
    #     "numberOfTrees", "variablesPerSplit", "minLeafPopulation",
    #     "bagFraction", "meanAccuracy", "SE_accuracy", "source_file"]


    # Chỉ giữ lại các cột có trong bảng (tránh lỗi nếu file thiếu cột)
    keep_cols = [col for col in keep_cols
                if col in all_data.columns]
    all_data = all_data[keep_cols]

    # Xuất kết quả ra file Excel
    output_file = os.path.join(path,"all_results_optimal_params.xlsx")
    all_data.to_excel(output_file, index=False, engine="openpyxl")

    print(f"✅ Đã gộp file và giữ lại cột tham số tối ưu, lưu tại: {output_file}")
else:
    print("❌ Không có file nào đọc được.")


# Đọc file gốc và file chứa 16 bộ tham số
file_all = os.path.join(path,"all_results_optimal_params.xlsx")
# file_16 = r"d:\Mon_hoc\NCKH\LinhLamTCoi\IndexRF_KFold\Summary_RFKFold\Summary.xlsx"
file_16 = r"d:\Mon_hoc\NCKH\AccModel\SVM\Summary\Summary.xlsx"

df_all = pd.read_excel(file_all, engine="openpyxl")
df_opt = pd.read_excel(file_16, engine="openpyxl")

# Xác định các cột tham số để đối chiếu (khóa chung)
# param_cols = ["numberOfTrees", "variablesPerSplit", "minLeafPopulation", "bagFraction"]
param_cols = ["gamma", "cost"]
# Giữ lại trong df_all những dòng trùng với 16 bộ tham số trong df_opt
df_filtered = df_all.merge(df_opt[param_cols], on=param_cols, how="inner")

# Xuất ra file Excel mới
# output_file = r"D:\Mon_hoc\NCKH\LinhLamTCoi\IndexRF_KFold\filtered_16_params.xlsx"
output_file = path+ "filtered_16_params.xlsx"
df_filtered.to_excel(output_file, index=False, engine="openpyxl")
print(f"✅ Đã lọc ra 16 dòng tham số tối ưu, lưu tại: {output_file}")


df = pd.read_excel(output_file)

# Nhóm theo bộ tham số và tính trung bình meanAccuracy
df_avg = df.groupby(param_cols, as_index=False)["meanAccuracy"].mean()

# Sắp xếp từ cao xuống thấp để chọn top 3
df_avg = df_avg.sort_values(by="meanAccuracy", ascending=False)

# Xuất ra file
out_path =os.path.join(path,"optimal_params_avg.xlsx")
df_avg.to_excel(out_path, index=False)

print(f"Đã lưu kết quả tại: {out_path}")
print(df_avg.head(3))



