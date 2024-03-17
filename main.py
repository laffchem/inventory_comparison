import pandas as pd

second_oldest_file = input("Input the name of the older file. Copy and paste it...\n")
most_recent_file = input(
    "Input the name of the most recent file. Copy and paste it...\n"
)

sof_df = pd.read_csv(second_oldest_file)
mrf_df = pd.read_csv(most_recent_file)

sof_df.sort_values(by="UPC", inplace=True)
mrf_df.sort_values(by="UPC", inplace=True)

merged_df = pd.merge(sof_df, mrf_df, on="UPC", suffixes=("_sof", "_mrf"))

merged_df["QtyChange"] = merged_df["QtyAvailable_mrf"] - merged_df["QtyAvailable_sof"]

merged_df["ChangeStatus"] = "No Change"
merged_df.loc[merged_df["QtyChange"] > 0, "ChangeStatus"] = "Quantity Increase"
merged_df.loc[merged_df["QtyChange"] < 0, "ChangeStatus"] = "Quantity Decrease"

final_df = merged_df[["UPC", "QtyAvailable_sof", "QtyAvailable_mrf", "ChangeStatus"]]
final_df.to_csv("./inventory_comparisons/comparison.csv")
