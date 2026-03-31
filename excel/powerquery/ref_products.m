let
    Source = Csv.Document(File.Contents("C:\Users\almon\Documents\projects\pricing_analytics-excel\data\clean\products.csv"),[Delimiter=",", Columns=7, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Use First Row as Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Change Type" = Table.TransformColumnTypes(#"Use First Row as Headers",{{"product_id", Int64.Type}, {"product_name", type text}, {"category", type text}, {"subcategory", type text}, {"brand", type text}, {"base_price", type number}, {"cost", type number}})
in
    #"Change Type"