from david8.core.base_params import BaseParams


class NumericParamStyle(BaseParams):
    def _render_param(self, key: str) -> str:
        return f'${key}'

    def get_parameters(self) -> list:
        return list(self._params_bag.values())


class QMarkParamStyle(BaseParams):
    def _render_param(self, key: str) -> str:
        return '?'

    def get_parameters(self) -> list:
        return list(self._params_bag.values())


class FormatParamStyle(BaseParams):
    def _render_param(self, key: str) -> str:
        return '%s'

    def get_parameters(self) -> tuple:
        return tuple(self._params_bag.values())


class NamedParamStyle(BaseParams):
    def _render_param(self, key: str) -> str:
        return f':p{key}'

    def get_parameters(self) -> dict:
        return {
            f'p{key}': value
            for key, value in self._params_bag.items()
        }


class PyFormatParamStyle(BaseParams):
    def _render_param(self, key: str) -> str:
        return f'%(p{key})s'

    def get_parameters(self) -> dict:
        return {
            f'p{key}': value
            for key, value in self._params_bag.items()
        }
