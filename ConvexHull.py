import numpy as np
from scipy.spatial import ConvexHull
import sys

# 從 pocket.txt 中提取原子座標
def extract_pocket_coordinates(pocket_file):
    coordinates = []
    with open(pocket_file, 'r') as f:
        for line in f:
            if line.startswith("ATOM"):
                parts = line.split()
                x = float(parts[5])
                y = float(parts[6])
                z = float(parts[7])
                coordinates.append([x, y, z])
    return np.array(coordinates)

# 將凸包保存為 PDB 文件
def save_hull_as_pdb(hull, output_file):
    with open(output_file, 'w') as f:
        # 寫入頂點作為 HETATM 記錄
        for i, vertex in enumerate(hull.points[hull.vertices]):
            f.write(f"HETATM{i+1:5}  V   VOX A   1    {vertex[0]:8.3f}{vertex[1]:8.3f}{vertex[2]:8.3f}  1.00  0.00          V\n")
        
        # 寫入連接信息（CONECT 記錄）
        vertex_map = {v: i for i, v in enumerate(hull.vertices)}
        for simplex in hull.simplices:
            atoms = [vertex_map[i] + 1 for i in simplex]
            f.write(f"CONECT{atoms[0]:5}{atoms[1]:5}{atoms[2]:5}\n")

# 計算凸包的質心
def calculate_centroid(hull):
    vertices = hull.points[hull.vertices]
    centroid = np.mean(vertices, axis=0)
    return centroid

# 將質心保存為 PDB 文件
def save_centroid_as_pdb(centroid, output_file):
    with open(output_file, 'w') as f:
        f.write(f"HETATM    1  CEN CEN A   1    {centroid[0]:8.3f}{centroid[1]:8.3f}{centroid[2]:8.3f}  1.00  0.00          C\n")

# 主程序
if __name__ == "__main__":
    # 檢查命令行參數
    if len(sys.argv) != 4:
        print("使用方法: python script.py <pocket文件> <凸包PDB文件> <質心PDB文件>")
        sys.exit(1)

    # 從命令行參數獲取文件名
    pocket_file = sys.argv[1]
    hull_output_file = sys.argv[2]
    centroid_output_file = sys.argv[3]

    # 提取座標
    pocket_coords = extract_pocket_coordinates(pocket_file)

    # 生成凸包
    hull = ConvexHull(pocket_coords)

    # 將凸包保存為 PDB 文件
    save_hull_as_pdb(hull, hull_output_file)
    print(f"凸包已保存為 {hull_output_file}")

    # 計算質心並保存為 PDB 文件
    centroid = calculate_centroid(hull)
    save_centroid_as_pdb(centroid, centroid_output_file)
    print(f"質心已保存為 {centroid_output_file}")
