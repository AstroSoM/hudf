import numpy as np
from astropy.io import fits
from scipy.integrate import simps
from midi_notes import midi_note

#====================================================================================================
def lookback_time(z, H0=69.6, Omega=0.286, Omega_k=0.0, Omega_L=0.714, Nz=1000):
    '''
    Input: Redshift
    Output: Lookback time [light-years]

    Adopt a Hubble constant of H0 = 69.6 km s^-1 Mpc^-1 and standard cosmology (Bennett et al. 2014).
    '''
    # Conversion factor for Hubble constant: [km s^-1 Mpc^-1] --> [yr^-1]
    Mpc2km = 3.0857e19                     # [km Mpc^-1]
    sec2yr = 1.0 / 3600.0 / 24.0 / 365.25  # [s yr^-1]
    H0_cgs = H0 / Mpc2km / sec2yr          # [yr^-1]
    if (z != 0.0):
        z_arr  = np.linspace(0.0, z, Nz)
        a_inv  = (1.0 + z_arr)
        Igrand = 1.0 / (a_inv * np.sqrt(Omega * a_inv**3 + Omega_k * a_inv**2 + Omega_L))
        t      = (1.0 / H0_cgs) * simps(y=Igrand, x=z_arr)  # [yr]
        return t
    else:  # Lookback time is zero if redshift is zero
        return 0.0


#====================================================================================================
def get_IDgal_Nmidi_lists(fits_file):
    '''
    Input: uvudf_rafelski_2015.fits
    Output: Two lists, one containing the galaxy IDs and the other the corresponding MIDI note numbers
    '''
    # Read in the FITS file for Table 5 from Rafelski et al. (2015)
    hdu_list = fits.open(fits_file)
    IDgal_list = hdu_list[1].data['ID']  # Galaxy ID
    zphotB = hdu_list[1].data['Z_BPZ']   # Photometric redshift
    zphotE = hdu_list[1].data['Z_EAZY']  # Photometric redshift
    zspec  = hdu_list[1].data['SPECZ']   # Spectroscopic redshift
    hdu_list.close()

    # Collect the redshifts to use for each galaxy
    #   - Use spectroscopic redshift if available
    #   - Otherwise, use the average of the two photometric redshifts
    N = len(IDgal_list)
    z = np.zeros(N)  # Redshift array
    t = np.zeros(N)  # Lookback time array
    for i in np.arange(N):
        if (zspec[i] != -99):
            z[i] = zspec[i]
        else:
            z[i] = (zphotB[i] + zphotE[i]) * 0.5
        # Calculate the lookback time [yr]
        t[i] = lookback_time(z[i])
        
    # Determine the note to play for each galaxy
    # The following choices for (tmin, tmax, dt) use all 88 piano notes (+5 more)
    tmin = 0.0     # Minimum lookback time [yr] (big bang)
    tmax = 13.8e9  # Maximum lookback time [yr] (age of the Universe)
    dt   = 0.15e9  # Lookback time increment corresponding to each semitone [yr]
    Nmidi_min = 21   # A1 - lowest note on a piano
    Nmidi_max = 113  # F9 - 5 semi-tones above the highest note on a piano
    Nmidi_list = []
    for i in np.arange(N):
        # Find the MIDI note number corresponding to the lookback time
        #   - Short (long) lookback times map to low (high) notes
        Nmidi = int(round((t[i] - tmin) / dt)) + Nmidi_min
        if (Nmidi < Nmidi_min): Nmidi = Nmidi_min
        if (Nmidi > Nmidi_max): Nmidi = Nmidi_max
        Nmidi_list.append(Nmidi)
    
    return IDgal_list, Nmidi_list


#====================================================================================================
