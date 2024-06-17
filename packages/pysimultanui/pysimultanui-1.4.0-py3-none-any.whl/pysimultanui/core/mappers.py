import importlib
from nicegui import ui
from PySimultan2.object_mapper import PythonMapper
from .method_mapper import MethodMapper


from typing import TYPE_CHECKING, Any, Optional
if TYPE_CHECKING:
    from .user import User
    from ..views.detail_views import DetailView


class ViewManager:

    def __init__(self, *args, **kwargs):
        self.views: dict[str, 'DetailView'] = {}

    def add_view(self,
                 taxonomy_entry_key: str,
                 view: 'DetailView'):
        self.views[taxonomy_entry_key] = view


class Mapping:

    def __init__(self,
                 user: 'User',
                 mapper: 'PythonMapper',
                 method_mapper: 'MethodMapper',
                 view_manager: 'ViewManager' = None,
                 name: str = 'Mapping'):

        self.name: str = name
        self.mapper: 'PythonMapper' = mapper
        self.method_mapper: 'MethodMapper' = method_mapper
        if self.method_mapper.mapper is None:
            self.method_mapper.mapper = self.mapper

        self.view_manager: ViewManager = view_manager if view_manager is not None else ViewManager()
        self.user: 'User' = user

    def create_mapped_classes(self, *args, **kwargs):
        _ = [self.mapper.get_mapped_class(x) for x in self.mapper.registered_classes.keys()]

    def copy(self, user: 'User'):

        new_method_mapper = self.method_mapper.copy()
        new_mapper = new_method_mapper.mapper.copy()
        new_mapper.method_mapper = new_method_mapper
        new_mapper.clear()

        _ = [new_mapper.get_mapped_class(x) for x in new_mapper.registered_classes.keys()]

        return Mapping(mapper=new_mapper,
                       user=user,
                       method_mapper=new_method_mapper,
                       view_manager=self.view_manager,
                       name=self.name)


class MapperManager:

    def __init__(self,
                 available_mappings: dict[str: Mapping] = None,
                 mappings: dict['User': list[Mapping]] = None) -> None:

        self.available_mappings: dict[str: Mapping] = available_mappings if available_mappings is not None else {}
        self.mappings: dict['User':
                            list[Mapping]] = mappings if mappings is not None else {}

        self.create_mapping(name='Default')

    def create_mapping(self,
                       name: str = 'Mapping',
                       user: 'User' = None,
                       mapper: 'PythonMapper' = None,
                       method_mapper: 'MethodMapper' = None,
                       view_manager: ViewManager = None) -> Mapping:

        if name in self.available_mappings:
            ui.notify(f'Mapping with name {name} already exists')
            raise ValueError(f'Mapping with name {name} already exists')

        if mapper is None:
            mapper = PythonMapper()
            _ = [mapper.get_mapped_class(x) for x in mapper.registered_classes.keys()]

        if method_mapper is None:
            method_mapper = MethodMapper(mapper=mapper)

        mapping = Mapping(mapper=mapper,
                          user=user,
                          name=name,
                          method_mapper=method_mapper,
                          view_manager=view_manager
                          )

        self.available_mappings[name] = mapping
        return mapping

    def get_mapping(self,
                    user: 'User',
                    name: str,
                    load_undefined: bool = True
                    ) -> Mapping:

        """
        Get a mapping for a user by name. If the mapping does not exist, create it.
        :param user:
        :param name:
        :param load_undefined: load undefined components
        :return:
        """

        if name is None:
            return None

        if self.mappings.get(user, None) is None:
            self.mappings[user] = {}

        if self.mappings[user].get(name) is None:
            self.mappings[user][name] = self.available_mappings[name].copy(user=user)

        mapping = self.mappings[user][name]
        mapping.mapper.load_undefined = load_undefined

        _ = [mapping.mapper.get_mapped_class(x) for x in mapping.mapper.registered_classes.keys()]

        return mapping

    def get_mapper(self,
                   user: 'User',
                   name: str) -> 'PythonMapper':

        if self.mappings.get(user, None) is None:
            self.mappings[user] = {}

        if self.mappings[user].get(name) is None:
            self.mappings[user][name] = self.available_mappings[name].copy(user=user)

        return self.mappings[user][name].mapper

    def get_method_mapper(self,
                          user: 'User',
                          name: str) -> 'MethodMapper':

            if self.mappings.get(user, None) is None:
                self.mappings[user] = {}

            if self.mappings[user].get(name) is None:
                self.mappings[user][name] = self.available_mappings[name].copy(user=user)

            return self.mappings[user][name].method_mapper

    def get_view_manager(self, name: str) -> ViewManager:
        return self.available_mappings[name].view_manager

    def set_mapper(self,
                   user: 'User',
                   name: str,
                   mapper: 'PythonMapper') -> None:
        self.mappings[user][name].mapper = mapper
        mapper.method_mapper = self.mappings[user][name].method_mapper

    def add_package(self,
                    package: str,
                    user: 'User') -> None:
        try:
            new_package = importlib.import_module(package)
        except ImportError as e:
            ui.notify(f'Could not import package {package}. Trying to install it.')
            try:
                import pip
                pip.main(['install', package])
                new_package = importlib.import_module(package)
            except Exception as e:
                ui.notify(f'Could not install package {package}: {e}')
                return

        self.create_mapping(name=package,
                            mapper=getattr(new_package, 'mapper', None),
                            method_mapper=getattr(new_package, 'method_mapper', None),
                            view_manager=getattr(new_package, 'view_manager', None)
                            )

        if user.tool_select is not None:
            options = list(user.available_mappings.keys()) if user is not None else []
            options.sort()
            user.tool_select.set_options(options)

        user.logger.info(f'Added package {package}')
        ui.notify(f'Added package {package}')


