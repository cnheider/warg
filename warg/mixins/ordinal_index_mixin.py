__all__ = [
    "OrdinalIndexingDictMixin",
]


#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.


class OrdinalIndexingDictMixin:
    """
    Mixin class for indexing a class instance __dict__ (SortedDict) with both integer (ordinal) indexing or
    key:str attributes (non-ordinal) access."""

    def __getitem__(self, item):
        if isinstance(item, int):
            return list(self.__dict__.values())[item]
        else:
            return self.__dict__[item]


if __name__ == "__main__":

    def asd() -> None:
        """
        :rtype: None
        """

        class IDTM(OrdinalIndexingDictMixin):
            pass

        a = IDTM()
        a.a = 2
        a.b = 3
        assert a[0] == 2
        assert a[1] == 3
