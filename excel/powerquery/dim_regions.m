let
    Source = Csv.Document(File.Contents("C:\Users\almon\Documents\projects\pricing_analytics-excel\data\raw\regions.csv"),[Delimiter=",", Columns=5, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Change Type" = Table.TransformColumnTypes(Source,{{"Column1", type text}, {"Column2", type text}, {"Column3", type text}, {"Column4", type text}, {"Column5", type text}}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Change Type", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"region_id", type text}, {"country", type text}, {"region", type text}, {"city", type text}, {"market_type", type text}})
in
    #"Changed Type"