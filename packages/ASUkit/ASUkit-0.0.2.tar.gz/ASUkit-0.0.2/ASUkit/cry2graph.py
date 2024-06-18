from ase.io import read
import numpy as np
from ase.db import connect
from ase.spacegroup import get_spacegroup, Spacegroup
from ase import Atoms
from ._utility._funs import *
import os
import pkg_resources
import pandas as pd
import json
import warnings


class parser():
    def __init__(self,database,entry_id):
        """
        This function processes a given database file and data ID to extract and return various graph-related data structures.

        Parameters:
            db_file (str): Path to the database file (e.g., 'cif.db').
            data_id (int): The ID of the data entry to be processed.

        Returns:
            tuple: A tuple containing the following elements:
                - node_embedding (np.ndarray): The node embeddings, 106-d.
                - masked_adj_matrix (np.ndarray): The masked adjacency matrix.
                - distance_matrix (np.ndarray): The distance matrix in Cartesian coordinates.
                - global_graph_info (np.ndarray): Global information about the graph, 140-d.

        Example:
            from ASUkit import cry2graph
            from ase.db import connect

            database = connect('cif.db')
            entry_id = 1

            node_embedding, adj_matrix, dis_matrix, global_info = cry2graph.parser(database, entry_id).get()
        """


        self.entry_id = entry_id
        self.database = database
        warnings.filterwarnings("ignore")
        _loc = pkg_resources.resource_filename('ASUkit', '')
        with open(os.path.join(_loc,'CGCNN_atom_emb.json') , 'r') as file:
            self.cgcnn_emb = json.load(file)

    def get(self):
        try:
            atoms = self.database.get_atoms(id=self.entry_id)
            N_symbols = atoms.get_chemical_symbols()  
            G_latt_consts = primitive2conveb(atoms)  
            G_spacegroup = get_spacegroup(atoms).no 
            G_latt_vol = atoms.get_volume() 
            G_ASUnum = atoms.get_global_number_of_atoms() 
            asu_atom_mass = atoms.get_masses() 
            spacegroup_obj = get_spacegroup(atoms)
            spacegroup_symbol = spacegroup_obj.symbol[0] 
            positions = atoms.get_positions() 
            sg = Spacegroup(G_spacegroup)
            sites,kinds = sg.equivalent_sites(positions)
            G_mass = sum(mass * kinds.count(index) for index, mass in enumerate(asu_atom_mass))     
            element_encode = symbol_to_atomic_number(N_symbols)
            # 11-d : lattice cell constants (6) ; spacegroup ; ASU number ; total node number; volume ; mass
            global_info = [G_latt_consts[0],G_latt_consts[1],G_latt_consts[2],G_latt_consts[3],
                        G_latt_consts[4],G_latt_consts[5],G_spacegroup,G_ASUnum,len(kinds),G_latt_vol,G_mass]
            # 95-d, CGCNN embedding + fractional coordinates
            node_emd = []
            for index, code in enumerate(kinds):
                _code = element_encode[code] # covert the node index of asu list to periodic table number
                value = self.cgcnn_emb[str(_code)] # 92-d
                node_emd.append(np.array(value + sites[index].tolist()+ global_info)) # 92+3+11 : 106-d
            crystal_system = space_group_to_crystal_system(G_spacegroup) 
            AtomCoordinates = covert2WPEMformat(sites,kinds,N_symbols)
            _,global_graph = xrdsim(G_latt_vol,spacegroup_symbol,AtomCoordinates,G_latt_consts,crystal_system) # 140-d
            # self connections, infilled 1 on edge between same asu  and infilled 1/dis on edge between diff ASU
            asu_dis_matrix = atoms.get_all_distances()
            np.fill_diagonal(asu_dis_matrix, asu_dis_matrix.diagonal() + 1)
            asu_dis_matrix = 1 / asu_dis_matrix
            adj_matrix =  np.zeros((len(kinds),len(kinds)))
            for i in range(len(kinds)):
                for j in range(len(kinds)):
                    row = kinds[i] # read in the asu code
                    col = kinds[j] # read in the asu code
                    adj_matrix[i,j] = asu_dis_matrix[row,col]
            # cut to 1.1
            adj_matrix = np.array(adj_matrix)
            adj_matrix[adj_matrix > 1.1] = 1.1
            
            _atoms = Atoms('X' * len(sites), positions=sites)
            distance_matrix = _atoms.get_all_distances()

        except Exception as e:
            print("An error occurred in testing dataset: crystal id = {}".format(self.entry_id), e)
            return None
        
        return np.array(node_emd),adj_matrix, distance_matrix, global_graph
    

