def dobule_to_dict(v):
    result = {}
    for key in v.__mapper__.c.keys():
        if getattr(v, key) is not None:
            result[key] = str(getattr(v, key))
        else:
            result[key] = getattr(v, key)
    return result


def to_json(all_vendors):
    v = [ dobule_to_dict(ven) for ven in all_vendors ]
    return v