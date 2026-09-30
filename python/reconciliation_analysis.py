import pandas as pd

# Load finance data
bank = pd.read_csv("bank_statement . csv.csv")
gl = pd.read_csv("general_ledger . csv.csv")

# Reconcile Bank Statement with General Ledger
merged = bank.merge(
    gl,
    on="Reference",
    how="left",
    suffixes=("_bank", "_gl")
)

# Calculate bank transaction amount
merged["Bank Amount"] = merged["Debit"] + merged["Credit"]

# Calculate difference
merged["Difference"] = merged["Bank Amount"] - merged["Amount"]

# Classify reconciliation status
merged["Reconciliation Status"] = "Matched"

merged.loc[
    merged["Amount"].isna(),
    "Reconciliation Status"
] = "Unmatched"

merged.loc[
    merged["Amount"].notna() & (merged["Difference"] != 0),
    "Reconciliation Status"
] = "Amount Mismatch"

# Display results
print("\n--- RECONCILIATION RESULTS ---")

print(
    merged[
        [
            "Transaction ID",
            "Reference",
            "Bank Amount",
            "Amount",
            "Difference",
            "Reconciliation Status"
        ]
    ]
)

# Display summary
print("\n--- RECONCILIATION SUMMARY ---")
print(merged["Reconciliation Status"].value_counts())

# Save exceptions
exceptions = merged[
    merged["Reconciliation Status"] != "Matched"
]

exceptions.to_csv(
    "reconciliation_exceptions.csv",
    index=False
)

# Find GL transactions missing from Bank Statement
gl_unmatched = gl[
    ~gl["Reference"].isin(bank["Reference"])
]

gl_unmatched.to_csv(
    "unmatched_gl_transactions.csv",
    index=False
)

# Save complete reconciliation output
final_reconciliation = merged[
    [
        "Transaction ID",
        "Date_bank",
        "Description",
        "Reference",
        "Debit",
        "Credit",
        "Bank Amount",
        "GL ID",
        "Account",
        "Amount",
        "Difference",
        "Reconciliation Status"
    ]
]

final_reconciliation.to_csv(
    "final_reconciliation_output.csv",
    index=False
)

print("\n--- OUTPUT FILES CREATED ---")
print("reconciliation_exceptions.csv")
print("unmatched_gl_transactions.csv")
print("final_reconciliation_output.csv")