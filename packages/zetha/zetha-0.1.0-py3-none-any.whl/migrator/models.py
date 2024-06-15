# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring
from typing import TYPE_CHECKING, Optional, Any
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint as Uq
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import object_session
from sqlalchemy.dialects.postgresql import JSONB

from requests import get

from . import enums as en
from .system import System
from ..columns import column, relationship, standard_fk
from ..base import standard_mapping
from ..methods import batch_list

if TYPE_CHECKING:
    from requests import Response

    from ..base import Betha
    from ..schema import BaseSchema


class Identifier(System):
    """Classe identificadora que se relaciona com uma entrada de qualquer tabela."""
    integracao_id: Mapped[UUID] = column(default_factory=uuid4, sort_order=-3, unique=True, init=False)
    row_id: Mapped[int] = column(BigInteger, sort_order=-2)
    row_tablename: Mapped[str] = column(sort_order=-2)
    row_schema: Mapped[str] = column(sort_order=-2)
    validado: Mapped[bool] = column(default=False) # Define se registro foi validado com sucesso
    migrado: Mapped[bool] = column(default=False) # Define se registro foi migrado com sucesso
    situacao: Mapped[Optional[str]] = column(default=None) # Situacao de acordo com response de lote

    validacao_id: Mapped[Optional[int]] = standard_fk('validacao')
    validacao: Mapped[Optional['Validacao']] = relationship(back_populates='identificador', default=None)

    lote_id: Mapped[Optional[int]] = standard_fk('lote')
    lote: Mapped[Optional['Lote']] = relationship(back_populates='identifiers', default=None)

    @property
    def row(self) -> Optional['Betha']:
        """Busca row referenciada em identificador"""
        model = standard_mapping.get_model(self.row_schema, self.row_tablename)
        return object_session(self).get(model, self.row_id) # type: ignore

    @classmethod
    def identify(cls, row: 'Betha'):
        row.identifier = cls(row_id=row.id, row_tablename=row.__tablename__, row_schema=row.SYSTEM)

    __table_args__ = (
        Uq('row_id', 'row_tablename', 'row_schema'),
    )


class Lote(System):
    api_id: Mapped[Optional[str]] = column()
    status_code: Mapped[Optional[int]] = column()
    response: Mapped[dict[str, Any]] = column(JSONB, default_factory=dict)
    situacao: Mapped[en.LoteSituacao] = column(default='NULL')

    identifiers: Mapped[list['Identifier']] = relationship(back_populates='lote', default_factory=list)

    def json(self, schema: 'BaseSchema') -> list[dict[str, Any]]:
        """Retorna dict de json com rows em lote"""
        return [
            {'idIntegracao': str(identifier.integracao_id), 'conteudo': schema.dump(identifier.row)}
            for identifier in self.identifiers
        ]
        
    def read_response(self, response: 'Response') -> None:
        self.status_code = response.status_code
        self.response = response.json()
        
    def get_lote(self, url_lote: str, headers: dict[str, str]) -> 'Response':
        if '{id}' not in url_lote:
            raise ValueError("Url informada deve conter o placeholder '{id}'")
        return get(url_lote.format(id=self.api_id), headers=headers)

    def update(self) -> None:
        if not self.response:
            raise ValueError('Lote precisa de json response anexado para validar situacao')

        situacao: Optional[str] = self.response.get('situacao')
        if situacao in {'AGENDADO', 'EXECUTANDO'}:
            self.situacao = situacao # type: ignore
            return

        retorno: list[dict[str, Any]] = self.response.get('retorno', [])
        retorno_size = len(retorno)
        retorno_executado_size = sum(1 for row in retorno if row.get('situacao') == 'EXECUTADO')

        if retorno_executado_size == 0:
            self.situacao = 'ERRO'
        elif retorno_executado_size == retorno_size:
            self.situacao = 'SUCESSO'
        else:
            self.situacao = 'PARCIAL'
    
    @classmethod
    def make_lotes(cls, indentifiers: list[Identifier], batch_size: int = 25):
        batched_identifiers = batch_list(indentifiers, batch_size)
        return [cls(identifiers=batch) for batch in batched_identifiers]


class Validacao(System):
    timestamp: Mapped[datetime] = column(default=datetime.now(), init=False)
    identificador: Mapped['Identifier'] = relationship()

    erros: Mapped[list["ValidacaoErro"]] = relationship()


class ValidacaoErro(System):
    tipo: Mapped[en.ValidacaoErroTipo] = column()
    descricao: Mapped[Optional[str]] = column()

    validacao_id: Mapped[int] = standard_fk('validacao')
    validacao: Mapped['Validacao'] = relationship(back_populates='erros')
