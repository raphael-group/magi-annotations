import json

def export_as_fixture(file_name, struct):
    with open(file_name, 'w') as out:
        json.dump(struct, out, sort_keys=True, indent=4)

def export_fileset(file_prefix, suffix_struct_map):
    for suffix, struct in suffix_struct_map.iteritems():
        export_as_fixture(file_prefix + suffix, struct)

# insert field names and model name from a list of tuples
def add_field_and_model_names(tuple_list, field_names, model_name, **kwargs):
#    if kwargs["pk"]:
    def make_single_row(tup):
        return dict(model=model_name,
                    fields = dict(zip(field_names, tup)))

    return map(make_single_row, tuple_list)
    
