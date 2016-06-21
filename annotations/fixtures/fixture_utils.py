import json, datetime

def export_as_fixture(file_name, struct):
    with open(file_name, 'w') as out:
        json.dump(struct, out, sort_keys=True, indent=4)

def export_fileset(file_prefix, suffix_struct_map):
    for suffix, struct in suffix_struct_map.iteritems():
        export_as_fixture(file_prefix + suffix, struct)

# insert field names and model name from a list of tuples
def add_field_and_model_names(tuple_list, field_names, model_name, **kwargs):
    def make_single_row(tup):
        base_obj = dict(model=model_name,
                    fields = dict(zip(field_names, tup)))
        if kwargs['pk']:
            make_single_row.pk += 1
            base_obj['pk'] = make_single_row.pk
        if kwargs["timestamp"]:
            now = time_now()
            base_obj['fields']['created_on'] = now
            base_obj['fields']['last_edited'] = now
        return base_obj
    make_single_row.pk = 0

    return map(make_single_row, tuple_list)

def time_now():
    return datetime.date.today().strftime("%Y-%m-%d")

