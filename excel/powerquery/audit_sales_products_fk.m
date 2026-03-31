let
    Source = Table.NestedJoin(fact_sales_snapshot, {"product_id_temp"}, dim_products, {"product_id"}, "dim_products", JoinKind.LeftAnti),
    #"Added Custom" = Table.AddColumn(Source, "rejection_reason", each "invalid product_id")
in
    #"Added Custom"