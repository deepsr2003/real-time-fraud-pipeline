import pandas as pd
import numpy as np

# We create 100 rows of random data that looks like the real data
# The model expects 30 columns (Time, V1-V28, Amount)
columns = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
data = np.random.randn(100, 30)
df = pd.DataFrame(data, columns=columns)

# Save it
df.to_csv('creditcard.csv', index=False)
print("Created a fake creditcard.csv for testing!")