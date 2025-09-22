import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm as cm

# --- Đọc file CSV ---
df = pd.read_csv(r"d:\Mon_hoc\NCKH\SVM_grid_results_allRepeats_2018_Q03.csv")

# Nếu file có cột "meanAccuracy" thì chuẩn hoá tên thành "accuracy"
if "meanAccuracy" in df.columns and "accuracy" not in df.columns:
    df["accuracy"] = df["meanAccuracy"]

# --- Tìm ngưỡng tối ưu (max accuracy) ---
best_row = df.loc[df["accuracy"].idxmax()]
print("Ngưỡng tối ưu:")
print(best_row)

# --- Hàm tìm ngưỡng bão hòa ---
def SaturationThreshold(df, x_col="gamma", y_col="accuracy", epsilon=0.001):
    df_sorted = df.sort_values(x_col).reset_index(drop=True)
    df_sorted["delta_acc"] = df_sorted[y_col].diff()

    # Vẽ biểu đồ 2D
    plt.figure(figsize=(8,5))
    plt.plot(df_sorted[x_col], df_sorted[y_col], marker="o", label="Accuracy")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"Accuracy vs {x_col}")
    plt.grid(True)
    plt.legend()
    # plt.show()

    # Tìm ngưỡng bão hòa (đầu tiên delta nhỏ hơn epsilon)
    sat_points = df_sorted[df_sorted["delta_acc"].abs() < epsilon]
    if not sat_points.empty:
        sat_point = sat_points.iloc[0]
        return sat_point[x_col], sat_point[y_col]
    else:
        return None

# sat_gamma = SaturationThreshold(df, x_col="gamma", y_col="accuracy")
# print("Ngưỡng bão hòa:", sat_gamma)

# --- Hàm vẽ stem plot 3D với colormap ---
def plot_svm_3d_colormap(df, gamma_col="gamma", cost_col="cost", acc_col="accuracy", cmap_name="viridis"):
    gamma = df[gamma_col].values
    cost = df[cost_col].values
    accuracy = df[acc_col].values

    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111, projection="3d")

    # Tạo chuỗi màu từ colormap
    cmap = cm.get_cmap(cmap_name)
    colors = cmap(np.linspace(0, 1, len(gamma)))

    for (g, c, a, col) in zip(gamma, cost, accuracy, colors):
        ax.plot([g, g], [c, c], [0, a], color=col, alpha=0.5)  # stem line
        ax.scatter(g, c, a, s=50, c=[col], alpha=0.9)          # point

    ax.set_xlabel("Gamma")
    ax.set_ylabel("Cost")
    ax.set_zlabel("Accuracy")
    ax.set_title(f"SVM Grid Search - Stem 3D Plot ({cmap_name} colormap)")
    plt.show()

# # --- Gọi hàm vẽ 3D ---
plot_svm_3d_colormap(df, gamma_col="gamma", cost_col="cost", acc_col="accuracy", cmap_name="plasma")
