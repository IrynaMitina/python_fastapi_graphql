
def get_field_names(info):
    """info from resolver;
    e.g. for movies resolver:
    ['.movies.id',
     '.movies.title',
     '.movies.releaseYear',
     '.movies.country',
     '.movies.director.fullName',
     '.movies.director.birthDate',
     '.movies.director.type',
     '.movies.genres']
    """
    node_dict = info.field_nodes[0].to_dict()
    return _get_field_names(node_dict)

def _get_field_names(node_dict, parent_prefix=""):
    fields = []
    prefix = f"{parent_prefix}.{node_dict['name']['value']}"
    for item in node_dict["selection_set"]["selections"]:
        if not item["selection_set"]:  # scalar field, not object
            fields.append(f"{prefix}.{item['name']['value']}")
        else:
            subfields = _get_field_names(item, prefix)
            fields.extend(subfields)
    return fields
