let
    Source = Csv.Document(File.Contents("C:\Users\almon\Documents\projects\pricing_analytics-excel\data\raw\competitor_prices.csv"),[Delimiter=",", Columns=4, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Trimmed Text" = Table.TransformColumns(#"Promoted Headers",{{"date", Text.Trim, type text}, {"competitor_name", Text.Trim, type text}}),
    #"Cleaned Text" = Table.TransformColumns(#"Trimmed Text",{{"date", Text.Clean, type text}, {"competitor_name", Text.Clean, type text}}),
    #"Added Custom" = Table.AddColumn(#"Cleaned Text", "date_clean", each try Date.From(DateTime.FromText([date])) otherwise null),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"date_clean", type date}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"date"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"date_clean", "date"}}),
    #"Invoked Custom Function" = Table.AddColumn(#"Renamed Columns", "competitor_price_clean", each fn_clean_numeric([competitor_price])),
    #"Changed Type1" = Table.TransformColumnTypes(#"Invoked Custom Function",{{"competitor_price_clean", type number}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Changed Type1",{"competitor_price"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns1",{{"competitor_price_clean", "competitor_price"}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Renamed Columns1",{{"product_id", type number}}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type2", {"product_id"}, dim_products, {"product_id"}, "dim_products", JoinKind.LeftOuter),
    #"Expanded dim_products" = Table.ExpandTableColumn(#"Merged Queries", "dim_products", {"base_price", "cost"}, {"dim_products.base_price", "dim_products.cost"}),
    #"Renamed Columns2" = Table.RenameColumns(#"Expanded dim_products",{{"dim_products.base_price", "base_price"}, {"dim_products.cost", "products.cost"}}),
    #"Added Custom1" = Table.AddColumn(#"Renamed Columns2", "price_index", each if [base_price] = null or [competitor_price] = null then null
else Number.Round([competitor_price] / [base_price], 3)),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "price_position", each if [price_index] = null then null
else if [price_index] < 0.95 then "competitor cheaper"
else if [price_index] > 1.05 then "competitor dearer"
else "at parity"),
    #"Changed Type3" = Table.TransformColumnTypes(#"Added Custom2",{{"price_index", type number}, {"price_position", type text}})
in
    #"Changed Type3"