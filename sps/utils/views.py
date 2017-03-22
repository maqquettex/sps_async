class MetaView(type):
    pass


class BaseView(metaclass=MetaView):
    pass