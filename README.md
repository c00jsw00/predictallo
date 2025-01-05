# predictallo
RhoGAP-class-IX-myosins-allosteric
1. wget http://files.rcsb.org/download/6z2s.pdb
2. grep ATOM 6z2s.pdb > rec.pdb
3. grep Q5Q 6z2s.pdb > lig.pdb
4.  python 7-predict-allo.py rec.pdb   (The mesh part represents a predicted allosteric binding site (PABS). Our predicted PABS is capable of encompassing the allosteric inhibitor Q5Q. Additionally, another compound displayed in molecular form is ADP metavanadate)
![allo](https://github.com/user-attachments/assets/7d8ac510-3480-4e8e-aade-82adb0f5797e)
5. wget https://github.com/ccsb-scripps/AutoDock-Vina/releases/download/v1.2.5/vina_1.2.5_linux_x86_64
6. chmod 755 vina_1.2.5_linux_x86_64
7. obabel rec.pdb -xr -O rec.pdbqt
8. obabel lig.pdb -O lig.pdbqt
9. python generate_conf.py --receptor rec.pdbqt --cpu 32 --num_modes 1000 rec.pdb conf
10. ./vina_1.2.5_linux_x86_64  --config conf --ligand lig.pdbqt --out lig-out.pdbqt
