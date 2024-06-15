# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring, too-many-ancestors
from typing import Optional, Any
from decimal import Decimal
from datetime import date, datetime
from collections import defaultdict
#from uuid import UUID

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, MappedAsDataclass
from sqlalchemy.dialects.postgresql import JSONB

#from jsonpath_ng import jsonpath, parse

from . import enums as en
from ...base import Betha
from ...columns import Num12to4, column, relationship, standard_fk
from ... import mixins as mx


class CamposAdicionais(MappedAsDataclass):
    campos_adicionais: Mapped[list[dict[str, Any]]] = column(JSONB, default_factory=list, repr=False)
    
    def flatten_campos(self) -> None:
        campos_flattened: list[dict[str, Any]] = []

        for agrupador in self.campos_adicionais:
            tipo = agrupador['tipo']
            identificador = agrupador['identificador']

            for campo in agrupador['campos']:
                campos_flattened.append({
                    'tipo': tipo,
                    'identificador': identificador,
                    'id': campo['id'],
                    'valor': campo['valor']
                })
        self.campos_adicionais = campos_flattened

    def group_campos(self) -> None:
        campos_grouped: dict[tuple[str, str], dict[str, Any]] = defaultdict(lambda: {'campos': []})

        for campo in self.campos_adicionais:
            identificador = campo['identificador']
            tipo = campo['tipo']

            key = (identificador, tipo,)

            campos_grouped[key]['identificador'] = identificador
            campos_grouped[key]['tipo'] = tipo
            campos_grouped[key]['campos'].append({
                'id': campo['id'],
                'valor': campo['valor']
            })
        self.campos_adicionais = [value for _, value in campos_grouped.items()]


class System(Betha):
    "Classe abstrata de sistema Folha"
    __abstract__ = True
    SYSTEM = 'folha'
    _BASE_URL = 'https://pessoal.betha.cloud/service-layer/v1/api/'

# TODO: Adicionar docstrings para cada modelo denotando caminho em sistema e descricao de tabela

class Ato(System):
    _PATH = 'ato'

    data_criacao: Mapped[Optional[date]] = column()
    data_publicacao: Mapped[Optional[date]] = column()
    data_resolucao: Mapped[Optional[date]] = column()
    data_vigorar: Mapped[Optional[date]] = column()
    numero_diario_oficial: Mapped[Optional[int]] = column()
    ementa: Mapped[Optional[str]] = column()
    numero_oficial: Mapped[Optional[str]] = column()

    tipo_id: Mapped[Optional[int]] = standard_fk('tipo_ato')
    tipo: Mapped['TipoAto'] = relationship()
    # fontes_divulgacao: Mapped[list['FontesDivulgacao']] = relationship(default_factory=list)


class CalculoFolha(System):
    _PATH = 'calculo-folha'

    conversao: Mapped[Optional[bool]] = column()
    data_agendamento: Mapped[Optional[date]] = column()
    data_pagamento: Mapped[Optional[date]] = column()
    tipo_vinculacao_matricula: Mapped[Optional[str]] = column()

    tipo_processamento: Mapped[Optional[en.FolhaTipoProcessamento]] = column()
    sub_tipo_processamento: Mapped[Optional[en.FolhaSubTipoProcessamento]] = column()

    folhas: Mapped[list["Folha"]] = relationship(back_populates='calculo_folha', default_factory=list)


class CampoAdicional(System, mx.Uuid):
    """Cadastro/Configuracao de campo adicional"""
    _PATH = 'campo-adicional'

    descricao: Mapped[str] = column()
    tipo: Mapped[str] = column()

    agrupador: Mapped['CampoAdicionalAgrupador'] = relationship(
        back_populates='configuracao',
        cascade='all, delete-orphan',
        default=None
    )


class CampoAdicionalAgrupador(System, mx.Uuid):
    titulo: Mapped[str] = column()

    configuracao_id: Mapped[int] = standard_fk('campo_adicional')
    configuracao: Mapped['CampoAdicional'] = relationship(back_populates='agrupador', default=None)

    campos: Mapped[list['CampoAdicionalColuna']] = relationship(
        back_populates='agrupador',
        cascade='all, delete-orphan',
        default_factory=list
    )


