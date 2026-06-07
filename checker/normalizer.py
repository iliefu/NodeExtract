def normalize(node):

    if "servername" in node:

        node["sni"] = node.pop(
            "servername"
        )

    if "grpc-service-name" in node:

        node["grpc-service-name"] = (
            str(
                node[
                    "grpc-service-name"
                ]
            )
        )

    if "port" in node:

        node["port"] = int(
            node["port"]
        )

    return node
