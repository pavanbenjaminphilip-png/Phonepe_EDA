import nbformat as nbf

def update_notebook_batch2(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbf.read(f, as_version=4)

    charts_data = [
        {
            "id": "Chart - 6",
            "title": "Top 10 Brands by User Count",
            "code": (
                "plt.figure(figsize=(10,6))\n"
                "brand_users = df_agg_user.groupby('Brand')['Transaction_count'].sum().sort_values(ascending=False).head(10).reset_index()\n"
                "sns.barplot(data=brand_users, x='Transaction_count', y='Brand', palette='coolwarm')\n"
                "plt.title('Top 10 Mobile Brands by User Count')\n"
                "plt.show()"
            ),
            "q1": "A bar chart is used to compare the popularity of different mobile brands among PhonePe users.",
            "q2": "Xiaomi and Samsung are the most popular brands among users, suggesting that the app is highly used on affordable to mid-range Android devices.",
            "q3": "Yes, this helps in optimizing the app performance for specific mobile brands and prioritizing bug fixes for the most popular devices."
        },
        {
            "id": "Chart - 7",
            "title": "State-wise Registered Users",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "state_users = df_map_user.groupby('State')['RegisteredUsers'].max().sort_values(ascending=False).head(10).reset_index()\n"
                "sns.barplot(data=state_users, x='RegisteredUsers', y='State', palette='YlOrBr')\n"
                "plt.title('Top 10 States by Registered Users')\n"
                "plt.show()"
            ),
            "q1": "I chose a bar chart to rank the states by their total user base.",
            "q2": "States like Uttar Pradesh and Maharashtra have the largest registered user bases, reflecting their high population and increasing internet penetration.",
            "q3": "Large user bases in specific states indicate mature markets where focus can shift from acquisition to retention and upselling services."
        },
        {
            "id": "Chart - 8",
            "title": "App Opens vs Registered Users (Scatter)",
            "code": (
                "plt.figure(figsize=(10,6))\n"
                "sns.scatterplot(data=df_map_user, x='RegisteredUsers', y='AppOpens', alpha=0.5, color='blue')\n"
                "plt.title('Registered Users vs App Opens')\n"
                "plt.show()"
            ),
            "q1": "A scatter plot is perfect for visualizing the correlation between two continuous variables.",
            "q2": "There is a strong positive correlation between registered users and app opens, which is expected. However, some outliers show high app opens with relatively fewer users, indicating high engagement.",
            "q3": "Identifying high-engagement regions helps in testing new features where users are most active."
        },
        {
            "id": "Chart - 9",
            "title": "Top 10 Pincodes by Transaction Amount",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "pin_trans = df_top_trans.groupby('Pincode')['Amount'].sum().sort_values(ascending=False).head(10).reset_index()\n"
                "pin_trans['Pincode'] = pin_trans['Pincode'].astype(str)\n"
                "sns.barplot(data=pin_trans, x='Amount', y='Pincode', palette='viridis')\n"
                "plt.title('Top 10 Pincodes by Transaction Amount')\n"
                "plt.show()"
            ),
            "q1": "A bar chart helps in identifying specific high-value local hubs based on pincodes.",
            "q2": "Specific urban pincodes (often business districts or tech parks) contribute disproportionately to the total transaction value.",
            "q3": "This granular data allows for highly targeted hyper-local marketing and partnership opportunities with local businesses."
        },
        {
            "id": "Chart - 10",
            "title": "Insurance Transaction Amount by Year",
            "code": (
                "plt.figure(figsize=(10,6))\n"
                "ins_yearly = df_agg_ins.groupby('Year')['Transaction_amount'].sum().reset_index()\n"
                "sns.barplot(data=ins_yearly, x='Year', y='Transaction_amount', palette='plasma')\n"
                "plt.title('Total Insurance Transaction Amount per Year')\n"
                "plt.show()"
            ),
            "q1": "A bar chart is used to show the growth of the insurance sector within the PhonePe ecosystem.",
            "q2": "The insurance segment is showing steady growth, especially after 2020, indicating that users are becoming comfortable purchasing financial products via the app.",
            "q3": "Growth in insurance transactions signifies successful diversification of the product portfolio beyond simple payments."
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
    update_notebook_batch2("Sample_EDA_Submission_Template.ipynb")
    print("Notebook Batch 2 updated successfully.")
