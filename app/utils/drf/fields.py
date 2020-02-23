from rest_framework import serializers

__all__ = (
    'PkModelField',
)


class PkModelField(serializers.Field):
    """
    특정 Model의 instance를 나타내는 Field
    주어지는 데이터가
        dict
            {'pk': 1}
        literal (pk가 될 수 있는 숫자/문자 등의 고정 값)
            1, '1'
    과 같은 여러 형태일 때 전부 처리해주도록 한다
    생성시에만 사용한다
    """

    def __init__(self, model, pk_key='pk', **kwargs):
        """
        :param model: Model class
        :param pk_key: 외부에서 전달되는 데이터가 dict형일 경우, pk에 해당하는 key
        :param kwargs:
        """
        self.model = model
        self.pk_key = pk_key
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not isinstance(data, self.model):
            try:
                pk = data[self.pk_key]
            except Exception:
                pk = data
            return get_object_or_404(self.model, pk=pk)
        return data

    def to_representation(self, value):
        return f'{self.model.__class__.__name__} instance (pk: {self.pk})'
