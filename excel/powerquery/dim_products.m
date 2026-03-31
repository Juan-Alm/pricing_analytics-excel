let
    Source = Csv.Document(File.Contents("C:\Users\almon\Documents\projects\pricing_analytics-excel\data\raw\products.csv"),[Delimiter=",", Columns=7, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Trimmed Text" = Table.TransformColumns(#"Promoted Headers",{{"product_name", Text.Trim, type text}, {"category", Text.Trim, type text}, {"subcategory", Text.Trim, type text}, {"brand", Text.Trim, type text}}),
    #"Cleaned Text" = Table.TransformColumns(#"Trimmed Text",{{"product_name", Text.Clean, type text}, {"category", Text.Clean, type text}, {"subcategory", Text.Clean, type text}, {"brand", Text.Clean, type text}}),
    #"Capitalized Each Word" = Table.TransformColumns(#"Cleaned Text",{{"product_name", Text.Proper, type text}, {"category", Text.Proper, type text}, {"subcategory", Text.Proper, type text}, {"brand", Text.Proper, type text}}),
    #"Added Custom" = Table.AddColumn(#"Capitalized Each Word", "base_price_clean", each try Number.From(Text.Trim(Text.From([base_price])))
otherwise null),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"base_price_clean", type number}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"base_price"}),
    #"Added Custom1" = Table.AddColumn(#"Removed Columns", "cost_clean", each try Number.From(Text.Trim(Text.From([cost]))) otherwise null),
    #"Changed Type1" = Table.TransformColumnTypes(#"Added Custom1",{{"cost_clean", type number}, {"product_id", Int64.Type}}),
    #"Merged Queries" = Table.NestedJoin(#"Changed Type1", {"product_id"}, ref_products, {"product_id"}, "clean_products", JoinKind.LeftOuter),
    #"Expanded clean_products" = Table.ExpandTableColumn(#"Merged Queries", "clean_products", {"cost"}, {"clean_products.cost"}),
    #"Renamed Columns" = Table.RenameColumns(#"Expanded clean_products",{{"clean_products.cost", "cost_reference"}}),
    #"Added Custom2" = Table.AddColumn(#"Renamed Columns", "Custom", each if [cost_clean] = null then [cost_reference] else [cost_clean]),
    #"Removed Columns1" = Table.RemoveColumns(#"Added Custom2",{"cost", "cost_clean", "cost_reference"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns1",{{"Custom", "cost_clean"}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Renamed Columns1",{{"cost_clean", type number}}),
    #"Removed Duplicates" = Table.Distinct(#"Changed Type2", {"product_id"}),
    #"Renamed Columns2" = Table.RenameColumns(#"Removed Duplicates",{{"base_price_clean", "base_price"}, {"cost_clean", "cost"}})
in
    #"Renamed Columns2"