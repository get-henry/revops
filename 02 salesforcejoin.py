import os
import pandas as pd

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