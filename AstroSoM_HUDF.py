import numpy as np
import os

'''
============================================
Astro-SoM #1: Hubble Ultra-Deep Field (HUDF)
============================================
To produce the products for the HUDF sonification, simply run this command from the terminal:
>> python AstroSoM_HUDF.py

The Hubble Space Telescope stared at one dark patch of sky for over 11 days. The result is the Hubble Ultra-Deep Field (HUDF): an image of 10,000 galaxies! Recently, a research team of astronomers measured the distances to all of these galaxies as far away as 13.1 billion light-years. We are seeing these most distant galaxies as they were when the Universe was only about 800 million years old, which is analogous to obtaining a snapshot of a 50 year old person when they were 3 years old.

In this month's Astro-SoM, we will produce an interactive image of the Hubble Ultra-Deep Field. Moving your mouse over any galaxy will play a note indicating how far away that galaxy is from us.
'''
#====================================================================================================
# STEP 1: Make individual MP3/OGG files for every MIDI note.

# Install the prerequisite software.
# >> pip install miditime
# >> brew install timidity
# >> brew install lame

# Loop through all 128 MIDI notes and output the sound files. We won't use them all, but that's okay.
from midi_notes import *
outdir = "/Users/salvesen/outreach/asom/hudf/results/notes/"
Nmidi_min = 0
Nmidi_max = 127
N = Nmidi_max - Nmidi_min + 1
Nmidi_arr = np.linspace(Nmidi_min, Nmidi_max, N)
for i in np.arange(N):
    Nmidi = int(Nmidi_arr[i])
    make_note(Nmidi=Nmidi, outdir=outdir)


#====================================================================================================
# STEP 2: Map pitch to the distance to each galaxy (in light-years).

# Download the FITS file containing the redshift for each galaxy (Table 5 from Rafelski et al. 2015).
# Install the prerequisite software.
# >> pip install astropy

# Determine the MIDI note to play for each galaxy.
from map_galaxies2notes import *
fits_file = "/Users/salvesen/outreach/asom/hudf/data/uvudf_rafelski_2015.fits"
IDgal_list, Nmidi_list = get_IDgal_Nmidi_lists(fits_file)

# How many galaxies are further away than X light-years?
# (For this to work, need to get "t" <-- see map_galaxies2notes.py)
#D    = 5.9e9  # [light-years]
#Ngal = len(np.where(t > D)[0])
#print "Fraction of galaxies: ", Ngal / float(len(t))


#====================================================================================================
# STEP 3: Align the HUDF press release image with the segmentation map.

# Download the pretty HUDF press release image.
# Download the Segmentation Map FITS file, which contains spatial information for each galaxy (Rafelski et al. 2015).
# Produce a re-scaled Segmentation Map image the overlaps with the HUDF image.
os.system("python rescale_segmap.py")

# That's it! Well, sorta. We still have to write the HTML code, which turned out to be the most challenging part for me.

