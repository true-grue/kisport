function RawBlock(raw)
    if raw.format:match 'html' and raw.text:match '%<table' then
        local ast = pandoc.read(raw.text, 'html')
        local table = ast.blocks[1]
        local caption = table.attr.identifier
        table.caption = pandoc.Caption({pandoc.Str(caption)})
        local div = pandoc.walk_block(pandoc.Div(ast.blocks), {
            Plain = function (element)
                local md = pandoc.utils.stringify(element)
                local ast = pandoc.read(md, 'markdown')
                return ast.blocks
            end
        })
        return div.content
    end
end
