let
    Source = Table.NestedJoin(fact_competitors, {"product_id"}, dim_products, {"product_id"}, "dim_products", JoinKind.LeftAnti)
in
    Source