class CampoAdicionalColuna(System, mx.Uuid):
    ordem: Mapped[Optional[int]] = column()
    obrigatorio: Mapped[bool] = column(default=False)
    configuracoes: Mapped[Optional[dict[str, Any]]] = column(JSONB)
    placeholder: Mapped[Optional[str]] = column()
    texto_ajuda: Mapped[Optional[str]] = column()
    titulo: Mapped[str] = column()
    variavel: Mapped[str] = column()

    formato: Mapped[Optional[en.CampoAdicionalFormato]] = column()

    agrupador_id: Mapped[int] = standard_fk('campo_adicional_agrupador')
    agrupador: Mapped['CampoAdicionalAgrupador'] = relationship(back_populates='campos')


class Cargo(System, CamposAdicionais):
    """
    Tabela representa cargos em sistema Betha.
    Configurando -> Cargos e Salários -> Cargos
    """
    _PATH = 'cargo'

    id: Mapped[int] = System.id
    dedicacao_exclusiva: Mapped[Optional[bool]] = column()
    extinto: Mapped[Optional[bool]] = column()
    paga_decimo_terceiro_salario: Mapped[Optional[bool]] = column()
    inicio_vigencia: Mapped[Optional[datetime]] = column()
    quantidade_vagas: Mapped[int] = column(default=0)
    quantidade_vagas_pcd: Mapped[int] = column(default=0)
    atividades_desempenhadas: Mapped[Optional[str]] = column()
    codigo_e_social: Mapped[Optional[str]] = column()
    descricao: Mapped[Optional[str]] = column()
    requisitos_necessarios: Mapped[Optional[str]] = column()

    acumulo_cargos: Mapped[Optional[Optional[en.CargoAcumuloCargos]]] = column()
    contagem_especial: Mapped[Optional[Optional[en.CargoContagemEspecial]]] = column()
    grau_instrucao: Mapped[Optional[Optional[en.CargoGrauInstrucao]]] = column()
    situacao_grau_instrucao: Mapped[Optional[Optional[en.CargoSituacaoGrauInstrucao]]] = column()
    unidade_pagamento: Mapped[Optional[Optional[en.CargoUnidadePagamento]]] = column()

    origem_id: Mapped[Optional[int]] = standard_fk('cargo')
    origem: Mapped[Optional['Cargo']] = relationship(remote_side=[id], back_populates='historicos')
    historicos: Mapped[list['Cargo']] =  relationship(back_populates='origem', default_factory=list)

    ato_id: Mapped[int] = standard_fk('ato')
    ato: Mapped['Ato'] = relationship()

    # cbo_id: Mapped[int] = standard_fk('cbo')
    # cbo: Mapped['Cbo'] = relationship()

    # configuracao_ferias_id: Mapped[int] = standard_fk('configuracao_ferias')
    # configuracao_ferias: Mapped['ConfiguracaoFerias'] = relationship()

    # configuracao_licenca_premio_id: Mapped[int] = standard_fk('configuracao_licenca_premio')
    # configuracao_licenca_premio: Mapped['ConfiguracaoLicencaPremio'] = relationship()

    # quadro_cargos_id: Mapped[int] = standard_fk('quadro_cargos')
    # quadro_cargos: Mapped['QuadroCargos'] = relationship()

    # tipo_id: Mapped[int] = standard_fk('tipo')
    # tipo: Mapped['Tipo'] = relationship()

    # areas_atuacao: Mapped[list['AreasAtuacao']] = relationship(default_factory=list)
    # cursos: Mapped[list['Cursos']] = relationship(default_factory=list)
    # organogramas: Mapped[list['Organogramas']] = relationship(default_factory=list)
    # planos_previdencia: Mapped[list['PlanosPrevidencia']] = relationship(default_factory=list)
    # remuneracoes: Mapped[list['Remuneracoes']] = relationship(default_factory=list)
    # tipos_diaria: Mapped[list['TiposDiaria']] = relationship(default_factory=list)
    # vinculos_empregaticios: Mapped[list['VinculosEmpregaticios']] = relationship(default_factory=list)


