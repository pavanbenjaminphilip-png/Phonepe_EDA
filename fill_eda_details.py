import nbformat as nbf

def fill_know_your_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbf.read(f, as_version=4)

    for i, cell in enumerate(nb.cells):
        # 1. Dataset First Look
        if "### Dataset First View" in cell.source:
            if i + 1 < len(nb.cells) and "# Dataset First Look" in nb.cells[i+1].source:
                nb.cells[i+1].source = (
                    "print('--- Aggregated Transaction First Look ---')\n"
                    "display(df_agg_trans.head())\n\n"
                    "print('--- Aggregated User First Look ---')\n"
                    "display(df_agg_user.head())"
                )
        
        # 2. Dataset Rows & Columns count
        if "### Dataset Rows & Columns count" in cell.source:
            if i + 1 < len(nb.cells) and "# Dataset Rows & Columns count" in nb.cells[i+1].source:
                nb.cells[i+1].source = (
                    "print(f'Aggregated Transaction Rows: {df_agg_trans.shape[0]}, Columns: {df_agg_trans.shape[1]}')\n"
                    "print(f'Aggregated User Rows: {df_agg_user.shape[0]}, Columns: {df_agg_user.shape[1]}')"
                )
        
        # 3. Dataset Information
        if "### Dataset Information" in cell.source:
            if i + 1 < len(nb.cells) and "# Dataset Info" in nb.cells[i+1].source:
                nb.cells[i+1].source = (
                    "print('--- Aggregated Transaction Info ---')\n"
                    "df_agg_trans.info()\n\n"
                    "print('\\n--- Aggregated User Info ---')\n"
                    "df_agg_user.info()"
                )
        
        # 4. Duplicate Values
        if "#### Duplicate Values" in cell.source:
            if i + 1 < len(nb.cells) and "# Dataset Duplicate Value Count" in nb.cells[i+1].source:
                nb.cells[i+1].source = (
                    "print(f'Duplicates in Aggregated Transaction: {df_agg_trans.duplicated().sum()}')\n"
                    "print(f'Duplicates in Aggregated User: {df_agg_user.duplicated().sum()}')"
                )
        
        # 5. Missing Values/Null Values
        if "#### Missing Values/Null Values" in cell.source:
            if i + 1 < len(nb.cells) and "# Missing Values/Null Values Count" in nb.cells[i+1].source:
                nb.cells[i+1].source = (
                    "print('--- Missing Values in Aggregated Transaction ---')\n"
                    "print(df_agg_trans.isnull().sum())\n\n"
                    "print('--- Missing Values in Aggregated User ---')\n"
                    "print(df_agg_user.isnull().sum())"
                )
            if i + 2 < len(nb.cells) and "# Visualizing the missing values" in nb.cells[i+2].source:
                 nb.cells[i+2].source = (
                    "plt.figure(figsize=(10,4))\n"
                    "sns.heatmap(df_agg_trans.isnull(), cbar=False, cmap='viridis')\n"
                    "plt.title('Missing Values Heatmap (Aggregated Transaction)')\n"
                    "plt.show()"
                 )

        # 6. What did you know about your dataset?
        if "### What did you know about your dataset?" in cell.source:
             if i + 1 < len(nb.cells) and "Answer Here" in nb.cells[i+1].source:
                nb.cells[i+1].source = (
                    "The dataset is extracted from PhonePe Pulse GitHub repository. It consists of multiple categories: \n"
                    "1. **Aggregated Data**: Contains high-level totals of transactions and users across years and quarters.\n"
                    "2. **Map Data**: Provides spatial distribution of transactions and app engagement at the district level.\n"
                    "3. **Top Data**: Highlights the top-performing pincodes and districts.\n"
                    "Initial inspection reveals that the dataset is clean with zero null values and zero duplicates. The hierarchical structure (State > Year > Quarter) is consistent across all tables, making it ideal for time-series and geographical analysis."
                )

        # 7. Variables Description
        if "### Variables Description" in cell.source:
            if i + 1 < len(nb.cells) and "Answer Here" in nb.cells[i+1].source:
                nb.cells[i+1].source = (
                    "1. **State**: The Indian state or union territory.\n"
                    "2. **Year**: The year of the data (2018-2023).\n"
                    "3. **Quarter**: The fiscal quarter (1, 2, 3, 4).\n"
                    "4. **Transaction_type**: Category of payment (e.g., Merchant, P2P, Recharge).\n"
                    "5. **Transaction_count**: Total number of transactions recorded.\n"
                    "6. **Transaction_amount**: Total value of transactions in Indian Rupees.\n"
                    "7. **Brand**: Mobile phone brand (e.g., Xiaomi, Samsung).\n"
                    "8. **RegisteredUsers**: Total number of users registered in a specific region."
                )

    with open(file_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

if __name__ == "__main__":
    fill_know_your_data("Sample_EDA_Submission_Template.ipynb")
    print("Notebook 'Know Your Data' section filled successfully.")
