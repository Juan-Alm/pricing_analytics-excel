let
    Source = Csv.Document(File.Contents("C:\Users\almon\Documents\projects\pricing_analytics-excel\data\raw\customers.csv"),[Delimiter=",", Columns=5, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Trimmed Text" = Table.TransformColumns(#"Promoted Headers",{{"region_id", Text.Trim, type text}, {"industry", Text.Trim, type text}, {"segment", Text.Trim, type text}, {"customer_name", Text.Trim, type text}}),
    #"Cleaned Text" = Table.TransformColumns(#"Trimmed Text",{{"region_id", Text.Clean, type text}, {"industry", Text.Clean, type text}, {"segment", Text.Clean, type text}, {"customer_name", Text.Clean, type text}}),
    #"Removed Duplicates" = Table.Distinct(#"Cleaned Text", {"customer_id"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Duplicates", {"region_id"}, dim_regions, {"region_id"}, "dim_regions", JoinKind.Inner),
    #"Removed Columns" = Table.RemoveColumns(#"Merged Queries",{"dim_regions"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns",{{"customer_id", Int64.Type}})
in
    #"Changed Type"