# ----------------------------------------------------------------
def covert2WPEMformat(sites, kinds, N_symbols):
    sites_list = sites.tolist()  
    for i in range(len(sites_list)):
        sites_list[i].insert(0, N_symbols[kinds[i]])
    return sites_list 

def space_group_to_crystal_system(space_group):
    if space_group < 1 or space_group > 230:
        return "Invalid space group number"
    elif space_group <= 2:
        return 7  
    elif space_group <= 15:
        return 6  
    elif space_group <= 74:
        return 4  
    elif space_group <= 142:
        return 3 
    elif space_group <= 167:
        return 5  
    elif space_group <= 194:
        return 2 
    else:
        return 1 
    

def xrdsim(Volume,Point_group,AtomCoordinates,latt,crystal_system,):
    # idear diffraction pattern with finite broadening 
    wavelength = 1.54184
    two_theta_range = (10, 80.0,0.5) 
    grid, d_list = Diffraction_index(crystal_system,latt,wavelength,two_theta_range)
    res_HKL, _, d_res_HKL, _ = cal_extinction(Point_group, grid,d_list,crystal_system,AtomCoordinates,wavelength,)
    mu_array = 2 * np.arcsin(wavelength /2/np.array(d_res_HKL)) * 180 / np.pi

    FHKL_square = []
    Mult = []
    for angle in range(len(res_HKL)):
        FHKL_square_left = 0
        FHKL_square_right = 0
        # _Atom_coordinate all atoms in lattice cell
        for atom in range(len(AtomCoordinates)):
            fi = cal_atoms(AtomCoordinates[atom][0],mu_array[angle], wavelength)
            FHKL_square_left += fi * np.cos(2 * np.pi * (AtomCoordinates[atom][1] * res_HKL[angle][0] +
                                                AtomCoordinates[atom][2] * res_HKL[angle][1] + AtomCoordinates[atom][3] * res_HKL[angle][2]))
            FHKL_square_right += fi * np.sin(2 * np.pi * (AtomCoordinates[atom][1] * res_HKL[angle][0] +
                                                AtomCoordinates[atom][2] * res_HKL[angle][1] + AtomCoordinates[atom][3] * res_HKL[angle][2]))
        Mult.append(mult_rule(res_HKL[angle][0],res_HKL[angle][1],res_HKL[angle][2],crystal_system))
        FHKL_square.append(FHKL_square_left ** 2 + FHKL_square_right ** 2)
        
    
  
    Ints = [] # cal peak intensity
    for angle in range(len(FHKL_square)):
        Ints.append(float(FHKL_square[angle] * Mult[angle] / Volume ** 2
                    * (1 + np.cos(mu_array[angle] * np.pi/180) ** 2) / (np.sin(mu_array[angle] / 2 * np.pi/180) **2 * np.cos(Mult[angle] / 2 * np.pi/180))))
    

    Γ = 0.888*wavelength/(20 * np.cos(np.radians(np.array(mu_array)/2))) # GrainSize = 20nm 
    gamma_list = Γ / 2 + 1e-10
    sigma2_list = Γ**2 / (8*np.sqrt(2)) + 1e-10


    x_sim = np.arange(two_theta_range[0],two_theta_range[1],two_theta_range[2])
    y_sim = 0
    for num in range(len(Ints)):
        _ = draw_peak_density(x_sim, Ints[num], mu_array[num], gamma_list[num], sigma2_list[num])
        y_sim += _
    # normalize the profile
    nor_y = y_sim / theta_intensity_area(x_sim,y_sim)
    
    # x_dis is 1.2 to 8.8
    return None, nor_y












