import nbformat as nbf

def update_notebook(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbf.read(f, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            if "# **Project Name**" in cell.source:
                cell.source = "# **Project Name**    - PhonePe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly"
            elif "Write the summary here within 500-600 words." in cell.source:
                cell.source = (
                    "The PhonePe Pulse Data Visualization and Exploration project aims to provide a comprehensive analysis of digital payment trends in India. "
                    "By leveraging the vast dataset provided by PhonePe Pulse, this project extracts, transforms, and loads (ETL) data into a structured MySQL database. "
                    "The core of the project involves an interactive Streamlit dashboard that allows users to explore transaction and user demographics across various states, districts, and time periods (years and quarters). "
                    "Through insightful visualizations like geo-maps, bar charts, and pie charts, the project uncovers key patterns in transaction volumes, values, and user engagement, offering valuable insights for business strategy and market understanding."
                )
            elif "**Write Problem Statement Here.**" in cell.source:
                cell.source = (
                    "The objective of this project is to build a robust data pipeline and a user-friendly dashboard to visualize PhonePe's transaction data. "
                    "The problem involves handling hierarchical JSON files, transforming them into a relational database, and creating a dynamic interface where stakeholders can easily identify top-performing regions, transaction growth trends, and user behavior patterns across India. "
                    "The final solution must provide actionable insights through 20+ interactive visualizations and a functional Streamlit application."
                )
            elif "#### **Define Your Business Objective?**" in cell.source:
                # The next cell usually contains "Answer Here."
                pass
            elif "Answer Here." in cell.source:
                # Need to be careful which "Answer Here" we are replacing.
                # Let's check the context.
                pass

    # Specific replacements by index if needed, but search is safer for structure.
    # Let's re-read the cells to find the exact "Answer Here." for Business Objective.
    for i, cell in enumerate(nb.cells):
        if "#### **Define Your Business Objective?**" in cell.source:
            if i + 1 < len(nb.cells) and "Answer Here." in nb.cells[i+1].source:
                nb.cells[i+1].source = (
                    "The primary business objective is to empower stakeholders with data-driven insights to optimize marketing strategies, identify high-growth regions, and understand user preferences in the digital payment ecosystem. Specifically, the project aims to:\n\n"
                    "1. Identify top 10 states and districts with the highest transaction volumes and values.\n"
                    "2. Monitor the growth of different transaction categories (e.g., Peer-to-peer, Merchant payments).\n"
                    "3. Analyze user engagement based on mobile brand preferences and app usage metrics.\n"
                    "4. Provide a geographical view of payment distribution to aid in regional resource allocation."
                )
        
        if "### Import Libraries" in cell.source:
             if i + 1 < len(nb.cells) and cell.cell_type == "markdown":
                # Assuming the next cell is the code cell for libraries
                nb.cells[i+1].source = (
                    "import pandas as pd\n"
                    "import mysql.connector\n"
                    "import matplotlib.pyplot as plt\n"
                    "import seaborn as sns\n"
                    "import plotly.express as px\n"
                    "from sqlalchemy import create_engine\n"
                    "import warnings\n"
                    "warnings.filterwarnings('ignore')"
                )

        if "### Dataset Loading" in cell.source:
            if i + 1 < len(nb.cells):
                nb.cells[i+1].source = (
                    "# Connection to MySQL database\n"
                    "engine = create_engine('mysql+mysqlconnector://root:pavan@localhost/phonepe_pulse')\n\n"
                    "# Loading tables into DataFrames\n"
                    "df_agg_trans = pd.read_sql('aggregated_transaction', engine)\n"
                    "df_agg_user = pd.read_sql('aggregated_user', engine)\n"
                    "df_agg_ins = pd.read_sql('aggregated_insurance', engine)\n"
                    "df_map_trans = pd.read_sql('map_transaction', engine)\n"
                    "df_map_user = pd.read_sql('map_user', engine)\n"
                    "df_map_ins = pd.read_sql('map_insurance', engine)\n"
                    "df_top_trans = pd.read_sql('top_transaction', engine)\n"
                    "df_top_user = pd.read_sql('top_user', engine)\n"
                    "df_top_ins = pd.read_sql('top_insurance', engine)\n\n"
                    "print('Data loaded successfully from MySQL.')"
                )

    with open(file_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

if __name__ == "__main__":
    update_notebook("Sample_EDA_Submission_Template.ipynb")
    print("Notebook updated successfully.")
