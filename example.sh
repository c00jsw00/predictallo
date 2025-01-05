#!/bin/bash

# 下載 PDB 文件
wget http://files.rcsb.org/download/6z2s.pdb

# 提取 ATOM 行並保存到 rec.pdb
grep ATOM 6z2s.pdb > rec.pdb

# 提取 Q5Q 行並保存到 lig.pdb
grep Q5Q 6z2s.pdb > lig.pdb

# 運行 Python 腳本進行預測
python 7-predict-allo.py rec.pdb

# 下載 gnina
wget https://github.com/gnina/gnina/releases/download/v1.1/gnina

# 賦予 gnina 執行權限
chmod 755 gnina

# 將 rec.pdb 轉換為 rec.pdbqt
obabel rec.pdb -xr -O rec.pdbqt

# 將 lig.pdb 轉換為 lig.pdbqt
obabel lig.pdb -O lig.pdbqt

# 運行 ConvexHull.py 腳本
python ConvexHull.py rec_out/allosteric_predictsite.pqr ConvexHull.pdb ConvexHull_center.pdb

# 使用 gnina 進行對接
./gnina -r rec.pdb -l lig.pdb --autobox_ligand ConvexHull_center.pdb -o docked.sdf --seed 0 --num_modes 100

# 運行 top5.py 腳本
python top5.py docked.sdf