class ConcursoProcessoSeletivo(System):
    _PATH = 'concurso-processo-seletivo'

    convocacao: Mapped[Optional[bool]] = column()
    data_avaliacao: Mapped[Optional[date]] = column()
    data_encerramento: Mapped[Optional[date]] = column()
    data_final_inscricao: Mapped[Optional[date]] = column()
    data_final_inscricao_isentos: Mapped[Optional[date]] = column()
    data_homologacao: Mapped[Optional[date]] = column()
    data_inicial_inscricao: Mapped[Optional[date]] = column()
    data_inicial_inscricao_isento: Mapped[Optional[date]] = column()
    data_prorrogacao: Mapped[Optional[date]] = column()
    data_prorrogacao_inscricao_isentos: Mapped[Optional[date]] = column()
    data_prorrogacao_validade: Mapped[Optional[date]] = column()
    data_validade: Mapped[Optional[date]] = column()
    ano_concurso: Mapped[Optional[int]] = column()
    descricao: Mapped[Optional[str]] = column()
    numero_edital: Mapped[Optional[str]] = column()
    observacao: Mapped[Optional[str]] = column()

    processo: Mapped[Optional[en.ConcursoProcessoSeletivoProcesso]] = column()
    regime_juridico: Mapped[Optional[en.ConcursoProcessoSeletivoRegimeJuridico]] = column()
    responsavel_execucao: Mapped[Optional[en.ConcursoProcessoSeletivoResponsavelExecucao]] = column()
    situacao_concurso_processo_seletivo: Mapped[Optional[en.ConcursoProcessoSeletivoSituacaoConcursoProcessoSeletivo]] = column()
    tipo_avaliacao: Mapped[Optional[en.ConcursoProcessoSeletivoTipoAvaliacao]] = column()
    tipo_processo_avaliacao: Mapped[Optional[en.ConcursoProcessoSeletivoTipoProcessoAvaliacao]] = column()
    tipo_recrutamento: Mapped[Optional[en.ConcursoProcessoSeletivoTipoRecrutamento]] = column()

    # ato_contratacao_temporaria_id: Mapped[int] = standard_fk('ato_contratacao_temporaria')
    # ato_contratacao_temporaria: Mapped['AtoContratacaoTemporaria'] = relationship()

    # ato_inscricao_id: Mapped[int] = standard_fk('ato_inscricao')
    # ato_inscricao: Mapped['AtoInscricao'] = relationship()

    # ato_inscricao_isentos_id: Mapped[int] = standard_fk('ato_inscricao_isentos')
    # ato_inscricao_isentos: Mapped['AtoInscricaoIsentos'] = relationship()

    # configuracao_recrutamento_id: Mapped[int] = standard_fk('configuracao_recrutamento')
    # configuracao_recrutamento: Mapped['ConfiguracaoRecrutamento'] = relationship()

    # contrato_id: Mapped[int] = standard_fk('contrato')
    # contrato: Mapped['Contrato'] = relationship()

    # executor_recrutamento_id: Mapped[int] = standard_fk('executor_recrutamento')
    # executor_recrutamento: Mapped['ExecutorRecrutamento'] = relationship()

    # cargos: Mapped[list['Cargos']] = relationship(default_factory=list)
    # comissoes_avaliacao: Mapped[list['ComissoesAvaliacao']] = relationship(default_factory=list)
    # concurso_processo_seletivo_avaliacoes: Mapped[list['ConcursoProcessoSeletivoAvaliacoes']] = relationship(default_factory=list)
    # editais: Mapped[list['Editais']] = relationship(default_factory=list)


class ConfiguracaoEvento(System):
    _PATH = 'configuracao-evento'

    codigo: Mapped[Optional[int]] = column(BigInteger)
    descricao: Mapped[Optional[str]] = column()
    inicio_vigencia: Mapped[Optional[datetime]] = column()
    tipo: Mapped[Optional[en.ConfiguracaoEventoTipo]] = column()
    classificacao: Mapped[Optional[en.ConfiguracaoEventoClassificacao]] = column()

    eventos: Mapped[list["FolhaEvento"]] = relationship(back_populates='configuracao', default_factory=list)
    composicao_bases: Mapped[list["FolhaComposicaoBase"]] = relationship(
        back_populates='configuracao_evento',
        default_factory=list
    )


class FolhaComposicaoBase(System):
    folha_id: Mapped[Optional[int]] = standard_fk('folha')
    base_id: Mapped[Optional[int]] = standard_fk('tipo_base')
    valor: Mapped[Decimal] = column()

    folha: Mapped["Folha"] = relationship(back_populates='composicao_bases', default=None)
    base: Mapped["TipoBase"] = relationship(default=None)

    configuracao_evento_id: Mapped[int] = standard_fk('configuracao_evento')
    configuracao_evento: Mapped["ConfiguracaoEvento"] = relationship(back_populates='composicao_bases', default=None)


