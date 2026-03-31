let
    Source = Csv.Document(File.Contents("C:\Users\almon\Documents\projects\pricing_analytics-excel\data\raw\sales_transactions.csv"),[Delimiter=",", Columns=12, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Removed Duplicates" = Table.Distinct(#"Promoted Headers", {"transaction_id"}),
    #"Trimmed Text" = Table.TransformColumns(#"Removed Duplicates",{{"product_id", Text.Trim, type text}, {"date", Text.Trim, type text}, {"customer_id", Text.Trim, type text}, {"region_id", Text.Trim, type text}}),
    #"Cleaned Text" = Table.TransformColumns(#"Trimmed Text",{{"product_id", Text.Clean, type text}, {"date", Text.Clean, type text}, {"customer_id", Text.Clean, type text}, {"region_id", Text.Clean, type text}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Cleaned Text",{"transaction_id", "date", "product_id", "customer_id", "region_id", "discount_pct", "cost", "units_sold", "final_price", "list_price", "revenue", "profit"}),
    #"Invoked Custom Function" = Table.AddColumn(#"Reordered Columns", "units_sold_clean", each fn_clean_numeric([units_sold])),
    #"Invoked Custom Function1" = Table.AddColumn(#"Invoked Custom Function", "final_price_clean", each fn_clean_numeric([final_price])),
    #"Invoked Custom Function2" = Table.AddColumn(#"Invoked Custom Function1", "list_price_clean", each fn_clean_numeric([list_price])),
    #"Invoked Custom Function3" = Table.AddColumn(#"Invoked Custom Function2", "revenue_clean", each fn_clean_numeric([revenue])),
    #"Invoked Custom Function4" = Table.AddColumn(#"Invoked Custom Function3", "profit_clean", each fn_clean_numeric([profit])),
    #"Removed Columns" = Table.RemoveColumns(#"Invoked Custom Function4",{"units_sold", "final_price", "list_price", "revenue", "profit"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns",{{"profit_clean", type number}, {"revenue_clean", type number}, {"list_price_clean", type number}, {"final_price_clean", type number}, {"units_sold_clean", type number}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "profit_flag", each if [profit_clean] < 0 then "negative_profit" else null),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom",{{"discount_pct", type number}}),
    #"Added Custom1" = Table.AddColumn(#"Changed Type1", "discount_flag ", each if [discount_pct] > 1 then "invalid_discount" else null),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "discount_flag2", each if [discount_pct] > 1 then null else [discount_pct]),
    #"Removed Columns1" = Table.RemoveColumns(#"Added Custom2",{"discount_pct"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns1",{{"discount_flag2", "discount_pct_clean"}}),
    #"Added Custom3" = Table.AddColumn(#"Renamed Columns", "units_sold_flag", each if [units_sold_clean] > 500 then "outlier" else null),
    #"Added Custom4" = Table.AddColumn(#"Added Custom3", "Custom", each if [units_sold_clean] > 500 then null else [units_sold_clean]),
    #"Removed Columns2" = Table.RemoveColumns(#"Added Custom4",{"units_sold_clean"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns2",{{"Custom", "units_sold_clean_clean"}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Renamed Columns1",{{"units_sold_clean_clean", type number}}),
    #"Added Custom5" = Table.AddColumn(#"Changed Type2", "date_clean", each try Date.From(DateTime.FromText([date])) otherwise null),
    #"Changed Type3" = Table.TransformColumnTypes(#"Added Custom5",{{"date_clean", type date}}),
    #"Removed Columns3" = Table.RemoveColumns(#"Changed Type3",{"date"}),
    #"Added Custom6" = Table.AddColumn(#"Removed Columns3", "product_id_temp", each try Number.From([product_id]) otherwise null),
    #"Changed Type4" = Table.TransformColumnTypes(#"Added Custom6",{{"product_id_temp", Int64.Type}}),
    #"Added Custom7" = Table.AddColumn(#"Changed Type4", "customer_id_temp", each try Number.From([customer_id]) otherwise null),
    #"Changed Type5" = Table.TransformColumnTypes(#"Added Custom7",{{"customer_id_temp", Int64.Type}}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type5", {"customer_id_temp"}, dim_customers, {"customer_id"}, "dim_customers", JoinKind.Inner),
    #"Removed Columns4" = Table.RemoveColumns(#"Merged Queries",{"dim_customers"}),
    #"Merged Queries1" = Table.NestedJoin(#"Removed Columns4", {"product_id_temp"}, dim_products, {"product_id"}, "dim_products", JoinKind.Inner),
    #"Removed Columns5" = Table.RemoveColumns(#"Merged Queries1",{"dim_products", "customer_id_temp", "product_id_temp"}),
    #"Changed Type6" = Table.TransformColumnTypes(#"Removed Columns5",{{"transaction_id", Int64.Type}, {"product_id", Int64.Type}, {"customer_id", Int64.Type}, {"discount_pct_clean", type number}, {"cost", type number}}),
    #"Renamed Columns2" = Table.RenameColumns(#"Changed Type6",{{"final_price_clean", "final_price"}, {"list_price_clean", "list_price"}, {"revenue_clean", "revenue"}, {"profit_clean", "profit"}, {"discount_pct_clean", "discount_pct"}, {"units_sold_clean_clean", "units_sold"}, {"date_clean", "date"}}),
    #"Added Custom8" = Table.AddColumn(#"Renamed Columns2", "row_quality", each let
    nullCount = 
        (if [date] = null then 1 else 0) +
        (if [final_price] = null then 1 else 0) +
        (if [revenue] = null then 1 else 0) +
        (if [profit] = null then 1 else 0) +
        (if [units_sold] = null then 1 else 0)
in
    if nullCount = 0 then "complete"
    else if nullCount <= 1 then "partial"
    else "incomplete"),
    #"Added Custom9" = Table.AddColumn(#"Added Custom8", "margin_pct", each if [cost] = null or [revenue] = null then null
else Number.Round(([revenue] - [cost]) / [revenue], 4)),
    #"Changed Type7" = Table.TransformColumnTypes(#"Added Custom9",{{"margin_pct", type number}})
in
    #"Changed Type7"