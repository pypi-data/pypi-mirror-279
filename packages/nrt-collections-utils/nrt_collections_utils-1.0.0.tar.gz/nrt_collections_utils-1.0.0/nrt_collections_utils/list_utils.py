

class ListUtil:
    @staticmethod
    def compare_lists(list_1: list, list_2: list) -> bool:
        if len(list_1) != len(list_2):
            return False

        for item in list_1:
            if item not in list_2:
                return False

        for item in list_2:
            if item not in list_1:
                return False

        return True

    @staticmethod
    def remove_none(list_: list):
        return [x for x in list_ if x is not None]

    @staticmethod
    def remove_duplicates(list_: list):
        return list(set(list_))
