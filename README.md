# predictallo
RhoGAP-class-IX-myosins-allosteric
1. wget http://files.rcsb.org/download/6z2s.pdb
2. grep ATOM 6z2s.pdb > rec.pdb
3. grep Q5Q 6z2s.pdb > lig.pdb
4.  python 7-predict-allo.py rec.pdb   (The mesh part represents a predicted allosteric binding site (PABS). Our predicted PABS is capable of encompassing the allosteric inhibitor Q5Q. Additionally, another compound displayed in molecular form is ADP metavanadate)
![allo](https://github.com/user-attachments/assets/7d8ac510-3480-4e8e-aade-82adb0f5797e)
5. git clone https://github.com/QVina/qvina.git
6. chmod u+x qvina/bin/qvina-w
7. obabel rec.pdb -xr -O rec.pdbqt
8. obabel lig.pdb -xr -O lig.pdbqt
9. python generate_conf.py --receptor rec.pdbqt --cpu 32 --num_modes 1000 rec.pdb conf
10.  ./gnina -r rec.pdb -l lig.pdb --autobox_ligand rec.pdb -o docked.sdf --seed 0 --num_modes 10000
