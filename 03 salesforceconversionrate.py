import os
import pandas as pd
import matplotlib.pyplot as plt

# Main execution
if __name__ == "__main__":
    # Set up file paths using os.path.join for cross-platform compatibility
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lead_report_path = os.path.join(base_dir, "data", "salesforce_lead_report.csv")
    contact_report_path = os.path.join(base_dir, "data", "salesforce_contact_report.csv")
    output_report_path = os.path.join(base_dir, "data", "salesforce_combined_report.csv")
    
    account_report_path = os.path.join(base_dir, "data", "salesforce_account_report.csv")
    joined_report_path = os.path.join(base_dir, "data", "salesforce_joined_report.csv")
    
    # Read the lead report
    lead_df = pd.read_csv(lead_report_path)
    lead_df.rename(columns={"Lead ID": "Record ID"}, inplace=True)
    lead_df["Record Type"] = "Lead"  # Add a column to differentiate records
    
    # Read the contact report
    contact_df = pd.read_csv(contact_report_path)
    contact_df.rename(columns={"Contact ID": "Record ID"}, inplace=True)
    contact_df["Record Type"] = "Contact"  # Add a column to differentiate records
    
    # Append the reports together
    combined_df = pd.concat([lead_df, contact_df], ignore_index=True)
    
    # Save the combined data to a new CSV file
    combined_df.to_csv(output_report_path, index=False)
    print(f"Combined report saved to: {output_report_path}")
    
    # Read the account report
    account_df = pd.read_csv(account_report_path)

    # Perform a left join to include all leads and contacts and match accounts
    joined_df = combined_df.merge(account_df, on="Account ID", how="left")
    
    # Rename columns with _x to _person and _y to _account
    joined_df = joined_df.rename(columns=lambda col: col.replace("_x", "_person").replace("_y", "_account"))
    
    # Count unique matches by checking non-null Account Name and counting unique Account IDs
    unique_matches = joined_df[joined_df["Account Name"].notnull()]["Account ID"].nunique()
    print(f"Number of unique matched Account IDs: {unique_matches}")

    # Save the joined data to a new CSV file
    joined_df.to_csv(joined_report_path, index=False)
    print(f"Joined report saved to: {joined_report_path}")
    
    # Calculate total leads, converted leads, and conversion rate by record type
    conversion_summary = joined_df.groupby("Record Type").agg(
        Total_Leads=("Record Type", "count"),
        Converted=("Lead Status", lambda x: (x == "Closed - Converted").sum()),
        Total_Accounts=("Account ID", "nunique"),
        Accounts_Converted=("Account ID", lambda x: x[joined_df.loc[x.index, "Lead Status"] == "Closed - Converted"].nunique())
    )
    
    # Calculate conversion rates
    conversion_summary["Converted Rate (%)"] = (
        (conversion_summary["Converted"] / conversion_summary["Total_Leads"]) * 100
    ).round(2)
    conversion_summary["Account Converted Rate (%)"] = (
        (conversion_summary["Accounts_Converted"] / conversion_summary["Total_Accounts"]) * 100
    ).round(2)

    # Add a combined row for overall totals
    overall_totals = pd.DataFrame({
        "Total_Leads": [conversion_summary["Total_Leads"].sum()],
        "Converted": [conversion_summary["Converted"].sum()],
        "Total_Accounts": [conversion_summary["Total_Accounts"].sum()],
        "Accounts_Converted": [conversion_summary["Accounts_Converted"].sum()],
        "Converted Rate (%)": [(conversion_summary["Converted"].sum() / conversion_summary["Total_Leads"].sum() * 100).round(2)],
        "Account Converted Rate (%)": [(conversion_summary["Accounts_Converted"].sum() / conversion_summary["Total_Accounts"].sum() * 100).round(2)]
    }, index=["Combined"])


    # Append combined totals to the summary
    conversion_summary = pd.concat([conversion_summary, overall_totals])
    
    # Create a tabular display using matplotlib
    fig, ax = plt.subplots(figsize=(8, 3))  # Adjust figure size as needed
    ax.axis("tight")
    ax.axis("off")
    table_data = conversion_summary.values.tolist()
    table_columns = conversion_summary.columns.tolist()
    
    # Add the table to the figure
    table = ax.table(cellText=table_data, colLabels=table_columns, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(table_columns))))  # Adjust column width
    
    # Display the table
    plt.title("Lead & Account Conversion Rate Report", fontsize=14, weight="bold")
    plt.show()