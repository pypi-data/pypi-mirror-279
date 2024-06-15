# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring, missing-class-docstring, too-many-ancestors
from marshmallow import fields as f
from ...schema import BaseSchema
from . import models as m

class MixinUuid:
    """Mixin utilizado para lidar com casos em que id cloud é um uuid"""
    cloud_uuid = f.String(data_key='id')


class SystemSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        pass


class CampoAdicionalColunaSchema(MixinUuid, SystemSchema):
    class Meta(SystemSchema.Meta):
        model = m.CampoAdicionalColuna
        exclude = ('cloud_id',)

    titulo = f.String()
    texto_ajuda = f.String()
    formato = f.String()
    variavel = f.String()
    placeholder = f.String()
    obrigatorio = f.Boolean()
    configuracoes = f.Raw()


class CampoAdicionalAgrupadorSchema(MixinUuid, SystemSchema):
    class Meta(SystemSchema.Meta):
        model = m.CampoAdicionalAgrupador
        exclude = ('cloud_id',)

    titulo = f.String()
    campos = f.List(f.Nested(CampoAdicionalColunaSchema))


class CampoAdicionalSchema(MixinUuid, SystemSchema):
    class Meta(SystemSchema.Meta):
        model = m.CampoAdicional
        exclude = ('cloud_id',)

    descricao = f.String()
    tipo = f.String()
    agrupador = f.Nested(CampoAdicionalAgrupadorSchema)


class CargoSchema(SystemSchema):
    class Meta(SystemSchema.Meta):
        model = m.Cargo

    descricao = f.String()
    campos_adicionais = f.Raw()
    codigo_e_social = f.String()
    inicio_vigencia = f.DateTime()
    paga_decimo_terceiro_salario = f.Boolean()
    grau_instrucao = f.String()
    situacao_grau_instrucao = f.String()
    contagem_especial = f.String()
    acumulo_cargos = f.String()
    dedicacao_exclusiva = f.Boolean()
    extinto = f.Boolean()
    quantidade_vagas = f.Integer()
    quantidade_vagas_pcd = f.Integer()
    requisitos_necessarios = f.String()
    atividades_desempenhadas = f.String()
    unidade_pagamento = f.String()

    historicos = f.List(f.Nested(lambda: CargoSchema(exclude=('historicos',))))
