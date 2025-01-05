# predictallo
RhoGAP-class-IX-myosins-allosteric
1. wget http://files.rcsb.org/download/6z2s.pdb
1. grep ATOM 6z2s.pdb > rec.pdb
2. grep Q5Q 6z2s.pdb > lig.pdb
3. python generate_conf.py 6z2s.txt config.conf --receptor my_receptor.pdbqt --cpu 4 --num_modes 10
