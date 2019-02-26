from typing import get_type_hints

from graphql import GraphQLField

from .type_converter import get_graphql_type_for_annotation


def field(wrap):
    # TODO: add prefix, make it a constant
    wrap._is_field = True
    # TODO: show error if no return type
    annotations = get_type_hints(wrap)

    field_type = get_graphql_type_for_annotation(annotations["return"], wrap.__name__)

    arguments_annotations = {
        key: value
        for key, value in annotations.items()
        if key not in ["info", "root", "return"]
    }

    arguments = {
        name: get_graphql_type_for_annotation(annotation, name)
        for name, annotation in arguments_annotations.items()
    }

    wrap.field = GraphQLField(field_type, args=arguments, resolve=wrap)
    return wrap