class FolhaEvento(System):
    """Objeto que reprenta eventos de folha em sistema Betha"""
    tipo: Mapped[Optional[en.ConfiguracaoEventoTipo]] = column()
    referencia: Mapped[Optional[Num12to4]] = column()
    valor: Mapped[Optional[Decimal]] = column()
    classificacao: Mapped[Optional[en.ConfiguracaoEventoClassificacao]] = column()
    lancamento_variavel: Mapped[bool] = column(default=False)

    folha_id: Mapped[int] = standard_fk('folha')
    folha: Mapped["Folha"] = relationship(back_populates='eventos', default=None)

    configuracao_id: Mapped[int] = standard_fk('configuracao_evento')
    configuracao: Mapped["ConfiguracaoEvento"] = relationship(back_populates='eventos', default=None)


class Folha(System):
    """Objeto que representa folhas/remuneracoes em sistema Betha."""
    _PATH = 'folha'

    tipo_processamento: Mapped[Optional[en.FolhaTipoProcessamento]] = column()
    sub_tipo_processamento: Mapped[Optional[en.FolhaSubTipoProcessamento]] = column()
    competencia: Mapped[Optional[str]] = column()
    folha_pagamento: Mapped[Optional[bool]] = column()
    total_bruto: Mapped[Optional[Decimal]] = column()
    total_desconto: Mapped[Optional[Decimal]] = column()
    total_liquido: Mapped[Optional[Decimal]] = column()
    data_fechamento: Mapped[Optional[date]] = column()
    data_pagamento: Mapped[Optional[date]] = column()
    data_liberacao: Mapped[Optional[date]] = column()
    data_calculo: Mapped[Optional[date]] = column()
    situacao: Mapped[Optional[en.FolhaSituacao]] = column()
    identificador_folha_de_pagamento: Mapped[Optional[str]] = column()
    pagamento_anterior: Mapped[Optional[int]] = column(BigInteger)
    pagamento_anterior_parcela: Mapped[Optional[int]] = column(BigInteger)
    quantidade_meses_rra: Mapped[Optional[Decimal]] = column()
    enviar_remuneracoes_e_social: Mapped[bool] = column(default=False)
    enviar_pagamentos_e_social: Mapped[bool] = column(default=False)

    matricula_id: Mapped[int] = standard_fk('matricula')
    matricula: Mapped['Matricula'] = relationship(back_populates='folhas', default=None)

    calculo_folha_id: Mapped[int] = standard_fk('calculo_folha')
    calculo_folha: Mapped['CalculoFolha'] = relationship(back_populates='folhas', default=None)

    eventos: Mapped[list['FolhaEvento']] = relationship(back_populates='folha', default=None)
    composicao_bases: Mapped[list['FolhaComposicaoBase']] = relationship(back_populates='folha', default_factory=list)


class GrupoFuncional(System):
    pass


