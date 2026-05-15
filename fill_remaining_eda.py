import nbformat as nbf

def fill_remaining_eda(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbf.read(f, as_version=4)

    for i, cell in enumerate(nb.cells):
        # 1. Dataset Columns
        if "# Dataset Columns" in cell.source:
            cell.source = (
                "print('Aggregated Transaction Columns:', df_agg_trans.columns.tolist())\n"
                "print('Aggregated User Columns:', df_agg_user.columns.tolist())"
            )
        
        # 2. Dataset Describe
        if "# Dataset Describe" in cell.source:
            cell.source = (
                "print('--- Aggregated Transaction Statistics ---')\n"
                "display(df_agg_trans.describe())\n\n"
                "print('--- Aggregated User Statistics ---')\n"
                "display(df_agg_user.describe())"
            )
        
        # 3. Check Unique Values
        if "# Check Unique Values for each variable." in cell.source:
            cell.source = (
                "for col in df_agg_trans.columns:\n"
                "    print(f'Unique values in {col}: {df_agg_trans[col].nunique()}')"
            )

    with open(file_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

if __name__ == "__main__":
    fill_remaining_eda("Sample_EDA_Submission_Template.ipynb")
    print("Remaining EDA sections filled successfully.")
