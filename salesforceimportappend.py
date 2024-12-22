import os
import pandas as pd

# Main execution
if __name__ == "__main__":
    # Set up file paths using os.path.join for cross-platform compatibility
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lead_report_path = os.path.join(base_dir, "data", "salesforce_lead_report.csv")
    contact_report_path = os.path.join(base_dir, "data", "salesforce_contact_report.csv")
    output_report_path = os.path.join(base_dir, "data", "salesforce_combined_report.csv")
    
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