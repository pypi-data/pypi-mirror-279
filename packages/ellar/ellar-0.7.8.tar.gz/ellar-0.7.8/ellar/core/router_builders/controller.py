import inspect
import typing as t

from ellar.common.constants import (
    CONTROLLER_METADATA,
    CONTROLLER_OPERATION_HANDLER_KEY,
    CONTROLLER_WATERMARK,
    OPERATION_ENDPOINT_KEY,
    ROUTE_OPERATION_PARAMETERS,
)
from ellar.common.logging import logger
from ellar.common.models import ControllerBase, ControllerType
from ellar.common.operations import RouteParameters, WsRouteParameters
from ellar.core.routing import (
    ControllerRouteOperation,
    ControllerWebsocketRouteOperation,
    EllarMount,
    RouteCollection,
)
from ellar.reflect import reflect
from starlette.routing import BaseRoute, Router

from .base import RouterBuilder


class ControllerRouterBuilder(RouterBuilder, controller_type=type(ControllerBase)):
    @classmethod
    def _get_route_functions(
        cls,
        klass: t.Type,
    ) -> t.Iterable[t.Callable]:
        for _method_name, method in inspect.getmembers(
            klass, predicate=inspect.isfunction
        ):
            if hasattr(method, OPERATION_ENDPOINT_KEY):
                yield method

    @classmethod
    def _process_controller_routes(
        cls, controller: t.Type[ControllerBase]
    ) -> t.Sequence[BaseRoute]:
        res = []

        if reflect.get_metadata(CONTROLLER_METADATA.PROCESSED, controller):
            return (
                reflect.get_metadata(CONTROLLER_OPERATION_HANDLER_KEY, controller) or []
            )

        for item in cls._get_route_functions(controller):
            parameters = item.__dict__[ROUTE_OPERATION_PARAMETERS]
            operation: t.Union[
                ControllerRouteOperation, ControllerWebsocketRouteOperation
            ]

            if not isinstance(parameters, list):
                parameters = [parameters]

            for parameter in parameters:
                if isinstance(parameter, RouteParameters):
                    operation = ControllerRouteOperation(controller, **parameter.dict())
                elif isinstance(parameter, WsRouteParameters):
                    operation = ControllerWebsocketRouteOperation(
                        controller, **parameter.dict()
                    )
                else:  # pragma: no cover
                    logger.warning(
                        f"Parameter type is not recognized. {type(parameter) if not isinstance(parameter, type) else parameter}"
                    )
                    continue

                reflect.define_metadata(
                    CONTROLLER_OPERATION_HANDLER_KEY,
                    [operation],
                    controller,
                )
                res.append(operation)
        reflect.define_metadata(CONTROLLER_METADATA.PROCESSED, True, controller)
        return res

    @classmethod
    def build(
        cls, controller_type: t.Union[t.Type[ControllerBase], t.Any], **kwargs: t.Any
    ) -> EllarMount:
        routes = cls._process_controller_routes(controller_type)

        app = Router()
        app.routes = RouteCollection(routes)  # type:ignore

        include_in_schema = reflect.get_metadata_or_raise_exception(
            CONTROLLER_METADATA.INCLUDE_IN_SCHEMA, controller_type
        )

        middleware = reflect.get_metadata(
            CONTROLLER_METADATA.MIDDLEWARE, controller_type
        )

        kwargs.setdefault("middleware", middleware)
        router = EllarMount(
            app=app,
            path=reflect.get_metadata_or_raise_exception(
                CONTROLLER_METADATA.PATH, controller_type
            ),
            name=reflect.get_metadata_or_raise_exception(
                CONTROLLER_METADATA.NAME, controller_type
            ),
            include_in_schema=include_in_schema
            if include_in_schema is not None
            else True,
            control_type=controller_type,
            **kwargs,
        )
        return router

    @classmethod
    def check_type(cls, controller_type: t.Union[t.Type, t.Any]) -> None:
        assert reflect.get_metadata(
            CONTROLLER_WATERMARK, controller_type
        ) and isinstance(controller_type, ControllerType), "Invalid Controller Type."
