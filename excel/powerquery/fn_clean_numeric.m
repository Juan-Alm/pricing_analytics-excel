(inputValue as any) as nullable number =>
let
    result =
        if inputValue = null then null
        else if Value.Is(inputValue, type number) then inputValue
        else
            let
                asText = Text.Trim(Text.From(inputValue)),
                parsed = try Number.From(asText) otherwise null
            in
                parsed
in
    result