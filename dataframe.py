import pandas as pd
import numpy as np

# Define the column names as strings
column_names = ['Column1',
                'Column2',
                'Column3',
                'Column4',
                'Column5',
                'Column6',
                'Column7',
                'Column8',
                'Column9',
                'Column10']

# Create a dictionary with random numbers as values
data = {column: np.random.randint(1, 100, 50) for column in column_names}

# Create the DataFrame
df = pd.DataFrame(data)
