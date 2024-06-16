import numpy as np
import pandas as pd
try:
    import openmm as mm
    import openmm.unit as unit
except ImportError:
    import simtk.openmm as mm
    import simtk.unit as unit
from openabc.lib import NA, kB, EC, VEP
import sys
import os

def harmonic_bond_term(df_bonds, use_pbc, force_group=1):
    """
    Harmonic bond term. 
    
    Parameters
    ----------
    df_bonds : pd.DataFrame
        Information for all the bonds. 
    
    use_pbc : bool
        Whether to use PBC. 
    
    force_group : int
        Force group.
    
    Returns
    -------
    bonds : Force
        OpenMM force object. 
    
    """
    bonds = mm.HarmonicBondForce()
    for _, row in df_bonds.iterrows():
        a1 = int(row['a1'])
        a2 = int(row['a2'])
        r0 = row['r0']
        k_bond = row['k_bond']
        bonds.addBond(a1, a2, r0, k_bond)
    bonds.setUsesPeriodicBoundaryConditions(use_pbc)
    bonds.setForceGroup(force_group)
    return bonds


def native_pair_gaussian_term(df_native_pairs, use_pbc, force_group=4):
    """
    Native pair term with Gaussian well. 
    
    Parameters epsilon_G, sigma_G, alpha_G all have _G to highlight these parameters are used in the native pair potential with Gaussian well. 
    """
    bonds = mm.CustomBondForce('''energy;
            energy=(-epsilon_G*G+alpha_G*(1-G)/r^12-offset)*step(cutoff-r);
            offset=-epsilon_G*exp(-18)+alpha_G*(1-exp(-18))/cutoff^12;
            cutoff=mu+6*sigma_G;
            G=exp(-(r-mu)^2/(2*sigma_G^2))''')
    bonds.addPerBondParameter('epsilon_G')
    bonds.addPerBondParameter('mu')
    bonds.addPerBondParameter('sigma_G')
    bonds.addPerBondParameter('alpha_G')
    for _, row in df_native_pairs.iterrows():
        a1 = int(row['a1'])
        a2 = int(row['a2'])
        epsilon_G = float(row['epsilon_G'])
        mu = float(row['mu'])
        sigma_G = float(row['sigma_G'])
        alpha_G = float(row['alpha_G'])
        bonds.addBond(a1, a2, [epsilon_G, mu, sigma_G, alpha_G])
    bonds.setUsesPeriodicBoundaryConditions(use_pbc)
    bonds.setForceGroup(force_group)
    return bonds


def native_pair_12_10_term(df_native_pairs, use_pbc, force_group=4):
    """
    A 12-10 potential for native pairs. 
    mu is the lowest energy distance for the 12-10 potential.
    
    Parameters
    ----------
    df_native_pairs : pd.DataFrame
        Information for all the native pairs. 
    
    use_pbc : bool
        Whether to use PBC. 
    
    force_group : int
        Force group.
    
    Returns
    -------
    bonds : Force
        OpenMM force object. 
    
    """
    bonds = mm.CustomBondForce('epsilon*(5*(mu/r)^12-6*(mu/r)^10)')
    bonds.addPerBondParameter('epsilon')
    bonds.addPerBondParameter('mu')
    for _, row in df_native_pairs.iterrows():
        a1 = int(row['a1'])
        a2 = int(row['a2'])
        epsilon = row['epsilon']
        mu = row['mu']
        bonds.addBond(a1, a2, [epsilon, mu])
    bonds.setUsesPeriodicBoundaryConditions(use_pbc)
    bonds.setForceGroup(force_group)
    return bonds


