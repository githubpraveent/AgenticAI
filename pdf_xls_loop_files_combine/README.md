# Bank of America Statement Parser

A Python application to extract transactions from Bank of America PDF statements and export them to Excel format for tax filing calculations.

## Features

- Extracts transactions from Bank of America monthly statements
- Parses Deposits and other credits
- Parses Withdrawals and other debits (including continued sections)
- **One Excel file per statement**: each PDF is written to `{statement_name}_transactions.xlsx`
- **Combined workbook** (`combine_all_xls.xlsx`): merges all outputs into a single file with:
  - **One tab per statement**: each tab keeps all data from that statement
  - **combine_data tab**: all transactions from every statement consolidated in one sheet (with a `Source` column) for bank reconciliation
- Formats Excel with proper date sorting and amount formatting

## Requirements

- Python 3.7 or higher
- Required packages (see requirements.txt)

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script directly:
```bash
python bank_statement_parser.py
```

The script will:
1. Read all PDFs from: `/Volumes/D/Praveen_Mac_D/InfiTrends/InfiTrends_Bank_Stmts/`
2. Extract transactions from each statement
3. Write one Excel file per statement to: `/Volumes/D/Praveen_Mac_D/InfiTrends/InfiTrends_Bank_Stmts/Stmt_Excels/`
4. Create `combine_all_xls.xlsx` in the same folder with one tab per statement plus a `combine_data` tab

### Custom Usage

You can modify the `main()` function in `bank_statement_parser.py` to use different file paths:

```python
parser = BankStatementParser(
    pdf_path="path/to/your/statement.pdf",
    output_dir="path/to/output/directory"
)
transactions = parser.process()
parser.export_to_excel()
```

## Output Format

**Per-statement files** (`{statement_name}_transactions.xlsx`) and each **statement tab** in `combine_all_xls.xlsx` contain:
- **Date**: Transaction date (YYYY-MM-DD format)
- **Type**: "Deposit" or "Withdrawal"
- **Description**: Transaction description
- **Amount**: Transaction amount (positive for deposits, negative for withdrawals)
- **Raw_Line**: Original line from PDF (for reference)

**combine_data tab** (in `combine_all_xls.xlsx`) has the same columns plus **Source** (statement/file name) so you can reconcile all bank transactions across statements.

## Notes

- The parser uses both table extraction and text extraction methods to maximize transaction detection
- Transactions are automatically sorted by date
- Withdrawal amounts are shown as negative values
- The output directory will be created automatically if it doesn't exist
