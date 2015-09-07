pyClusterAnlysis is a python program which can read .xyz movie file and analyze the cluster of particles in the file.
The program generally take into 4 input paramenters 1) moviefile.xyz 2)(int) idxMovieStart 3)(float)wellWidth and 4)(float)sphereThreshold, e.g.
python pyClusterAnalysis movie.xyz 1 1.5 0.2
Noting that sphereThreshold 0 means spherical clusters, 0.5 means disks and 1 means rods.
The program also need a parameter input file as "Analysis.input". This file should have the following format:
(float)temperature (float)rho (int)numberOfParticles
(float)boxX (float)boxY (float)boxZ
The output of this program is the cluster size distribution with 2 output files with the distribution of spherical clusters(sphere_dist.dat) and non-spherical clusters(nonsphere_dist.dat).
