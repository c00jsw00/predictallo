import re
import sys

def extract_minimized_affinity(sdf_content):
    # 正則表達式匹配 minimizedAffinity 值
    pattern = re.compile(r"> <minimizedAffinity>\n(-?\d+\.\d+)")
    matches = pattern.findall(sdf_content)
    
    # 將匹配到的值轉換為浮點數
    minimized_affinities = [float(match) for match in matches]
    
    # 根據 minimizedAffinity 值排序（從小到大）
    minimized_affinities.sort()
    
    # 返回前五個值
    return minimized_affinities[:5]

def extract_molecule_blocks(sdf_content):
    # 使用正則表達式分割 SDF 內容為單個分子區塊
    molecule_blocks = re.split(r"\$\$\$\$", sdf_content)
    # 移除最後一個空區塊（如果有）
    if molecule_blocks[-1].strip() == "":
        molecule_blocks = molecule_blocks[:-1]
    return molecule_blocks

def find_molecules_by_affinity(sdf_content, top_affinities):
    molecule_blocks = extract_molecule_blocks(sdf_content)
    selected_molecules = []
    
    for block in molecule_blocks:
        # 在每個分子區塊中查找 minimizedAffinity 值
        match = re.search(r"> <minimizedAffinity>\n(-?\d+\.\d+)", block)
        if match:
            affinity = float(match.group(1))
            if affinity in top_affinities:
                selected_molecules.append(block)
    
    return selected_molecules

def save_molecules_to_sdf(molecules, output_file):
    # 將分子區塊寫入新的 SDF 檔案，並滿足格式要求
    with open(output_file, "w") as file:
        # 檔案開頭前三行是空的
        file.write("\n\n\n")
        
        for molecule in molecules:
            # 寫入分子區塊
            file.write(molecule.strip() + "\n")
            # $$$$ 前一行是空的
            file.write("\n$$$$\n")
            # $$$$ 後三行是空的
            file.write("\n\n\n")

def main():
    # 檢查是否提供了文件路徑作為參數
    if len(sys.argv) < 2:
        print("請提供 dock.txt 文件路徑作為參數。")
        return
    
    # 獲取文件路徑
    file_path = sys.argv[1]
    
    try:
        # 讀取文件內容
        with open(file_path, "r") as file:
            sdf_content = file.read()
        
        # 提取並排序 minimizedAffinity 值
        top_5_affinities = extract_minimized_affinity(sdf_content)
        print("Top 5 minimizedAffinity values:")
        for affinity in top_5_affinities:
            print(affinity)
        
        # 找到對應的分子區塊
        selected_molecules = find_molecules_by_affinity(sdf_content, top_5_affinities)
        
        # 將分子存成新的 SDF 檔案
        output_file = "top_5_molecules.sdf"
        save_molecules_to_sdf(selected_molecules, output_file)
        print(f"已將分子存儲到 {output_file}")
    
    except FileNotFoundError:
        print(f"錯誤：找不到文件 {file_path}，請檢查文件路徑。")
    except Exception as e:
        print(f"發生錯誤：{e}")

# 執行主程序
if __name__ == "__main__":
    main()