# class MapperSelectDialog(ui.dialog):
#
#     def __init__(self, user=None) -> None:
#         super().__init__()
#         self._user = None
#
#         with self, ui.card():
#             ui.label('Select Toolbox:')
#             self.select = ui.select(options=list(self.user.available_mappings.keys()) if self.user is not None else [],
#                                     value=self.user.selected_mapper if self.user is not None else None,).classes('w-full')
#
#             with ui.checkbox('Load undefined components',
#                              value=True) as self.load_undefined:
#                 ui.tooltip('Load components that are not defined in the mapping')
#
#             with ui.row():
#                 ui.button('OK', on_click=self.select_mapper)
#                 ui.button('Cancel', on_click=self.cancel)
#
#         self.user = user
#
#     @property
#     def user(self) -> 'User':
#         return self._user
#
#     @user.setter
#     def user(self, value: 'User') -> None:
#         self._user = value
#         if self.user is not None:
#             self.select.options = list(self.user.available_mappings.keys())
#             self.select.value = self.user.selected_mapper
#         else:
#             self.select.options = []
#             self.select.value = None
#
#     def select_mapper(self, *args, **kwargs):
#
#         mapper = self.user.mapper_manager.get_mapping(self.user, self.select.value)
#         mapper.load_undefined = self.load_undefined.value
#         self.user.selected_mapper = self.select.value
#         self.user.project_manager.refresh_all_items()
#         ui.notify(f'Selected mapper: {self.user.selected_mapper}')
#         self.close()
#
#     def cancel(self, *args, **kwargs):
#         self.close()
#
#     def open(self, *args, **kwargs):
#         super().open(*args, **kwargs)


class MapperDropdown(ui.select):

    def __init__(
            self,
            user: 'User',
            *args,
            **kwargs,
    ) -> None:
        self._user = None

        # options = list(self.user.available_mappings.keys()) if self.user is not None else [],
        # value = self.user.selected_mapper if self.user is not None else None

        super().__init__(options=[],
                         on_change=self.mapper_changed,
                         *args,
                         **kwargs)

        self.user = user

    @property
    def user(self) -> 'User':
        return self._user

    @user.setter
    def user(self, value: 'User') -> None:
        self._user = value
        options = list(self.user.available_mappings.keys()) if self.user is not None else []
        options.sort()
        self.set_options(options)
        self.value = self.user.selected_mapper if self.user is not None else None

    def mapper_changed(self, *args, **kwargs):
        try:
            self.user.selected_mapper = self.value
            self.user.project_manager.refresh_all_items()
            ui.notify(f'Selected mapper: {self.user.selected_mapper}')
        except Exception as e:
            ui.notify(f'Error: {e}')


class AddPackageDialog(ui.dialog):

    def __init__(self, user=None) -> None:
        super().__init__()
        self._user = None

        with self, ui.card():
            ui.label('Add Toolbox')
            self.package_input = ui.input(placeholder='Package name').classes('w-full')
            with ui.row():
                ui.button('OK', on_click=self.ok)
                ui.button('Cancel', on_click=self.cancel)

        self.user = user

    def ok(self, *args, **kwargs):
        package_name = self.package_input.value
        self.user.mapper_manager.add_package(package_name,
                                             self.user)
        self.close()

    def cancel(self, *args, **kwargs):
        self.close()

    def open(self, *args, **kwargs):
        super().open(*args, **kwargs)
