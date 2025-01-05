# predictallo
RhoGAP-class-IX-myosins-allosteric
1. wget http://files.rcsb.org/download/6z2s.pdb
2. grep ATOM 6z2s.pdb > rec.pdb
3. grep Q5Q 6z2s.pdb > lig.pdb
4.  python 7-predict-allo.py rec.pdb
5.  (The mesh part represents a predicted allosteric binding site (PABS). Our predicted PABS is capable of encompassing the allosteric inhibitor Q5Q. Additionally, another compound displayed in molecular form is ADP metavanadate)
![allo](https://github.com/user-attachments/assets/7d8ac510-3480-4e8e-aade-82adb0f5797e)
6. wget https://github.com/gnina/gnina/releases/download/v1.1/gnina
7. chmod 755 gnina
8. obabel rec.pdb -xr -O rec.pdbqt
9. obabel lig.pdb -O lig.pdbqt
10.  python ConvexHull.py rec_out/allosteric_predictsite.pqr ConvexHull.pdb ConvexHull_center.pdb
11. ./gnina -r rec.pdb -l lig.pdb --autobox_ligand ConvexHull_center.pdb -o docked.sdf --seed 0 --num_modes 100
12. python top5.py docked.sdf
![allo2](https://github.com/user-attachments/assets/5c0fc982-dfd0-4518-99fe-d10fe715ab32)

