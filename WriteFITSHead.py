#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 11:34:16 2023

@author: danakoeppe
"""

import numpy as np
import pandas as pd
import os

from astropy.io import fits


class FITSHead():
    """
    Obtain instrument configurations, WCS, etc. and
        keep track of them with a dictionary.
    After exposure, write the contents of dictionary to FITS header
        using header.set(key,val,comment)
    
    """
    
    def __init__(self):
        
        self.filename = None
        
        self.expTime = {'EXPTIME':None}
        self.objName = {'OBJECT': None} # 'OBJECT' name of object i.e. ABELL S1101
        self.obsType = {'OBSTYPE': None} # 'OBSTYPE' type of observation i.e. BIAS, FLAT, OBJ...
        self.radecSys = {'RADECSYS': 'FK5'} # 'RADECSYS' default coordinate system, prob won't change
        self.radecEq = {'RADECEQ': 2000} # 'RADECEQ' default equinox, prob won't change
        self.ra = {'RA': None} # 'RA' RA of object [hr]
        self.dec = {'DEC': None} # 'DEC' DEC of object [deg]
        
        # ---------parameters from SAM adaptive optics module (AOM)--------- #
        
        ### motor controllers, switches, and telemetry boards of AOM are connected to the instrument computer (IC)
        self.telRA = {'TELRA':None} # 'TELRA' telescope pointing RA [hr]
        self.telDEC = {'TELDEC': None} # 'TELDEC' telescope pointing DEC [deg]
        self.hourangle = {'HA': None} # 'HA' hourangle [H:M:S]
        self.airmass = {'AIRMASS': None} # airmass at time of observation
        
        ## position angle of the RA and DEC axes relative to the +Y axis of CCD, positive is CCW        
        self.rapangl = {'RAPANGL': None} # position angle PA-90
        self.decpangl = {'DECPANGL': None} # position angle PA
        
        # ----------------------- #
        
        # ---------WCS related parameters--------- #
        # can probably just be fully imported after astrometry is complete
        # but writing them here for now
        
        ### SAMOS Imaging CCD parameters
        self.pixsize1 = {'PIXSIZE1': 13} # serial pixel size in microns
        self.pixsize2 = {'PIXSIZE2': 13} # parallel pixel size in microns
        self.pixscale1 = {'PIXSCALE1': 0.17} # serial unbinned pixel scale 1
        self.pixscale2 = {'PIXSCALE2': 0.17} # parallel unbinned pixel scale 2
        
        # matrix elements for astrometric solution
        
        self.wcsdim = {'WCSDIM': 2}
        self.ctype1 = {'CTYPE1': 'RA---TAN'} # RA---TAN-SIP? for distorion
        self.ctype2 = {'CTYPE2': 'DEC--TAN'} # DEC--TAN-SIP?
        self.crval1 = {'CRVAL1': None} # reference RA coordinate
        self.crval2 = {'CRVAL2': None} # reference DEC coordinate
        self.crpix1 = {'CRPIX1': None} # reference serial pixel coordinate
        self.crpix2 = {'CRPIX2': None} # reference parallel pixel coordinate
        self.cd11 = {'CD1_1': None}
        self.cd22 = {'CD2_2': None}
        self.cd12 = {'CD1_2': None}
        self.cd21 = {'CD2_1': None}
        self.cdelt1 = {'CDELT1': None} # degrees per pixel serial direction
        self.cdelt2 = {'CDELT2': None} # degrees per pixel parallel direction
        
        
        # ----------------------- #
        
        
        # ---------SAMOS configuration parameters--------- #
        
        self.filters = {'FILTERS': None} # names of filter wheels in A and B
        self.filter1 = {'FILTER1': None} # name of filter wheel A
        self.filter2 = {'FILTER2': None} # name of filter wheel B
        self.filtpos = {'FILTPOS': None} # filter position wheel A and wheel B ex. 'FW_A1 FW_B3'
        
    
    
FITSHead()
        
        
        
        