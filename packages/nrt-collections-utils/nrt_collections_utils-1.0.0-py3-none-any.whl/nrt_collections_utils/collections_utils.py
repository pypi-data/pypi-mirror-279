

class CollectionsUtil:

    @classmethod
    def deep_args_to_list(cls, *args) -> list:
        args_list = []

        for arg in args:
            args_list.extend(cls.__args_to_list_recursive(arg))

        return args_list

    @staticmethod
    def is_iter(obj) -> bool:
        try:
            iter(obj)
        except TypeError:
            return False

        return True

    @classmethod
    def __args_to_list_recursive(cls, arg):
        args_list = []

        if cls.is_iter(arg) and not isinstance(arg, str):
            for a in arg:
                args_list.extend(cls.__args_to_list_recursive(a))
        else:
            args_list.append(arg)

        return args_list
