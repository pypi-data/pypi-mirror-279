def name_file(struct):
    if hasattr(struct, "subkind"):
        suffix = struct.subkind
    else:
        suffix = struct.kind
    if hasattr(struct, "source"):
        if struct.source:
            fname = f"{struct.identifier}_{struct.source}_ATK{suffix}"
        elif struct.pos:
            fname = f"{struct.identifier}_ATK{suffix}"
    elif hasattr(struct, "sources"):
        if len(struct.identifiers) > 1:
            fname = f"{struct.identifiers[0]}_AndOtherSource(s)_ATK{suffix}"
        else:
            fname = f"{struct.identifiers[0]}_ATK{suffix}"

    return fname
