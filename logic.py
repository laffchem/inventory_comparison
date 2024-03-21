import pandas as pd
import csv
import glob
import os

pd.options.mode.copy_on_write = True  # This creates a copy in memory instead of providing a view. (Will be standard behavior in pandas 3.0)


# Note - of = older file | nf = newer file
# Comparing 2 Files -- Note you have to provide an output filename... Not the .csv part though
def compare_inventory_files(outputFileName):
    older_file = input(
        "Input the name of the older inventory file. Copy and paste it...\n"
    )
    newer_file = input(
        "Input the name of the newer inventory file. Copy and paste it...\n"
    )

    of_df = pd.read_csv(older_file)
    nf_df = pd.read_csv(newer_file)

    merged_df = pd.merge(of_df, nf_df, on="UPC", suffixes=("_older", "_newer"))

    merged_df["QtyChange"] = (
        merged_df["QtyAvailable_newer"] - merged_df["QtyAvailable_older"]
    )

    filtered_df = merged_df[merged_df["QtyAvailable_newer"] >= 3]
    filtered_df["QtyChange"] = (
        filtered_df["QtyAvailable_newer"] - filtered_df["QtyAvailable_older"]
    )

    filtered_df["PercentageChange"] = (
        (
            (
                (filtered_df["QtyAvailable_newer"] - filtered_df["QtyAvailable_older"])
                / filtered_df["QtyAvailable_older"]
            )
            * 100
        )
        .round(2)
        .map("{:.2f}%".format)
    )

    filtered_df.loc[:, "ChangeStatus"] = "No Change"
    filtered_df.loc[filtered_df["QtyChange"] > 0, "ChangeStatus"] = "Quantity Increase"
    filtered_df.loc[filtered_df["QtyChange"] < 0, "ChangeStatus"] = "Quantity Decrease"

    final_df = filtered_df[
        [
            "UPC",
            "QtyAvailable_older",
            "QtyAvailable_newer",
            "ChangeStatus",
            "PercentageChange",
        ]
    ]

    final_df.to_csv(f"./inventory_comparisons/{outputFileName}.csv")
    print("Output file written to inventory_comparisons directory...")


# Comparing 2 Files for missing upcs -- Note you have to provide an output filename... Not the .csv part though
def find_missing_upcs_from_two_files(outputFileName):
    older_file = input(
        "Input the name of the older inventory file. Copy and paste it...\n"
    )
    newer_file = input(
        "Input the name of the newer inventory file. Copy and paste it..."
    )

    of_df = pd.read_csv(older_file)
    nf_df = pd.read_csv(newer_file)

    upcs_older_file = set(of_df["UPC"])
    upcs_newer_file = set(nf_df["UPC"])

    missing_from_older_file = upcs_newer_file - upcs_older_file
    missing_from_newer_file = upcs_older_file - upcs_newer_file

    missing_upcs_df = pd.DataFrame(columns=["UPC", "MissingFrom"])
    missing_upcs_df["UPC"] = list(
        missing_from_older_file.union(missing_from_newer_file)
    )
    missing_upcs_df["MissingFrom"] = missing_upcs_df["UPC"].apply(
        lambda upc: (
            older_file
            if upc in missing_from_older_file
            else (newer_file if upc in missing_from_newer_file else "Both")
        )
    )

    missing_upcs_df.to_csv(f"./upc_comparisons/{outputFileName}.csv")
    print("Output file written to upc_comparisons directory...")


def count_rows_of_inventory_file():
    file = input("Input the name of the file\n")
    df = pd.read_csv(file)
    filtered_df = df[df["QtyAvailable"] >= 3]  # Filtering the DataFrame correctly
    length = len(filtered_df)  # Getting the length of the filtered DataFrame
    print("Length of inventory file with QtyAvailable >= 3: ", length)


def get_product_upc(item):
    start_str = "LIN**UP*"
    end_str = "*VN"
    start = item.index(start_str) + len(start_str)
    end = item.index(end_str, start + 1)
    return item[start:end]


def parse_edi_files_for_upcs(edi_file_name):
    products = ["UPC"]
    with open(edi_file_name, "r") as file:
        lines = file.readlines()
        product_list = [item for item in lines if "LIN**UP*" in item]
        for item in product_list:
            result = get_product_upc(item)
            products.append(result)
    csv_data = []
    csv_file_name = edi_file_name.replace(".edi", ".csv")
    for item in products:
        csv_data.append([item])
    with open(f"./edi_to_csv/{csv_file_name}", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(csv_data[0])
        for row in csv_data[1:]:
            writer.writerow(row)


def parse_directory_of_edi_files_for_upcs(folder_name):
    products = ["UPC"]
    folder_path = os.path.join(".", folder_name)
    os.chdir(folder_path)
    files = glob.glob("*.edi")
    print(files)
    for edi_file in files:
        with open(edi_file, "r") as file:
            lines = file.readlines()
            lines
            product_list = [item for item in lines if "LIN**UP*" in item]
            for item in product_list:
                result = get_product_upc(item)
                result
                products.append(result)
        csv_data = []
        csv_file_name = edi_file.replace(".edi", ".csv")
        for item in products:
            csv_data.append([item])
        with open(
            os.path.join("..", "batch_edi_to_csv", csv_file_name), "w", newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow(csv_data[0])
            for row in csv_data[1:]:
                writer.writerow(row)


def choose_option():
    options = """Choose from the following options. Ensure you only enter the number and press enter.
    1. Compare inventory files to see percent increase or decrease in specific UPCs.
    2. Compare inventory files to see UPCs that are missing from either file.
    3. Parse through edi files to create a csv of contained UPCs for comparison in one of other methods.
    4. Give a length value for the active products in the inventory file in question.
    5. Parse through a directory of edi files to create csvs of contained UPCs for comparison in one of the other methods.\n"""
    option = int(input(options))
    return option


def run_program(choice):
    match choice:
        case 1:
            return compare_inventory_files("output")

        case 2:
            return find_missing_upcs_from_two_files("output")
        case 3:
            return parse_edi_files_for_upcs(
                input("Input the edi file name.\n") + ".edi"
            )
        case 4:
            return count_rows_of_inventory_file()
        case 5:
            return parse_directory_of_edi_files_for_upcs(
                input("Input the name of your folder.\n")
            )
