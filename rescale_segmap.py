import numpy as np
import os
from PIL import Image
from astropy.io import fits
from scipy.misc import imread, toimage, imresize
from map_galaxies2notes import *

#====================================================================================================
'''
Produce a re-scaled version of the Segmentation Map that maps 1:1 to the HUDF image.

Outputs:
--------
HUDF_large.png - Full-size Hubble Ultra Deep Field press release image
HUDF_small.png - Reduced-size Hubble Ultra Deep Field press release image (800px wide)
NoteMap_large.csv - 2D array of notes mapped to each pixel in the full-size HUDF image
NoteMap_small.csv - 2D array of notes mapped to each pixel in the reduced-size HUDF image

MIDI_large.png - Map of MIDI note numbers corresponding to each pixel for the full-size HUDF image
MIDI_small.png - Map of MIDI note numbers corresponding to each pixel for the reduced-size HUDF image
SMap_large.png - Segmentation map that has been rescaled and aligned to the full-size HUDF image
SMap_small.png - Segmentation map that has been rescaled and aligned to the reduced-size HUDF image

*The MIDI and SMap output images are not actually ever used, but are nice to have anyways.
*They are currently commented out.
'''
#====================================================================================================
outdir = "/Users/salvesen/outreach/asom/hudf/results/"

# Read in the HUDF image (JPG) and get its size
imHUDF = "/Users/salvesen/outreach/asom/hudf/data/hs-2014-27-a-full_jpg.jpg"
imHUDF_data = imread(imHUDF)
Nx = imHUDF_data.shape[0]  # Number of X-pixels in the HUDF image
Ny = imHUDF_data.shape[1]  # Number of Y-pixels in the HUDF image

# Output a large and small (Nx = 900 px) HUDF image
imHUDF_large = toimage(imHUDF_data)
imHUDF_large.save(outdir+"HUDF_large.png", 'PNG')
frac = 800.0 / float(Ny)  # Fraction of current image size to obtain a small image with Ny = 800px
imHUDF_data = imresize(arr=imHUDF_large, size=frac)
imHUDF_small = toimage(imHUDF_data)
imHUDF_small.save(outdir+"HUDF_small.png", 'PNG')

# Get the galaxy ID list and the MIDI note list
fits_file = "/Users/salvesen/outreach/asom/hudf/data/uvudf_rafelski_2015.fits"
IDgal_list, Nmidi_list = get_IDgal_Nmidi_lists(fits_file)

'''
# Identifying galaxies to compute the coordinate transformation matrix
# !!! BE CAREFUL !!! x = y, y = x
axis('off')
subplot(1,2,1)
imshow(imHUDF_data)
subplot(1,2,2)
imshow(imSMap_data)
'''
# Mathematica gives the solution:
a = -1.2317
b = -1.57645
c = -1.57582
d = 1.23242
e = 9335.34
f = 5697.93

#====================================================================================================
def get_NoteMap(imHUDF, frac=1.0):
    '''
    Generate the Note Map for the large or small HUDF image.

    Input: Filename of the HUDF image and fraction by which to downsize the full-size HUDF
    Output: Note Map (2D list)
    '''
    imHUDF_data = imread(imHUDF)
    Nx = imHUDF_data.shape[0]  # Number of X-pixels in the HUDF image
    Ny = imHUDF_data.shape[1]  # Number of Y-pixels in the HUDF image
    
    # Read in the Segmentation Map image (pixel values correspond to galaxy ID numbers)
    imSMap = "/Users/salvesen/outreach/asom/hudf/data/segmentation_map_rafelski_2015.fits"
    hdu_list = fits.open(imSMap)
    imSMap_data = hdu_list[0].data
    hdu_list.close()

    # Create RGBA image arrays for the rescaled Segmentation Map and the MIDI Map
    #imSMap = Image.new('RGBA', (Nx, Ny))
    #imMIDI = Image.new('RGBA', (Nx, Ny))

    # Make a 2D list that will contain the MIDI note numbers corresponding to the Segmentation Map
    NoteMap = []

    # Loop through each pixel in the HUDF
    for i in np.arange(Nx):
    
        # Add an empty row
        NoteMap.append([])
    
        for j in np.arange(Ny):
        
            # Find the pixel in the SMap that corresponds to the current pixel in the HUDF
            xHUDF = i / frac
            yHUDF = j / frac
            xSMap = a * xHUDF + b * yHUDF + e
            ySMap = c * xHUDF + d * yHUDF + f

            # Populate the rescaled Smap with the proper galaxy ID
            iSMap = int(round(xSMap))
            jSMap = int(round(ySMap))
            IDgal = imSMap_data[iSMap, jSMap]
            IDgal_tuple = (IDgal, IDgal, IDgal, 255)
            #imSMap.putpixel((i,j), IDgal_tuple)

            # Populate the MIDI note map with the tone corresponding to the galaxy ID
            # (this part takes up the most of the computational time)
            if ((IDgal == 0) or (IDgal not in IDgal_list)):
                #toneRGBA = (255, 255, 255, 255)
                #imMIDI.putpixel((i,j), toneRGBA)  # There is no galaxy for this pixel, set RBG = 255
                NoteMap[i].append(-1)

            else:
                itone = np.where(IDgal_list == IDgal)[0]
                tone  = Nmidi_list[itone]
                #toneRGBA = (tone, tone, tone, 255)
                #imMIDI.putpixel((i,j), toneRGBA)
                NoteMap[i].append(tone)
    
        # Give a progress report every so often
        if ((i % 100) == 0):
            pctComplete = float(i)/float(Nx) * 100
            print "    % Complete: ", '{:.1f}'.format(pctComplete)

    # Output images of the Segmentation Map and MIDI Map
    #imSMap.save(outdir+"SMap.png", 'PNG')
    #imMIDI.save(outdir+"MIDIMap.png", 'PNG')
    #print Nx, Ny
    return NoteMap


#====================================================================================================
# Get the Note Maps for large/small HUDF image and output as CSV files

# Large Note Map
imHUDF_large  = outdir + "HUDF_large.png"
NoteMap_large = get_NoteMap(imHUDF=imHUDF_large, frac=1.0)
fout_large    = outdir + "NoteMap_large.csv"
file = open(fout_large, 'w')
for item in NoteMap_large:
    file.write(str(item)+"\n")
file.close()
os.system("sed -i 's/\[//g' " + fout_large)
os.system("sed -i 's/\]//g' " + fout_large)
os.system("sed -i 's/ //g' " + fout_large)

# Small Note Map
imHUDF_small  = outdir + "HUDF_small.png"
NoteMap_small = get_NoteMap(imHUDF=imHUDF_small, frac=frac)
fout_small    = outdir + "NoteMap_small.csv"
file = open(fout_small, 'w')
for item in NoteMap_small:
    file.write(str(item)+"\n")
file.close()
os.system("sed -i 's/\[//g' " + fout_small)
os.system("sed -i 's/\]//g' " + fout_small)
os.system("sed -i 's/ //g' " + fout_small)
