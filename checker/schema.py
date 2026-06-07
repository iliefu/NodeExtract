def proxy(node):

    return {

        k:v

        for k,v in node.items()

        if v not in (
            None,
            "",
            []
        )
    }
