import pytest
import pandas as pd
from pathlib import Path
from libs.salesforce_data_handler import SalesforceDataHandler


@pytest.fixture
def setup_test_files(tmp_path):
    """
    Creates a temporary directory with sample CSV data for leads, contacts, 
    and accounts. Returns the temp path so tests can read/write there.
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    # 1) Create a sample Lead CSV
    lead_csv = data_dir / "salesforce_lead_report.csv"
    lead_csv.write_text(
        "Lead ID,Name,Account ID\n"
        "1,Alice,100\n"
        "2,Bob,\n"
    )

    # 2) Create a sample Contact CSV
    contact_csv = data_dir / "salesforce_contact_report.csv"
    contact_csv.write_text(
        "Contact ID,Name,Account ID\n"
        "10,Charlie,200\n"
        "11,Diana,100\n"
    )

    # 3) Create a sample Account CSV
    account_csv = data_dir / "salesforce_account_report.csv"
    account_csv.write_text(
        "Account ID,Account Name\n"
        "100,Acme Corp\n"
        "200,Globex\n"
        "300,Initech\n"
    )

    # Return the top-level tmp_path
    return tmp_path


def test_get_combined_lead_contact(setup_test_files):
    """
    Test get_combined_lead_contact ensures we combine
    leads and contacts properly and that columns are standardized.
    """
    handler = SalesforceDataHandler(
        base_dir=str(setup_test_files),
        lead_filename="salesforce_lead_report.csv",
        contact_filename="salesforce_contact_report.csv"
    )

    combined_df = handler.get_combined_lead_contact()

    # Should have 2 leads + 2 contacts = 4 rows
    assert len(combined_df) == 4, "Expected 4 total rows in combined lead/contact data."

    # Check required columns
    assert "Record ID" in combined_df.columns
    assert "Record Type" in combined_df.columns
    assert "Name" in combined_df.columns

    # Verify that 2 rows are "Lead" and 2 rows are "Contact"
    lead_count = (combined_df["Record Type"] == "Lead").sum()
    contact_count = (combined_df["Record Type"] == "Contact").sum()
    assert lead_count == 2, f"Expected 2 lead rows but got {lead_count}"
    assert contact_count == 2, f"Expected 2 contact rows but got {contact_count}"


def test_join_with_account_data(setup_test_files):
    """
    Test join_with_account_data ensures that the combined DF
    is successfully joined with the account CSV using Account ID.
    """
    handler = SalesforceDataHandler(
        base_dir=str(setup_test_files),
        lead_filename="salesforce_lead_report.csv",
        contact_filename="salesforce_contact_report.csv",
        account_filename="salesforce_account_report.csv"
    )

    # Combine leads/contacts
    combined_df = handler.get_combined_lead_contact()

    # Join with account
    joined_df = handler.join_with_account_data(combined_df)
    assert "Account Name" in joined_df.columns, "Joined DataFrame should contain 'Account Name'."

    # Check that "Alice" (lead row) with Account ID = 100 is joined to "Acme Corp"
    alice_row = joined_df.loc[joined_df["Name"] == "Alice"].iloc[0]
    assert alice_row["Account Name"] == "Acme Corp", "Alice should be associated with 'Acme Corp'."


def test_save_combined_lead_contact(setup_test_files):
    """
    Test save_combined_lead_contact ensures CSV is written to disk 
    with the correct rows/columns.
    """
    handler = SalesforceDataHandler(
        base_dir=str(setup_test_files),
        lead_filename="salesforce_lead_report.csv",
        contact_filename="salesforce_contact_report.csv",
        account_filename="salesforce_account_report.csv"
    )

    output_file = "salesforce_combined_output.csv"
    handler.save_combined_lead_contact(output_file)

    # Confirm the file was created
    combined_path = Path(setup_test_files) / "data" / output_file
    assert combined_path.exists(), "Combined lead/contact output file was not created."

    # Read it back in to verify contents
    df = pd.read_csv(combined_path)
    assert len(df) == 4, "Expected 4 rows in the combined CSV."
    assert "Record ID" in df.columns
    assert "Record Type" in df.columns


def test_save_joined_report(setup_test_files, capsys):
    """
    Test save_joined_report ensures that a joined CSV is written to disk
    and logs the correct number of matched Account IDs.
    """
    handler = SalesforceDataHandler(
        base_dir=str(setup_test_files),
        lead_filename="salesforce_lead_report.csv",
        contact_filename="salesforce_contact_report.csv",
        account_filename="salesforce_account_report.csv"
    )

    combined_df = handler.get_combined_lead_contact()
    output_file = "salesforce_joined_output.csv"
    handler.save_joined_report(combined_df, output_file)

    # Confirm the file was created
    joined_path = Path(setup_test_files) / "data" / output_file
    assert joined_path.exists(), "Joined output file was not created."

    # Read it back and confirm that Account Name is present
    joined_df = pd.read_csv(joined_path)
    assert "Account Name" in joined_df.columns, "Joined CSV should contain 'Account Name'."
    assert len(joined_df) == 4, "Expected 4 total rows in the joined CSV."

    # Capture printed output and confirm match count was printed
    captured = capsys.readouterr()
    assert "Number of unique matched Account IDs:" in captured.out, \
        "Expected the joined report print statement with matched account count."
