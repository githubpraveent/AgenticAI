# Bank of America Statement Parser

A Python application to extract transactions from Bank of America PDF statements and export them to Excel format for tax filing calculations.

## Features

- Extracts transactions from Bank of America monthly statements
- Parses Deposits and other credits
- Parses Withdrawals and other debits (including continued sections)
- Exports all transactions to Excel (.xlsx) format
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
1. Read the PDF from: `/Volumes/D/Praveen_Mac_D/InfiTrends/InfiTrends_Bank_Stmts/InfiTrends_eStmt_2025-01-31.pdf`
2. Extract all transactions
3. Generate an Excel file in: `/Volumes/D/Praveen_Mac_D/InfiTrends/InfiTrends_Bank_Stmts/Stmt_Excels/`

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

The Excel file contains the following columns:
- **Date**: Transaction date (YYYY-MM-DD format)
- **Type**: "Deposit" or "Withdrawal"
- **Description**: Transaction description
- **Amount**: Transaction amount (positive for deposits, negative for withdrawals)
- **Raw_Line**: Original line from PDF (for reference)

## Notes

- The parser uses both table extraction and text extraction methods to maximize transaction detection
- Transactions are automatically sorted by date
- Withdrawal amounts are shown as negative values
- The output directory will be created automatically if it doesn't exist
