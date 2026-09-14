def get_model_field(object, attr, display=False, many_to_many=False):
    """ Поиск атрибута модели по дереву каталога """
    try:
        if display:
            self_attr = getattr(object, attr)()
        elif many_to_many:
            self_attr = getattr(object, attr).all()
        else:
            self_attr = getattr(object, attr)
    except:
        self_attr = ''
    if self_attr:
        return self_attr
    else:
        try:
            return get_model_field(object.tree.get().parent.content_object, attr, display, many_to_many)
        except:
            return ''
    return ''
