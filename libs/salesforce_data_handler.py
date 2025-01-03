import os
import pandas as pd

class SalesforceDataHandler:
    """
    A class that encapsulates reading, combining, and joining Salesforce data.

    This class is designed to streamline working with the legacy code,
    while following best practices for modularity and maintainability.

    Attributes:
        base_dir (str): The base directory used for reading/writing files.
        lead_report_path (str): Path to the Salesforce Lead report.
        contact_report_path (str): Path to the Salesforce Contact report.
        account_report_path (str): (Optional) Path to the Salesforce Account report, if needed.
    """
    
    def __init__(self, base_dir: str, lead_filename: str, contact_filename: str, account_filename: str = None):
        """
        Initializes SalesforceDataHandler with paths for leads, contacts, and (optionally) accounts.

        Args:
            base_dir (str): The base directory used for reading/writing files.
            lead_filename (str): Filename for the Lead CSV (e.g., 'salesforce_lead_report.csv').
            contact_filename (str): Filename for the Contact CSV (e.g., 'salesforce_contact_report.csv').
            account_filename (str, optional): Filename for the Account CSV (e.g., 'salesforce_account_report.csv'). 
                Defaults to None if you do not need account data.
        """
        self.base_dir = base_dir
        self.lead_report_path = os.path.join(base_dir, "data", lead_filename)
        self.contact_report_path = os.path.join(base_dir, "data", contact_filename)
        self.account_report_path = (
            os.path.join(base_dir, "data", account_filename)
            if account_filename is not None
            else None
        )
    
    def _read_and_prepare_report(self, csv_path: str, id_column: str, record_type: str) -> pd.DataFrame:
        """
        Reads a Salesforce CSV report, renames the ID column to 'Record ID', 
        and adds a 'Record Type' column.

        Args:
            csv_path (str): Full path to the CSV file.
            id_column (str): The original ID column name (e.g., 'Lead ID', 'Contact ID').
            record_type (str): The record type to set (e.g., 'Lead', 'Contact').

        Returns:
            pd.DataFrame: The processed DataFrame.
        """
        df = pd.read_csv(csv_path)
        df.rename(columns={id_column: "Record ID"}, inplace=True)
        df["Record Type"] = record_type
        return df

    def _combine_reports(self, dataframes: list[pd.DataFrame]) -> pd.DataFrame:
        """
        Combines multiple DataFrames (e.g., leads and contacts) into one.

        Args:
            dataframes (list[pd.DataFrame]): A list of DataFrames to concatenate.

        Returns:
            pd.DataFrame: A single combined DataFrame.
        """
        return pd.concat(dataframes, ignore_index=True)

    def get_combined_lead_contact(self) -> pd.DataFrame:
        """
        Reads and combines lead and contact CSVs into a single DataFrame.

        Returns:
            pd.DataFrame: A combined DataFrame with leads and contacts.
        """
        # Read leads
        lead_df = self._read_and_prepare_report(
            self.lead_report_path, 
            id_column="Lead ID", 
            record_type="Lead"
        )

        # Read contacts
        contact_df = self._read_and_prepare_report(
            self.contact_report_path, 
            id_column="Contact ID", 
            record_type="Contact"
        )

        # Combine
        combined_df = self._combine_reports([lead_df, contact_df])
        return combined_df

    def save_combined_lead_contact(self, output_filename: str) -> None:
        """
        Saves the combined lead/contact data to a CSV.

        Args:
            output_filename (str): Filename for the combined CSV (e.g., 'salesforce_combined_report.csv').
        """
        output_path = os.path.join(self.base_dir, "data", output_filename)
        combined_df = self.get_combined_lead_contact()
        combined_df.to_csv(output_path, index=False)
        print(f"Combined lead/contact report saved to: {output_path}")

    def join_with_account_data(self, combined_df: pd.DataFrame, account_key: str = "Account ID") -> pd.DataFrame:
        """
        Performs a left join between the combined lead/contact DataFrame and the account DataFrame.

        Args:
            combined_df (pd.DataFrame): A DataFrame of leads/contacts with an 'Account ID' column.
            account_key (str): The join key column (e.g., 'Account ID').

        Returns:
            pd.DataFrame: A joined DataFrame that includes account columns.
        """
        if not self.account_report_path:
            raise ValueError("No account file was provided during initialization.")
        
        account_df = pd.read_csv(self.account_report_path)
        
        joined_df = combined_df.merge(account_df, on=account_key, how="left")

        # Optional: rename columns to avoid collisions
        joined_df.rename(
            columns=lambda col: col.replace("_x", "_person").replace("_y", "_account"), 
            inplace=True
        )
        return joined_df

    def save_joined_report(self, combined_df: pd.DataFrame, joined_filename: str) -> None:
        """
        Saves the joined (combined leads/contacts + account) data to a CSV.

        Args:
            combined_df (pd.DataFrame): The DataFrame to join with accounts.
            joined_filename (str): Filename for the joined CSV (e.g., 'salesforce_joined_report.csv').
        """
        if not self.account_report_path:
            raise ValueError("No account file was provided to save joined report.")
        
        joined_path = os.path.join(self.base_dir, "data", joined_filename)
        joined_df = self.join_with_account_data(combined_df)
        joined_df.to_csv(joined_path, index=False)
        print(f"Joined lead/contact/account report saved to: {joined_path}")
        
        # Example: count how many Account IDs were matched
        unique_matches = joined_df[joined_df["Account Name"].notnull()][
            "Account ID"
        ].nunique()
        print(f"Number of unique matched Account IDs: {unique_matches}")
