from PySimultan2 import config
from PySimultan2.object_mapper import PythonMapper


def patch(user_manager):

    # from .method_mapper import method_mapper

    # user_manager.mapper_manager.create_mapping(mapper=config.get_default_mapper(),
    #                                            method_mapper=method_mapper)

    from nicegui import app

    class GlobalData:
        def __init__(self):
            self._data_model = None
            self._mapper = None

        @property
        def data_model(self):
            return self._data_model

        @data_model.setter
        def data_model(self, value):
            self._data_model = value

        @property
        def mapper(self):
            if self._mapper is None:
                self._mapper = PythonMapper()
            return self._mapper

        @mapper.setter
        def mapper(self, value):
            self._mapper = value

    global_data = GlobalData()

    def get_user_default_data_model(*args, **kwargs):
        try:
            return user_manager.users[app.storage.user['username']].data_model
        except Exception as e:
            return global_data.data_model

    def set_user_default_data_model(data_model, *args, **kwargs):
        try:
            user_manager.users[app.storage.user['username']].data_model = data_model
        except Exception as e:
            global_data.data_model = data_model

    def get_user_default_mapper(*args, **kwargs):
        try:
            return user_manager.users[app.storage.user['username']].mapper
        except Exception as e:
            return global_data.mapper

    def set_user_default_mapper(mapper, *args, **kwargs):
        try:
            user_manager.users[app.storage.user['username']].mapper = mapper
        except Exception as e:
            global_data.mapper = mapper

    config.get_default_data_model = get_user_default_data_model
    config.set_default_data_model = set_user_default_data_model

    config.get_default_mapper = get_user_default_mapper
    config.set_default_mapper = set_user_default_mapper
