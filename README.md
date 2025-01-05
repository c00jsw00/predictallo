# predictallo
RhoGAP-class-IX-myosins-allosteric
1. wget http://files.rcsb.org/download/6z2s.pdb
1. grep ATOM 6z2s.pdb > rec.pdb
2. grep Q5Q 6z2s.pdb > lig.pdb
3. wget https://github.com/gnina/gnina/releases/download/v1.1/gnina
4. chmod +x gnina
5. ./gnina --help
6.  python 7-predict-allo.py rec.pdb   (The mesh part represents a predicted allosteric binding site (PABS). Our predicted PABS is capable of encompassing the allosteric inhibitor Q5Q. Additionally, another compound displayed in molecular form is ADP metavanadate)
![allo](https://github.com/user-attachments/assets/7d8ac510-3480-4e8e-aade-82adb0f5797e)
7. 
