let
    Source = Table.NestedJoin(dim_customers, {"region_id"}, dim_regions, {"region_id"}, "raw_regions", JoinKind.LeftAnti),
    #"Added Custom" = Table.AddColumn(Source, "rejection_reasion", each "invalid region_id"),
    #"Removed Columns" = Table.RemoveColumns(#"Added Custom",{"raw_regions"})
in
    #"Removed Columns"