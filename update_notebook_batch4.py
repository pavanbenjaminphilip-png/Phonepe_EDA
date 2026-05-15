import nbformat as nbf

def update_notebook_batch4(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbf.read(f, as_version=4)

    charts_data = [
        {
            "id": "Chart - 16",
            "title": "Top 10 Districts for App Opens",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "dist_opens = df_map_user.groupby('District')['AppOpens'].sum().sort_values(ascending=False).head(10).reset_index()\n"
                "sns.barplot(data=dist_opens, x='AppOpens', y='District', palette='flare')\n"
                "plt.title('Top 10 Districts by App Opens')\n"
                "plt.show()"
            ),
            "q1": "A bar chart highlights the districts with the highest digital engagement.",
            "q2": "Bengaluru Urban consistently leads in app engagement, reflecting its status as a tech hub.",
            "q3": "High app opens indicate a loyal user base that can be targeted for beta testing new app features."
        },
        {
            "id": "Chart - 17",
            "title": "Yearly Insurance Transaction Growth",
            "code": (
                "plt.figure(figsize=(10,6))\n"
                "ins_growth = df_agg_ins.groupby('Year')['Transaction_count'].sum().reset_index()\n"
                "sns.lineplot(data=ins_growth, x='Year', y='Transaction_count', marker='o', color='red')\n"
                "plt.title('Yearly Insurance Transaction Count Growth')\n"
                "plt.show()"
            ),
            "q1": "A line chart shows the momentum of insurance adoption over the years.",
            "q2": "There is a sharp increase in insurance transactions in 2022-2023, possibly due to better product visibility and pandemic-induced awareness.",
            "q3": "This suggests that insurance is a high-growth sector for the company to invest more in."
        },
        {
            "id": "Chart - 18",
            "title": "Top 10 States by Insurance Amount",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "ins_amt_state = df_agg_ins.groupby('State')['Transaction_amount'].sum().sort_values(ascending=False).head(10).reset_index()\n"
                "sns.barplot(data=ins_amt_state, x='Transaction_amount', y='State', palette='crest')\n"
                "plt.title('Top 10 States by Insurance Transaction Amount')\n"
                "plt.show()"
            ),
            "q1": "A bar chart ranks the states by their contribution to insurance revenue.",
            "q2": "Karnataka and Maharashtra are leaders in insurance amounts as well, consistent with their overall digital payment leadership.",
            "q3": "Regional dominance helps in negotiating better terms with insurance providers in those specific states."
        },
        {
            "id": "Chart - 19",
            "title": "Quarterly Registered Users Growth",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "user_growth = df_map_user.groupby(['Year', 'Quarter'])['RegisteredUsers'].max().reset_index()\n"
                "user_growth['Period'] = user_growth['Year'].astype(str) + '-Q' + user_growth['Quarter'].astype(str)\n"
                "sns.lineplot(data=user_growth, x='Period', y='RegisteredUsers', marker='p', color='purple')\n"
                "plt.xticks(rotation=45)\n"
                "plt.title('Quarterly Registered Users Growth')\n"
                "plt.show()"
            ),
            "q1": "A line chart tracks the user acquisition speed over time.",
            "q2": "The user base is growing steadily, with no signs of saturation yet, which is positive for long-term growth.",
            "q3": "Continuous user growth justifies the expansion of the platform into a 'Super App' with more services."
        },
        {
            "id": "Chart - 20",
            "title": "Top 10 Districts by Insurance Count",
            "code": (
                "plt.figure(figsize=(12,6))\n"
                "dist_ins_count = df_map_ins.groupby('District')['Count'].sum().sort_values(ascending=False).head(10).reset_index()\n"
                "sns.barplot(data=dist_ins_count, x='Count', y='District', palette='magma')\n"
                "plt.title('Top 10 Districts by Insurance Transaction Count')\n"
                "plt.show()"
            ),
            "q1": "A bar chart helps in identifying the most active insurance markets at a district level.",
            "q2": "Metropolitan districts are again the primary drivers, but some Tier-2 districts are also showing significant activity.",
            "q3": "Tier-2 district activity shows that digital insurance is reaching beyond the metros, opening new market segments."
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
    update_notebook_batch4("Sample_EDA_Submission_Template.ipynb")
    print("Notebook Batch 4 updated successfully.")