def class2_bond_term(df_bonds, use_pbc, force_group=1):
    """
    Class2 bond term. 
    
    Parameters
    ----------
    df_bonds : pd.DataFrame
        Information for all the bonds. 
    
    use_pbc : bool
        Whether to use PBC. 
    
    force_group : int
        Force group.
    
    Returns
    -------
    bonds : Force
        OpenMM force object. 
    
    """
    bonds = mm.CustomBondForce('k_bond_2*(r-r0)^2+k_bond_3*(r-r0)^3+k_bond_4*(r-r0)^4')
    bonds.addPerBondParameter('r0')
    bonds.addPerBondParameter('k_bond_2')
    bonds.addPerBondParameter('k_bond_3')
    bonds.addPerBondParameter('k_bond_4')
    for _, row in df_bonds.iterrows():
        a1 = int(row['a1'])
        a2 = int(row['a2'])
        parameters = row[['r0', 'k_bond_2', 'k_bond_3', 'k_bond_4']].tolist()
        bonds.addBond(a1, a2, parameters)
    bonds.setUsesPeriodicBoundaryConditions(use_pbc)
    bonds.setForceGroup(force_group)
    return bonds


def ddd_dh_elec_switch_bond_term(df_bonds, use_pbc, salt_conc=150.0*unit.millimolar, temperature=300.0*unit.kelvin, 
                                 cutoff1=1.2*unit.nanometer, cutoff2=1.5*unit.nanometer, 
                                 switch_coeff=[1, 0, 0, -10, 15, -6], force_group=6):
    """
    A bonded form of Debye-Huckel potential with distance-dependent dielectric and a switch function. 
    
    Parameters
    ----------
    df_bonds : pd.DataFrame
        Information for all the bonds. 
    
    use_pbc : bool
        Whether to use PBC. 
    
    salt_conc : Quantity
        Monovalent salt concentration.
    
    temperature : Quantity
        Temperature.
    
    cutoff1 : Quantity
        Cutoff distance 1.
    
    cutoff2 : Quantity
        Cutoff distance 2. 
    
    switch_coeff : list
        Switch function coefficients. 
    
    force_group : int
        Force group. 
    
    """
    alpha = NA*EC**2/(4*np.pi*VEP)
    gamma = VEP*kB*temperature/(2.0*NA*salt_conc*EC**2)
    # use a distance-dependent relative permittivity (dielectric)
    dielectric_water = 78.4
    A = -8.5525
    kappa = 7.7839
    B = dielectric_water - A
    zeta = 0.03627
    alpha_value = alpha.value_in_unit(unit.kilojoule_per_mole*unit.nanometer)
    cutoff1_value = cutoff1.value_in_unit(unit.nanometer)
    cutoff2_value = cutoff2.value_in_unit(unit.nanometer)
    gamma_value = gamma.value_in_unit(unit.nanometer**2)
    assert switch_coeff[0] == 1
    assert np.sum(np.array(switch_coeff)) == 0
    switch_term_list = []
    for i in range(len(switch_coeff)):
        if i == 0:
            switch_term_list.append(f'{switch_coeff[i]}')
        else:
            switch_term_list.append(f'({switch_coeff[i]}*((r-{cutoff1_value})/({cutoff2_value}-{cutoff1_value}))^{i})')
    switch_term_string = '+'.join(switch_term_list)
    bonds = mm.CustomBondForce(f'''energy;
            energy=q1_times_q2*{alpha_value}*exp(-r/ldby)*switch/(dielectric*r);
            switch=({switch_term_string})*step(r-{cutoff1_value})*step({cutoff2_value}-r)+step({cutoff1_value}-r);
            ldby=(dielectric*{gamma_value})^0.5;
            dielectric={A}+{B}/(1+{kappa}*exp(-{zeta}*{B}*r));
            ''')
    bonds.addPerBondParameter('q1_times_q2')
    for _, row in df_bonds.iterrows():
        a1 = int(row['a1'])
        a2 = int(row['a2'])
        q1 = float(row['q1'])
        q2 = float(row['q2'])
        if (q1 != 0) and (q2 != 0):
            bonds.addBond(a1, a2, [q1*q2])
    bonds.setUsesPeriodicBoundaryConditions(use_pbc)
    bonds.setForceGroup(force_group)
    return bonds



