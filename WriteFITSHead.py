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
        
    Using dictionaries because they can keep track of the 
    header keyword, value, and comments.
    Each attribute can the be combined into a main param dict,
    which will get written to header.
    

    
    
    """
    
    def __init__(self):
        
        self.main_dict = None # main dictionary will be the container for all params
        
        self.filename = {'FILENAME' : None}
        
        self.expTime = {'EXPTIME': (None, 'Exposure time (s)')}
        self.objName = {'OBJECT': (None,'User-defined name of object')} # 'OBJECT' name of object i.e. ABELL S1101
        self.obsType = {'OBSTYPE': (None, 'Type of observation')} # 'OBSTYPE' type of observation i.e. BIAS, FLAT, OBJ...
        self.radecSys = {'RADECSYS': ('FK5', 'Default coordinate system')} # prob won't change
        self.radecEq = {'RADECEQ': (2000, 'Default equinox')} # prob won't change
        self.ra = {'RA': (None,'RA of object (hr)')}  
        self.dec = {'DEC': (None,'DEC of object (deg)')} 
        
        # ---------parameters from SAM adaptive optics module (AOM)--------- #
        
        ### motor controllers, switches, and telemetry boards of AOM are connected to the instrument computer (IC)
        self.telRA = {'TELRA':(None, 'RA of telescope (hr)')} 
        self.telDEC = {'TELDEC': (None, 'DEC of telescope (deg)')}
        self.hourangle = {'HA': (None, 'Hourangle (H:M:S)')} 
        self.airmass = {'AIRMASS': (None, 'Airmass')} 
        
        ## position angle of the RA and DEC axes relative to the +Y axis of CCD, positive is CCW        
        self.rapangl = {'RAPANGL': (None, 'Position angle of the RA axis (deg)')} # position angle PA-90
        self.decpangl = {'DECPANGL': (None, 'Position angle of the DEC axis (deg)')} # position angle PA
        
        # ----------------------- #
        
        # ---------WCS related parameters--------- #
        # can probably just be fully imported after astrometry is complete
        # but writing them here for now
        
        ### SAMOS Imaging CCD parameters
        self.pixsize1 = {'PIXSIZE1': (13, 'Unbinned pixel size for axis 1 (microns)')}
        self.pixsize2 = {'PIXSIZE2': (13, 'Unbinned pixel size for axis 2 (microns)')} 
        self.pixscale1 = {'PIXSCALE1': (0.17, 'Unbinned pixel scale for axis 1 (arcsec/pixel)')} 
        self.pixscale2 = {'PIXSCALE2': (0.17, 'Unbinned pixel scale for axis 2 (arcsec/pixel)')} 
        
        # matrix elements for astrometric solution
        
        self.wcsdim = {'WCSDIM': (2, 'WCS dimensionality')}
        self.ctype1 = {'CTYPE1': ('RA---TAN', 'Coordinate type')} # RA---TAN-SIP? for distorion
        self.ctype2 = {'CTYPE2': ('DEC--TAN', 'Coordinate type')} # DEC--TAN-SIP?
        self.crval1 = {'CRVAL1': (None, 'Coordinate reference value')} 
        self.crval2 = {'CRVAL2': (None, 'Coordinate reference value')} 
        self.crpix1 = {'CRPIX1': (None, 'Coordinate reference pixel')} 
        self.crpix2 = {'CRPIX2': (None, 'Coordinate reference pixel')} 
        self.cd11 = {'CD1_1': None}
        self.cd22 = {'CD2_2': None}
        self.cd12 = {'CD1_2': None}
        self.cd21 = {'CD2_1': None}
        self.cdelt1 = {'CDELT1': None} # degrees per pixel serial direction
        self.cdelt2 = {'CDELT2': None} # degrees per pixel parallel direction
        
        
        # ----------------------- #
        
        
        # ---------SAMOS configuration parameters--------- #
        # including params for spec side for completeness
        
        
        self.filters = {'FILTERS': (None, 'Names of filter wheels in A and B')}
        self.filter1 = {'FILTER1': (None, 'Name of filter wheel A')}
        self.filter2 = {'FILTER2': (None, 'Name of filter wheel B')}
        self.filtpos = {'FILTPOS': (None, 'Filter positions A and B')}
        self.grating = {'GRATING' : (None, 'VPH grating name')}
        self.dmdReg = {'DMDREG' : (None, 'Name of corresponding DMD .reg file')} # not a standard FITS keyword
        
    def create_main_params_dict(self):
        
        """
        Combine all the attributes into a single dictionary 
            that will be passed to the write_fits_header method.
        """
        
        ## need to put these in a better order
        
        self.main_dict = self.filename |\
                    self.expTime |\
                    self.objName |\
                    self.obsType |\
                    self.radecSys |\
                    self.radecEq |\
                    self.ra |\
                    self.dec |\
                    self.telRA |\
                    self.telDEC |\
                    self.hourangle |\
                    self.airmass | \
                    self.rapangl |\
                    self.decpangl |\
                    self.pixsize1 |\
                    self.pixsize2 |\
                    self.pixscale1 |\
                    self.pixscale2 |\
                    self.wcsdim |\
                    self.ctype1 |\
                    self.ctype2 |\
                    self.crval1 |\
                    self.crval2 |\
                    self.crpix1 |\
                    self.crpix2 |\
                    self.cd11 |\
                    self.cd22 |\
                    self.cd12 |\
                    self.cd21 |\
                    self.cdelt1 |\
                    self.cdelt2 |\
                    self.filters |\
                    self.filter1 |\
                    self.filter2 |\
                    self.filtpos |\
                    self.grating |\
                    self.dmdReg
        
    def write_fits_header(self, input_header):
        
        """
        Set header keys based on main dictionary
        For None values, replace with empty string.
        Params:
            input_header : the CCD will create its own FITS header,
                this function will update/add values.
        """
        
        output_header = input_header.copy()
        
        if self.main_dict is None:
            self.create_main_params_dict()
        
        for key, value in self.main_dict.items():
            
            if type(value)==tuple:
                val = value[0]
                comment = value[1]
                if val is None:
                    val='unavail '
                
                output_header.set(key,val,comment)
            else:
                if value is None:
                    value = 'unavail '
                output_header.set(key, value)
            
        self.output_header = output_header
        
        

#FITSHead()   
        
        
        