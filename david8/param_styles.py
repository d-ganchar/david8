from david8.core.base_params import BaseParams


class NumericParamStyle(BaseParams):
    def _render_param(self, param_index: str) -> str:
        return f'${param_index}'


class QMarkParamStyle(BaseParams):
    def _render_param(self, param_index: str) -> str:
        return '?'


class FormatParamStyle(BaseParams):
    def _render_param(self, param_index: str) -> str:
        return '%s'


class NamedParamStyle(BaseParams):
    def _render_param(self, param_index: str) -> str:
        return f':p{param_index}'

    def _create_param_key(self, param_index: str) -> str:
        return f'p{param_index}'


class PyFormatParamStyle(BaseParams):
    def _render_param(self, param_index: str) -> str:
        return f'%(p{param_index})s'

    def _create_param_key(self, param_index: str) -> str:
        return f'p{param_index}'
