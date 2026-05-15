import nbformat as nbf

def fix_business_objective_answer(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbf.read(f, as_version=4)

    for i, cell in enumerate(nb.cells):
        if "What do you suggest the client to achieve Business Objective ?" in cell.source:
            if i + 1 < len(nb.cells) and "Answer Here." in nb.cells[i+1].source:
                nb.cells[i+1].source = (
                    "To achieve the business objectives, I suggest the following strategies:\n\n"
                    "1. **Localized Expansion**: Invest in onboarding merchants in Tier-2 and Tier-3 cities of high-growth states like Uttar Pradesh and Bihar, where the user base is large but transaction frequency is still growing.\n"
                    "2. **Feature Optimization**: Since Peer-to-Peer (P2P) transfers are dominant, introduce incentives for users to convert these into Merchant payments (e.g., cashback for paying local vendors).\n"
                    "3. **Insurance Cross-selling**: Leverage the steady growth in the insurance sector by offering personalized, low-ticket insurance products (like mobile or health micro-insurance) directly to users identified as frequent transactors in urban hubs.\n"
                    "4. **Brand-Specific Campaigns**: Partner with top mobile brands (Xiaomi, Samsung) for exclusive in-app offers to deepen engagement with the existing heavy user base.\n"
                    "5. **Seasonal Retention**: Plan major loyalty programs during Q3 and Q4 to capitalize on the identified festive season surge, ensuring users remain on the platform after the peak period."
                )

    with open(file_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

if __name__ == "__main__":
    fix_business_objective_answer("Sample_EDA_Submission_Template.ipynb")
    print("Business Objective answer fixed successfully.")
