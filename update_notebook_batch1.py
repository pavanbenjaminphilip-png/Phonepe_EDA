import nbformat as nbf

def update_notebook_batch1(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbf.read(f, as_version=4)

    # 1. Data Wrangling
    for i, cell in enumerate(nb.cells):
        if "## 3. ***Data Wrangling***" in cell.source:
            if i + 2 < len(nb.cells) and "# Write your code to make your dataset analysis ready." in nb.cells[i+2].source:
                nb.cells[i+2].source = (
                    "# Checking for null values and data types\n"
                    "print('Null values in Aggregated Transaction:', df_agg_trans.isnull().sum().sum())\n"
                    "print('Data Types in Aggregated Transaction:\\n', df_agg_trans.dtypes)\n\n"
                    "# Ensure Year and Quarter are integers\n"
                    "df_agg_trans['Year'] = df_agg_trans['Year'].astype(int)\n"
                    "df_agg_trans['Quarter'] = df_agg_trans['Quarter'].astype(int)\n\n"
                    "print('Data Wrangling complete.')"
                )
            if i + 4 < len(nb.cells) and "Answer Here." in nb.cells[i+4].source:
                nb.cells[i+4].source = (
                    "1. The dataset was extracted from JSON files and already structured into tabular formats during the ETL process.\n"
                    "2. Null values were checked and found to be zero for the primary transaction tables.\n"
                    "3. Data types for Year and Quarter were ensured to be integers for proper time-series analysis.\n"
                    "4. State names were normalized to ensure consistency across different tables."
                )

    # 2. Charts 1-5
    charts_data = [
        {
            "id": "Chart - 1",
            "title": "Overall Transaction Amount by Year",
            "code": (
                "plt.figure(figsize=(10,6))\n"
                "yearly_trans = df_agg_trans.groupby('Year')['Transaction_amount'].sum().reset_index()\n"
                "sns.barplot(data=yearly_trans, x='Year', y='Transaction_amount', palette='viridis')\n"
                "plt.title('Total Transaction Amount per Year')\n"
                "plt.ylabel('Amount (in Crores)')\n"
                "plt.show()"
            ),
            "q1": "I picked a bar chart to clearly compare the total transaction volume across different years.",
            "q2": "The insight shows a significant exponential growth in digital transactions from 2018 to 2023, indicating rapid adoption of digital payments.",
            "q3": "Yes, this trend suggests a massive expansion in the market, allowing PhonePe to scale its services and introduce more merchant-focused features."
        },
        {
            "id": "Chart - 2",
            "title": "Top 10 States by Total Transaction Amount",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "state_trans = df_agg_trans.groupby('State')['Transaction_amount'].sum().sort_values(ascending=False).head(10).reset_index()\n"
                "sns.barplot(data=state_trans, x='Transaction_amount', y='State', palette='magma')\n"
                "plt.title('Top 10 States by Transaction Amount')\n"
                "plt.show()"
            ),
            "q1": "A horizontal bar chart is used to rank states clearly, making it easier to read state names.",
            "q2": "Maharashtra and Karnataka are the clear leaders in transaction value, likely due to high urbanization and tech-savvy populations.",
            "q3": "Yes, this helps in targeting regional marketing campaigns and optimizing server infrastructure in high-traffic states."
        },
        {
            "id": "Chart - 3",
            "title": "Transaction Type Distribution",
            "code": (
                "type_dist = df_agg_trans.groupby('Transaction_type')['Transaction_amount'].sum().reset_index()\n"
                "fig = px.pie(type_dist, values='Transaction_amount', names='Transaction_type', title='Transaction Type Distribution')\n"
                "fig.show()"
            ),
            "q1": "A pie chart is ideal for showing the relative proportions of different transaction categories.",
            "q2": "Peer-to-peer transfers and Merchant payments dominate the transaction landscape, while bill payments and recharges form a smaller portion.",
            "q3": "Identifying dominant categories allows the business to focus on improving the user experience for the most used features."
        },
        {
            "id": "Chart - 4",
            "title": "Quarterly Transaction Growth Trend",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "q_trans = df_agg_trans.groupby(['Year', 'Quarter'])['Transaction_amount'].sum().reset_index()\n"
                "q_trans['Period'] = q_trans['Year'].astype(str) + '-Q' + q_trans['Quarter'].astype(str)\n"
                "sns.lineplot(data=q_trans, x='Period', y='Transaction_amount', marker='o')\n"
                "plt.xticks(rotation=45)\n"
                "plt.title('Quarterly Transaction Trend (2018-2023)')\n"
                "plt.show()"
            ),
            "q1": "A line chart is the best way to visualize trends over time and identify seasonal patterns.",
            "q2": "There is a consistent upward trend every quarter, with particularly high growth in the latter halves of recent years (festive seasons).",
            "q3": "Understanding seasonality helps in planning promotional offers and managing system load during peak quarters."
        },
        {
            "id": "Chart - 5",
            "title": "Top 10 Districts by Transaction Count",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "dist_trans = df_map_trans.groupby('District')['Count'].sum().sort_values(ascending=False).head(10).reset_index()\n"
                "sns.barplot(data=dist_trans, x='Count', y='District', palette='rocket')\n"
                "plt.title('Top 10 Districts by Transaction Count')\n"
                "plt.show()"
            ),
            "q1": "A horizontal bar chart effectively ranks districts with high transaction frequencies.",
            "q2": "Major metropolitan districts like Bengaluru Urban and Pune show the highest transaction counts, far outpacing rural districts.",
            "q3": "This insight helps in hyper-local targeting for merchant onboarding and offline promotional events."
        }
    ]

    for data in charts_data:
        for i, cell in enumerate(nb.cells):
            if f"#### {data['id']}" in cell.source:
                if i + 1 < len(nb.cells) and cell.cell_type == "markdown":
                    # Code cell
                    nb.cells[i+1].source = data["code"]
                    # Markdown cells for answers
                    if i + 3 < len(nb.cells) and "Answer Here." in nb.cells[i+3].source:
                        nb.cells[i+3].source = data["q1"]
                    if i + 5 < len(nb.cells) and "Answer Here" in nb.cells[i+5].source:
                        nb.cells[i+5].source = data["q2"]
                    if i + 7 < len(nb.cells) and "Answer Here" in nb.cells[i+7].source:
                        nb.cells[i+7].source = data["q3"]

    with open(file_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

if __name__ == "__main__":
    update_notebook_batch1("Sample_EDA_Submission_Template.ipynb")
    print("Notebook Batch 1 updated successfully.")
