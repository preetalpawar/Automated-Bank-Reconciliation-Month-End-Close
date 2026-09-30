SELECT
    COUNT(*) AS total_bank_transactions,

    SUM(
        CASE
            WHEN g."Reference" IS NOT NULL
            AND (b."Debit" + b."Credit") = g."Amount"
            THEN 1 ELSE 0
        END
    ) AS matched_transactions,

    SUM(
        CASE
            WHEN g."Reference" IS NULL
            THEN 1 ELSE 0
        END
    ) AS unmatched_transactions,

    SUM(
        CASE
            WHEN g."Reference" IS NOT NULL
            AND (b."Debit" + b."Credit") <> g."Amount"
            THEN 1 ELSE 0
        END
    ) AS amount_mismatches

FROM bank_statement AS b
LEFT JOIN general_ledger AS g
    ON b."Reference" = g."Reference";