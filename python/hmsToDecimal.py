import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

import astropy.coordinates as coord
import astropy.units as u

filename = '20170515_spreadsheet.csv'

df = pd.read_csv(filename, usecols=['StarName','RA','DEC'])

df.loc[:,'radeg'] = coord.Angle(df.loc[:,'RA'], unit=u.hour).degree
df.loc[:,'decdeg'] = coord.Angle(df.loc[:,'DEC'], unit=u.degree).degree

df.to_csv('newfile.csv',
          sep=',',
          columns=['StarName','radeg','decdeg'],
          index=False)

# To get reddening, make sure to go in afterward and change column names to:
# object,ra,dec
# Delete any blank lines, *, etc

