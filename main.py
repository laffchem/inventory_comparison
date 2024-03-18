import pandas as pd

pd.options.mode.copy_on_write = True  # This creates a copy in memory instead of providing a view. (Will be standard behavior in pandas 3.0)

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

filtered_df = merged_df[merged_df["QtyAvailable_mrf"] > 3]

filtered_df["QtyChange"] = (
    filtered_df["QtyAvailable_mrf"] - filtered_df["QtyAvailable_snf"]
)

filtered_df.loc[:, "ChangeStatus"] = "No Change"
filtered_df.loc[filtered_df["QtyChange"] > 0, "ChangeStatus"] = "Quantity Increase"
filtered_df.loc[filtered_df["QtyChange"] < 0, "ChangeStatus"] = "Quantity Decrease"

final_df = filtered_df[["UPC", "QtyAvailable_snf", "QtyAvailable_mrf", "ChangeStatus"]]

final_df.to_csv("./comparisons/comparison.csv")
