import typing as t
from inspect import isabstract

from injector import (
    AssistedBuilder,
    Binding,
    SingletonScope,
    UnsatisfiedRequirement,
    _is_specialization,
)
from injector import (
    Binder as InjectorBinder,
)
from injector import (
    Module as InjectorModule,
)
from injector import NoScope as TransientScope
from injector import Scope as InjectorScope

from ..providers import Provider
from ..scopes import (
    RequestScope,
    ScopeDecorator,
)
from ..service_config import get_scope, is_decorated_with_injectable

if t.TYPE_CHECKING:  # pragma: no cover
    from ellar.core.modules import ModuleBase

    from .ellar_injector import EllarInjector

NOT_SET = object()


class Container(InjectorBinder):
    __slots__ = (
        "injector",
        "_auto_bind",
        "_bindings",
        "_bindings_by_tag",
        "parent",
        "_aliases",
        "_exact_aliases",
    )

    injector: "EllarInjector"

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)
        self._bindings_by_tag: t.Dict[str, t.Type[t.Any]] = {}

    @t.no_type_check
    def create_binding(
        self,
        interface: t.Type,
        to: t.Any = None,
        scope: t.Union[ScopeDecorator, t.Type[InjectorScope]] = None,
    ) -> Binding:
        provider = self.provider_for(interface, to)
        scope = scope or get_scope(to or interface) or TransientScope
        if isinstance(scope, ScopeDecorator):
            scope = scope.scope
        return Binding(interface, provider, scope)

    def get_binding(self, interface: t.Type) -> t.Tuple[Binding, InjectorBinder]:
        is_scope = isinstance(interface, type) and issubclass(interface, InjectorScope)
        is_assisted_builder = _is_specialization(interface, AssistedBuilder)
        try:
            return self._get_binding(
                interface, only_this_binder=is_scope or is_assisted_builder
            )
        except (KeyError, UnsatisfiedRequirement):
            if is_scope:
                scope = interface
                self.bind(scope, to=scope(self.injector))
                return self._get_binding(interface)
            # The special interface is added here so that requesting a special
            # interface with auto_bind disabled works
            if (
                self._auto_bind
                or self._is_special_interface(interface)
                or is_decorated_with_injectable(interface)
            ):
                binding = self.create_binding(interface)
                self._bindings[interface] = binding
                return binding, self

        raise UnsatisfiedRequirement(None, interface)

    def get_interface_by_tag(self, tag: str) -> t.Type[t.Any]:
        interface = self._bindings_by_tag.get(tag)
        if interface:
            return interface
        if isinstance(self.parent, Container):
            return self.parent.get_interface_by_tag(tag)

        raise UnsatisfiedRequirement(None, t.cast(t.Any, tag))

    def register_binding(
        self, interface: t.Type, binding: Binding, tag: t.Optional[str] = None
    ) -> None:
        self._bindings[interface] = binding

        if tag:
            self._bindings_by_tag[tag] = interface

    @t.no_type_check
    def register(
        self,
        base_type: t.Type,
        concrete_type: t.Union[t.Type, t.Any] = None,
        scope: t.Union[t.Type[InjectorScope], ScopeDecorator] = None,
        tag: t.Optional[str] = None,
    ) -> None:
        try:
            if concrete_type and isinstance(concrete_type, type):
                assert issubclass(concrete_type, base_type), (
                    f"Cannot register {base_type.__name__} for abstract class "
                    f"{concrete_type.__name__}"
                )
        except TypeError:  # pragma: no cover
            # ignore generic types issues
            pass

        provider = self.provider_for(base_type, concrete_type)

        _scope: t.Any = scope or NOT_SET

        if _scope is NOT_SET and isinstance(concrete_type, type):
            _scope = get_scope(concrete_type) or TransientScope
        elif _scope is NOT_SET:
            _scope = get_scope(base_type) or TransientScope

        if isinstance(_scope, ScopeDecorator):
            _scope = _scope.scope

        self.register_binding(base_type, Binding(base_type, provider, _scope), tag=tag)

    def register_instance(
        self,
        instance: t.Any,
        concrete_type: t.Optional[t.Union[t.Type, Provider]] = None,
        tag: t.Optional[str] = None,
    ) -> None:
        assert not isinstance(instance, type)
        _concrete_type = instance.__class__ if not concrete_type else concrete_type
        self.register(_concrete_type, instance, scope=SingletonScope, tag=tag)

    def register_singleton(
        self,
        base_type: t.Type,
        concrete_type: t.Union[t.Type, t.Any, Provider] = None,
        tag: t.Optional[str] = None,
    ) -> None:
        """

        :param base_type:
        :param concrete_type:
        :return:
        """
        if not concrete_type:
            self.register_exact_singleton(base_type, tag=tag)
        self.register(base_type, concrete_type, scope=SingletonScope, tag=tag)

    def register_transient(
        self,
        base_type: t.Type,
        concrete_type: t.Optional[t.Union[t.Type, Provider]] = None,
        tag: t.Optional[str] = None,
    ) -> None:
        """

        :param base_type:
        :param concrete_type:
        :return:
        """
        if not concrete_type:
            self.register_exact_transient(base_type, tag=tag)
        self.register(base_type, concrete_type, scope=TransientScope, tag=tag)

    def register_scoped(
        self,
        base_type: t.Type,
        concrete_type: t.Optional[t.Union[t.Type, Provider]] = None,
        tag: t.Optional[str] = None,
    ) -> None:
        """

        :param base_type:
        :param concrete_type:
        :return:
        """
        if not concrete_type:
            self.register_exact_scoped(base_type, tag=tag)
        self.register(base_type, concrete_type, scope=RequestScope, tag=tag)

    def register_exact_singleton(
        self, concrete_type: t.Type, tag: t.Optional[str] = None
    ) -> None:
        """

        :param concrete_type:
        :return:
        """
        assert not isabstract(concrete_type)
        self.register(base_type=concrete_type, scope=SingletonScope, tag=tag)

    def register_exact_transient(
        self, concrete_type: t.Type, tag: t.Optional[str] = None
    ) -> None:
        """

        :param concrete_type:
        :return:
        """
        assert not isabstract(concrete_type)
        self.register(base_type=concrete_type, scope=TransientScope, tag=tag)

    def register_exact_scoped(
        self, concrete_type: t.Type, tag: t.Optional[str] = None
    ) -> None:
        """

        :param concrete_type:
        :return:
        """
        assert not isabstract(concrete_type)
        self.register(base_type=concrete_type, scope=RequestScope, tag=tag)

    @t.no_type_check
    def install(
        self,
        module: t.Union[t.Type["ModuleBase"], "ModuleBase"],
        **init_kwargs: t.Any,
    ) -> t.Union[InjectorModule, "ModuleBase"]:
        # TODO: move install core to application module
        #   create a ModuleWrapper with init_kwargs

        """Install a module into this container[binder].

        In this context the module is one of the following:

        * function taking the :class:`Container` as it's only parameter

          ::

            def configure(container):
                bind(str, to='s')

            container.install(configure)

        * instance of :class:`Module` (instance of it's subclass counts)

          ::

            class MyModule(StarletteAPIModuleBase):
                def register_services(self, container):
                    container.bind(str, to='s')

            container.install(MyModule())

        * subclass of :class:`Module` - the subclass needs to be instantiable so if it
          expects any parameters they need to be injected

          ::

            container.install(MyModule)
        """

        instance = t.cast(t.Union[t.Type["ModuleBase"], "ModuleBase"], module)

        if isinstance(instance, type) and issubclass(
            t.cast(type, instance), InjectorModule
        ):
            instance = t.cast(type, instance)(**init_kwargs)
        elif isinstance(instance, type):
            return self.injector.get(instance)
        elif not isinstance(instance, type) and not isinstance(
            instance, InjectorModule
        ):
            return instance

        instance(self)
        return instance
