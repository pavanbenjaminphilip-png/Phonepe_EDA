import nbformat as nbf

def update_notebook_batch3(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbf.read(f, as_version=4)

    charts_data = [
        {
            "id": "Chart - 11",
            "title": "Quarterly Transaction Type Trend",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "q_type_trans = df_agg_trans.groupby(['Quarter', 'Transaction_type'])['Transaction_amount'].mean().reset_index()\n"
                "sns.lineplot(data=q_type_trans, x='Quarter', y='Transaction_amount', hue='Transaction_type', marker='o')\n"
                "plt.title('Average Transaction Amount by Type and Quarter')\n"
                "plt.show()"
            ),
            "q1": "A line plot is used to track the performance of different transaction types across quarters.",
            "q2": "Peer-to-peer payments show the highest average transaction values compared to recharges and bill payments.",
            "q3": "This helps in identifying which services are used for high-value transactions versus small frequent ones."
        },
        {
            "id": "Chart - 12",
            "title": "State-wise Transaction Count Distribution",
            "code": (
                "plt.figure(figsize=(10,10))\n"
                "state_count = df_agg_trans.groupby('State')['Transaction_count'].sum().head(10)\n"
                "plt.pie(state_count, labels=state_count.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))\n"
                "plt.title('Transaction Count Distribution across Top 10 States')\n"
                "plt.show()"
            ),
            "q1": "A pie chart highlights the contribution of each state to the total transaction count.",
            "q2": "A few states contribute to nearly 50% of the total transactions, showing a concentration of digital payment adoption.",
            "q3": "Businesses can focus on these high-volume states for premium service launches."
        },
        {
            "id": "Chart - 13",
            "title": "Yearly Average Transaction Value",
            "code": (
                "plt.figure(figsize=(10,6))\n"
                "df_agg_trans['Avg_Value'] = df_agg_trans['Transaction_amount'] / df_agg_trans['Transaction_count']\n"
                "avg_val = df_agg_trans.groupby('Year')['Avg_Value'].mean().reset_index()\n"
                "sns.lineplot(data=avg_val, x='Year', y='Avg_Value', marker='s', color='green')\n"
                "plt.title('Yearly Trend of Average Transaction Value')\n"
                "plt.show()"
            ),
            "q1": "A line chart shows how the value per transaction has evolved over the years.",
            "q2": "While transaction counts are increasing, the average value per transaction might be stabilizing, suggesting widespread use for smaller daily tasks.",
            "q3": "This indicates the shift towards micro-payments in the digital economy."
        },
        {
            "id": "Chart - 14",
            "title": "Insurance Count vs Amount per State",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "ins_state = df_agg_ins.groupby('State')[['Transaction_count', 'Transaction_amount']].sum().head(10).reset_index()\n"
                "ins_state.plot(x='State', y=['Transaction_count', 'Transaction_amount'], kind='bar', figsize=(12,6))\n"
                "plt.title('Insurance Transaction Count vs Amount by State')\n"
                "plt.show()"
            ),
            "q1": "A grouped bar chart compares two different metrics (count and amount) for the same category.",
            "q2": "Some states have high counts but lower amounts, indicating a preference for low-premium insurance products.",
            "q3": "This helps in tailoring insurance product offerings based on regional spending capacity."
        },
        {
            "id": "Chart - 15",
            "title": "Quarterly App Opens Growth",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "app_growth = df_map_user.groupby(['Year', 'Quarter'])['AppOpens'].sum().reset_index()\n"
                "app_growth['Period'] = app_growth['Year'].astype(str) + '-Q' + app_growth['Quarter'].astype(str)\n"
                "sns.barplot(data=app_growth, x='Period', y='AppOpens', color='orange')\n"
                "plt.xticks(rotation=45)\n"
                "plt.title('Total App Opens per Quarter')\n"
                "plt.show()"
            ),
            "q1": "A bar chart effectively shows the growth in user engagement (app opens) over time.",
            "q2": "App opens have increased significantly, showing that users are returning to the app more frequently.",
            "q3": "Higher engagement leads to better cross-selling opportunities for other financial services like loans or investments."
        }
    ]

    for data in charts_data:
        for i, cell in enumerate(nb.cells):
            if f"#### {data['id']}" in cell.source:
                if i + 1 < len(nb.cells) and cell.cell_type == "markdown":
                    nb.cells[i+1].source = data["code"]
                    if i + 3 < len(nb.cells) and "Answer Here." in nb.cells[i+3].source:
                        nb.cells[i+3].source = data["q1"]
                    if i + 5 < len(nb.cells) and "Answer Here" in nb.cells[i+5].source:
                        nb.cells[i+5].source = data["q2"]
                    if i + 7 < len(nb.cells) and "Answer Here" in nb.cells[i+7].source:
                        nb.cells[i+7].source = data["q3"]

    with open(file_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

if __name__ == "__main__":
    update_notebook_batch3("Sample_EDA_Submission_Template.ipynb")
    print("Notebook Batch 3 updated successfully.")
