# -*- coding: utf-8 -*-
from typing import Literal

LoteSituacao = Literal[
    'NULL',
    'AGENDADO',
    'EXECUTANDO',
    'SUCESSO',
    'ERRO',
    'PARCIAL'
]

ValidacaoErroTipo = Literal[
    'CAMPO_REQUERIDO_NULO',
    'VALOR_MONETARIO_NEGATIVO'
]
