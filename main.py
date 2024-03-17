import pandas as pd

second_newest_file = input("Input the name of the older file. Copy and paste it...\n")
most_recent_file = input(
    "Input the name of the most recent file. Copy and paste it...\n"
)

snf_df = pd.read_csv(second_newest_file)
mrf_df = pd.read_csv(most_recent_file)

snf_df.sort_values(by="UPC", inplace=True)
mrf_df.sort_values(by="UPC", inplace=True)

merged_df = pd.merge(snf_df, mrf_df, on="UPC", suffixes=("_snf", "_mrf"))

merged_df["QtyChange"] = merged_df["QtyAvailable_mrf"] - merged_df["QtyAvailable_snf"]

merged_df["ChangeStatus"] = "No Change"
merged_df.loc[merged_df["QtyChange"] > 0, "ChangeStatus"] = "Quantity Increase"
merged_df.loc[merged_df["QtyChange"] < 0, "ChangeStatus"] = "Quantity Decrease"

final_df = merged_df[["UPC", "QtyAvailable_snf", "QtyAvailable_mrf", "ChangeStatus"]]
final_df.to_csv("./inventory_comparisons/comparison.csv")
