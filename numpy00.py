import numpy as np
import pandas as pd

#######################
## Numpy bits ##
# generate random sample
np.random.seed(8675309)
nda = np.random.beta(10,10,100)
nda
ndb = np.random.beta(10,10,100)

#### Random number matrix
darray = np.random.randint(0, 100, [1000, 50])  # creates ndarray
df = pd.DataFrame(darray)

pd.options.display.max_rows
# default is 60
pd.options.display.max_columns = 8