class Matricula(System):
    area_atuacao_alterada: Mapped[Optional[bool]] = column()
    beneficio_concedido_decisao_judicial: Mapped[Optional[bool]] = column()
    cargo_alterado: Mapped[Optional[bool]] = column()
    cargo_comissionado_adicionado: Mapped[Optional[bool]] = column()
    clausula_assecuratoria_contrato_temporario: Mapped[Optional[bool]] = column()
    compensa_horas: Mapped[Optional[bool]] = column()
    conselheiro_tutelar: Mapped[Optional[bool]] = column()
    controla_horas_manual: Mapped[Optional[bool]] = column()
    controla_per_aquis_ferias_antes_admissao: Mapped[Optional[bool]] = column()
    enviar_esocial: Mapped[Optional[bool]] = column()
    estagio_obrigatorio: Mapped[Optional[bool]] = column()
    gera_registro_preliminar: Mapped[Optional[bool]] = column()
    jornada_parcial: Mapped[Optional[bool]] = column()
    ocupa_vaga: Mapped[Optional[bool]] = column()
    ocupa_vaga_comissionado: Mapped[Optional[bool]] = column()
    optante_fgts: Mapped[Optional[bool]] = column()
    outra_origem: Mapped[Optional[bool]] = column()
    possui_seguro_vida: Mapped[Optional[bool]] = column()
    previdencia_federal: Mapped[Optional[bool]] = column()
    primeiro_emprego: Mapped[Optional[bool]] = column()
    profissional_saude_seguranca_publica: Mapped[Optional[bool]] = column()
    recebe_abono_permanencia: Mapped[Optional[bool]] = column()
    recebe_decimo_terceiro: Mapped[Optional[bool]] = column()
    registra_ponto: Mapped[Optional[bool]] = column()
    salario_alterado: Mapped[Optional[bool]] = column()
    salario_comissionado_alterado: Mapped[Optional[bool]] = column()
    data_admissao_origem: Mapped[Optional[date]] = column()
    data_admissao_retificada_proc_trab: Mapped[Optional[date]] = column()
    data_agendamento_rescisao: Mapped[Optional[date]] = column()
    data_alteracao_salario_esocial: Mapped[Optional[date]] = column()
    data_base: Mapped[Optional[date]] = column()
    data_final: Mapped[Optional[date]] = column()
    data_inicial_periodo_aquisitivo_ferias_antes_admissao: Mapped[Optional[date]] = column()
    data_inicio_contrato: Mapped[Optional[date]] = column()
    data_nomeacao: Mapped[Optional[date]] = column()
    data_obito: Mapped[Optional[date]] = column()
    data_opcao: Mapped[Optional[date]] = column()
    data_posse: Mapped[Optional[date]] = column()
    data_prorrogacao: Mapped[Optional[date]] = column()
    data_prorrogacao_contrato_temporario: Mapped[Optional[date]] = column()
    data_saida_cargo_comissionado: Mapped[Optional[date]] = column()
    data_termino_contrato_temporario: Mapped[Optional[date]] = column()
    data_transferencia: Mapped[Optional[date]] = column()
    inicio_abono_permanencia: Mapped[Optional[date]] = column()
    inicio_turno_corrido: Mapped[Optional[date]] = column()
    inicio_vigencia: Mapped[Optional[datetime]] = column()
    quantidade_horas_mes: Mapped[Optional[Decimal]] = column()
    rendimento_mensal: Mapped[Optional[Decimal]] = column()
    salario_comissionado: Mapped[Optional[Decimal]] = column()
    entidade_origem: Mapped[Optional[int]] = column()
    quantidade_horas_semana: Mapped[Optional[int]] = column()
    cnpj_entidade_qualificadora: Mapped[Optional[str]] = column()
    conta_fgts: Mapped[Optional[str]] = column()
    cpf_matricula_origem: Mapped[Optional[str]] = column()
    descricao_beneficio: Mapped[Optional[str]] = column()
    descricao_salario: Mapped[Optional[str]] = column()
    e_social: Mapped[Optional[str]] = column()
    matricula_empresa_origem: Mapped[Optional[str]] = column()
    motivo_contrato_temporario: Mapped[Optional[str]] = column()
    n_processo_trabalhista: Mapped[Optional[str]] = column()
    numero_apolice_seguro_vida: Mapped[Optional[str]] = column()
    numero_beneficio: Mapped[Optional[str]] = column()
    numero_beneficio_anterior: Mapped[Optional[str]] = column()
    numero_cartao_ponto: Mapped[Optional[str]] = column()
    numero_contrato: Mapped[Optional[str]] = column()
    objetivo: Mapped[Optional[str]] = column()
    observacao: Mapped[Optional[str]] = column()
    observacao_contrato: Mapped[Optional[str]] = column()

    # controle_jornada: Mapped['MatriculaControleJornada'] = column()
    # duracao_beneficio: Mapped['MatriculaDuracaoBeneficio'] = column()
    # formacao_fase: Mapped['MatriculaFormacaoFase'] = column()
    # formacao_periodo: Mapped['MatriculaFormacaoPeriodo'] = column()
    # forma_pagamento: Mapped['MatriculaFormaPagamento'] = column()
    # hipotese_legal_contrato_temporario: Mapped['MatriculaHipoteseLegalContratoTemporario'] = column()
    # indicativo_admissao: Mapped['MatriculaIndicativoAdmissao'] = column()
    # indicativo_provimento: Mapped['MatriculaIndicativoProvimento'] = column()
    # motivo_inicio_beneficio: Mapped['MatriculaMotivoInicioBeneficio'] = column()
    # natureza_atividade: Mapped['MatriculaNaturezaAtividade'] = column()
    # ocorrencia_sefip: Mapped['MatriculaOcorrenciaSefip'] = column()
    # origem_concurso: Mapped['MatriculaOrigemConcurso'] = column()
    # origem_salario: Mapped['MatriculaOrigemSalario'] = column()
    # prazo_determinado_contrato_temporario: Mapped['MatriculaPrazoDeterminadoContratoTemporario'] = column()
    # situacao: Mapped['MatriculaSituacao'] = column()
    # situacao_beneficio: Mapped['MatriculaSituacaoBeneficio'] = column()
    # tempo_aposentadoria: Mapped['MatriculaTempoAposentadoria'] = column()
    # tipo: Mapped['MatriculaTipo'] = column()
    # tipo_admissao: Mapped['MatriculaTipoAdmissao'] = column()
    # tipo_contratacao_aprendiz: Mapped['MatriculaTipoContratacaoAprendiz'] = column()
    # tipo_contrato_parcial: Mapped['MatriculaTipoContratoParcial'] = column()
    # tipo_de_beneficio: Mapped['MatriculaTipoDeBeneficio'] = column()
    # tipo_inclusao_contrato_temporario: Mapped['MatriculaTipoInclusaoContratoTemporario'] = column()
    # tipo_provimento: Mapped['MatriculaTipoProvimento'] = column()
    # unidade_pagamento: Mapped['MatriculaUnidadePagamento'] = column()

    # ato_contrato_id: Mapped[int] = standard_fk('ato')
    # ato_contrato: Mapped['Ato'] = relationship()

    # ato_alteracao_salario_id: Mapped[int] = standard_fk('ato')
    # ato_alteracao_salario: Mapped['Ato'] = relationship()

    # conta_bancaria_pagamento_id: Mapped[int] = standard_fk('conta_bancaria')
    # conta_bancaria_pagamento: Mapped['ContaBancaria'] = relationship()

    # pessoa_id: Mapped[int] = standard_fk('pessoa')
    # pessoa: Mapped['Pessoa'] = relationship()

    # grupo_funcional_id: Mapped[int] = standard_fk('grupo_funcional')
    # grupo_funcional: Mapped['GrupoFuncional'] = relationship()

    # jornada_trabalho_id: Mapped[int] = standard_fk('jornada_trabalho')
    # jornada_trabalho: Mapped['JornadaTrabalho'] = relationship()

    # motivo_alteracao_salario_id: Mapped[int] = standard_fk('motivo_alteracao_salario')
    # motivo_alteracao_salario: Mapped['MotivoAlteracaoSalario'] = relationship()

    # organograma_id: Mapped[int] = standard_fk('organograma')
    # organograma: Mapped['Organograma'] = relationship()

    # processo_trabalhista_id: Mapped[int] = standard_fk('processo_trabalhista')
    # processo_trabalhista: Mapped['ProcessoTrabalhista'] = relationship()

    # rescisao_id: Mapped[int] = standard_fk('rescisao')
    # rescisao: Mapped['Rescisao'] = relationship()

    # vinculo_empregaticio_id: Mapped[int] = standard_fk('vinculo_empregaticio')
    # vinculo_empregaticio: Mapped['VinculoEmpregaticio'] = relationship()

    folhas: Mapped[list['Folha']] = relationship(default_factory=list)
    # funcoes_gratificadas: Mapped[list['FuncoesGratificadas']] = relationship(default_factory=list)
    # historicos: Mapped[list['Historicos']] = relationship(default_factory=list)
    # lotacoes_fisicas: Mapped[list['LotacoesFisicas']] = relationship(default_factory=list)
    # matricula_licencas_premio: Mapped[list['MatriculaLicencasPremio']] = relationship(default_factory=list)
    # matriculas_adicionais: Mapped[list['MatriculasAdicionais']] = relationship(default_factory=list)
    # previdencias: Mapped[list['Previdencias']] = relationship(default_factory=list)
    # reintegracoes: Mapped[list['Reintegracoes']] = relationship(default_factory=list)
    # responsaveis: Mapped[list['Responsaveis']] = relationship(default_factory=list)


class Pessoa(System):
    _PATH = 'pessoa'


class TipoAto(System):
    _PATH = 'tipo-ato'
    descricao: Mapped[Optional[str]] = column()
    classificacao: Mapped[Optional[en.TipoAtoClassificacao]] = column()


class TipoBase(System):
    _PATH = 'base'

    descricao: Mapped[Optional[str]] = column()
    sigla: Mapped[Optional[str]] = column()
    classificacao_base_calculo: Mapped[Optional[en.TipoBaseClassificacao]] = column()
