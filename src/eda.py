import pandas as pd

# charger dataset
df = pd.read_csv("data/train.csv")

print("Shape du dataset :")
print(df.shape)

print("\nColonnes :")
print(df.columns)

print("\nExemple données :")
print(df.head())

print("\nDistribution toxicité :")
print(df["toxic"].value_counts())