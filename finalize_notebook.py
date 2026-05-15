import nbformat as nbf

def finalize_notebook(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbf.read(f, as_version=4)

    for i, cell in enumerate(nb.cells):
        if "### Summary of Key Findings" in cell.source or "# **Conclusion**" in cell.source:
            # Look for the next Answer cell
            for j in range(i+1, min(i+5, len(nb.cells))):
                if "Answer Here" in nb.cells[j].source:
                    nb.cells[j].source = (
                        "1. **Explosive Growth**: Digital transactions have seen exponential growth from 2018 to 2023, with increasing adoption in every quarter.\n"
                        "2. **Regional Leadership**: Maharashtra, Karnataka, and Telangana are the top states driving both transaction volume and value.\n"
                        "3. **User Behavior**: Peer-to-peer transfers and Merchant payments are the primary drivers of transaction volume, while insurance is an emerging high-growth sector.\n"
                        "4. **Brand Dominance**: Xiaomi and Samsung are the most widely used mobile brands among PhonePe users, indicating high reach in the mid-range smartphone segment.\n"
                        "5. **High Engagement**: There is a strong correlation between registered users and app opens, with major tech hubs showing the highest engagement levels."
                    )
                    break
        
        if "### Recommendations" in cell.source or "## **Actionable Insights**" in cell.source:
            for j in range(i+1, min(i+5, len(nb.cells))):
                if "Answer Here" in nb.cells[j].source:
                    nb.cells[j].source = (
                        "1. **Hyper-local Marketing**: Focus marketing efforts on the top 10 pincodes and districts identified to maximize ROI.\n"
                        "2. **Diversify Financial Products**: Given the growth in insurance, introduce more customized insurance and investment products for Tier-2 cities.\n"
                        "3. **Brand Partnerships**: Collaborate with top mobile brands like Xiaomi and Samsung for pre-installed app deals or exclusive cashback offers.\n"
                        "4. **Merchant Onboarding**: Scale up merchant acquisition in states with high P2P transactions to convert those users into merchant payment users.\n"
                        "5. **Seasonal Campaigns**: Plan major promotional campaigns during Q3 and Q4 to capitalize on the identified festive season growth trends."
                    )
                    break

    with open(file_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

if __name__ == "__main__":
    finalize_notebook("Sample_EDA_Submission_Template.ipynb")
    print("Notebook finalized successfully.")
