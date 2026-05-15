import nbformat as nbf

def final_polish_notebook(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbf.read(f, as_version=4)

    for i, cell in enumerate(nb.cells):
        # 1. Solution to Business Objective
        if "What do you suggest the client to achieve Business Objective ?" in cell.source:
            if i + 2 < len(nb.cells) and "Answer Here." in nb.cells[i+2].source:
                nb.cells[i+2].source = (
                    "To achieve the business objectives, I suggest the following strategies:\n\n"
                    "1. **Localized Expansion**: Invest in onboarding merchants in Tier-2 and Tier-3 cities of high-growth states like Uttar Pradesh and Bihar, where the user base is large but transaction frequency is still growing.\n"
                    "2. **Feature Optimization**: Since Peer-to-Peer (P2P) transfers are dominant, introduce incentives for users to convert these into Merchant payments (e.g., cashback for paying local vendors).\n"
                    "3. **Insurance Cross-selling**: Leverage the steady growth in the insurance sector by offering personalized, low-ticket insurance products (like mobile or health micro-insurance) directly to users identified as frequent transactors in urban hubs.\n"
                    "4. **Brand-Specific Campaigns**: Partner with top mobile brands (Xiaomi, Samsung) for exclusive in-app offers to deepen engagement with the existing heavy user base.\n"
                    "5. **Seasonal Retention**: Plan major loyalty programs during Q3 and Q4 to capitalize on the identified festive season surge, ensuring users remain on the platform after the peak period."
                )
        
        # 2. Conclusion
        if "# **Conclusion**" in cell.source or "## **Conclusion**" in cell.source or ("Conclusion" in cell.source and cell.cell_type == "markdown"):
            if i + 1 < len(nb.cells) and "Write the conclusion here." in nb.cells[i+1].source:
                 nb.cells[i+1].source = (
                    "In conclusion, the PhonePe Pulse data analysis reveals a robust and rapidly maturing digital payment ecosystem in India. The exponential growth in transaction volume and value from 2018 to 2023 underscores a structural shift in consumer behavior towards digital-first financial interactions. While metropolitan hubs like Bengaluru and Mumbai remain the primary drivers, the data indicates significant untapped potential in regional markets. By focusing on hyper-local merchant adoption and diversifying into financial services like insurance, PhonePe can continue to lead the market and drive financial inclusion across the country."
                )

    with open(file_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

if __name__ == "__main__":
    final_polish_notebook("Sample_EDA_Submission_Template.ipynb")
    print("Notebook final polish complete.")
