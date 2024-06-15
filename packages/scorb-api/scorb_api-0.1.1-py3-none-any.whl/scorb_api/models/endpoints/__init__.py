
from scorb_api.models.endpoints.entidade_customizadas import EntidadeCustomizada
from scorb_api.models.endpoints.globais import (
    ProjectorTemplate, ValidationConfiguration, AlcanceTipo, AtributoCustomizado, CenarioCampo, CenarioCategoria, Cenario, InventarioTemplate, ResumoHCeSalarioCCeEmpresa, TabelaCustomizadaGlobais
)
from scorb_api.models.endpoints.entidade_de_cenario import(
    AlcanceExcecao,
    CalculoAlcance,
    CalculoAlcanceVerbaDependencia,
    CenarioVisao,
    CentroCusto,
    CentroCustoVerbaValorReal,
    CheckCadeirasTotal,
    CheckCadeirasTotalPorVerba,
    ConsultaCadeiraFixo,
    ConsultaCentroDeCustoFixoNew,
    ConsultaCentroDeCustoFixoOld,
    ContaContabil,
    Cotacao,
    ExpressaoCustomizada,
    FaixaSalarialAlcance,
    FaixaSalarialEsquema,
    FaixaSalarialEsquemaItem,
    FaixaSalarialReajusteAlcance,
    FuncaoCustomizada,
    Funcionario,
    FuncionarioAlocacao,
    FuncionarioSalarioPrevisto,
    FuncionarioTipo,
    GrupoCargo,
    GrupoCentroCusto,
    GrupoEmpregado,
    GrupoNivelSalarial,
    GrupoVerba,
    Moeda,
    NivelSalarial,
    Plano,
    PlanoContas,
    Posicao,
    ReajusteAlcance,
    ReajusteAlcanceExcecao,
    ReajusteAlcanceMotivo,
    ReportCalculatedField,
    Verba,
    VerbaCategoria,
    VerbaCentroCustoDepara,
    VerbaContaContabilAlcance,
    VerbaReajusteContaContabil,
)
from scorb_api.models.endpoints.tabelas_customizadas import TabelaCustomizada

class Globais():
    def __init__(self, header_auth) -> None:
        self.header_auth = header_auth
    
    
    def alcance_tipo(self) -> AlcanceTipo:
        return AlcanceTipo(self.header_auth)
    
    def atributo_customizado(self) -> AtributoCustomizado:
        return AtributoCustomizado(self.header_auth)
    
    def cenario(self) -> Cenario:
        return Cenario(self.header_auth)
    
    def cenario_field(self) -> CenarioCampo:
        return CenarioCampo(self.header_auth)
    
    def cenario_category(self) -> CenarioCategoria:
        return CenarioCategoria(self.header_auth)
    
    def inventario_template(self) -> InventarioTemplate:
        return InventarioTemplate(self.header_auth)
    
    def projector_template(self) -> ProjectorTemplate:
        return ProjectorTemplate(self.header_auth)
    
    def tabela_customizada(self) -> TabelaCustomizadaGlobais:
        return TabelaCustomizadaGlobais(self.header_auth)
    
    def validation_configuration(self) -> ValidationConfiguration:
        return ValidationConfiguration(self.header_auth)
    
    def resumo_hc_e_salario_cc_e_empresa(self) -> ResumoHCeSalarioCCeEmpresa:
        return ResumoHCeSalarioCCeEmpresa(self.header_auth)

class EntidadesDeCenario():
    def __init__(self, header_auth) -> None:
        self.header_auth = header_auth
    
    def alcance_excecao(self, cenario_code) -> AlcanceExcecao:
        return AlcanceExcecao(self.header_auth, cenario_code)

    def calculo_alcance(self, cenario_code) -> CalculoAlcance:
        return CalculoAlcance(self.header_auth, cenario_code)

    def calculo_alcance_verba_dependencia(self, cenario_code) -> CalculoAlcanceVerbaDependencia:
        return CalculoAlcanceVerbaDependencia(self.header_auth, cenario_code)

    def cenario_visao(self, cenario_code) -> CenarioVisao:
        return CenarioVisao(self.header_auth, cenario_code)

    def centro_custo(self, cenario_code) -> CentroCusto:
        return CentroCusto(self.header_auth, cenario_code)
    
    def centro_custo_verba_valor_real(self, cenario_code) -> CentroCustoVerbaValorReal:
        return CentroCustoVerbaValorReal(self.header_auth, cenario_code)
    
    def check_caderias_total(self, cenario_code) -> CheckCadeirasTotal:
        return CheckCadeirasTotal(self.header_auth, cenario_code)
    
    def check_caderias_total_por_verba(self, cenario_code) -> CheckCadeirasTotalPorVerba:
        return CheckCadeirasTotalPorVerba(self.header_auth, cenario_code)
    
    def consulta_cadeira_fixo(self, cenario_code) -> ConsultaCadeiraFixo:
        return ConsultaCadeiraFixo(self.header_auth, cenario_code)
    
    def consulta_centro_de_custo_fixo_new(self, cenario_code) -> ConsultaCentroDeCustoFixoNew:
        return ConsultaCentroDeCustoFixoNew(self.header_auth, cenario_code)
    
    def consulta_centro_de_custo_fixo_old(self, cenario_code) -> ConsultaCentroDeCustoFixoOld:
        return ConsultaCentroDeCustoFixoOld(self.header_auth, cenario_code)

    def conta_contabil(self, cenario_code) -> ContaContabil:
        return ContaContabil(self.header_auth, cenario_code)
    
    def cotacao(self, cenario_code) -> Cotacao:
        return Cotacao(self.header_auth, cenario_code)
    
    def expressao_customizada(self, cenario_code) -> ExpressaoCustomizada:
        return ExpressaoCustomizada(self.header_auth, cenario_code)
    
    def faixa_salarial_alcance(self, cenario_code) -> FaixaSalarialAlcance:
        return FaixaSalarialAlcance(self.header_auth, cenario_code)
    
    def faixa_salarial_esquema(self, cenario_code) -> FaixaSalarialEsquema:
        return FaixaSalarialEsquema(self.header_auth, cenario_code)

    def faixa_salarial_esquema_item(self, cenario_code) -> FaixaSalarialEsquemaItem:
        return FaixaSalarialEsquemaItem(self.header_auth, cenario_code)

    def faixa_salarial_reajuste_alcance(self, cenario_code) -> FaixaSalarialReajusteAlcance:
        return FaixaSalarialReajusteAlcance(self.header_auth, cenario_code)

    def funcao_customizada(self, cenario_code) -> FuncaoCustomizada:
        return FuncaoCustomizada(self.header_auth, cenario_code)
    
    def funcionario(self, cenario_code) -> Funcionario:
        return Funcionario(self.header_auth, cenario_code)

    def funcionario_alocacao(self, cenario_code) -> FuncionarioAlocacao:
        return FuncionarioAlocacao(self.header_auth, cenario_code)

    def funcionario_salario_previsto(self, cenario_code) -> FuncionarioSalarioPrevisto:
        return FuncionarioSalarioPrevisto(self.header_auth, cenario_code)

    def funcionario_tipo(self, cenario_code) -> FuncionarioTipo:
        return FuncionarioTipo(self.header_auth, cenario_code)
    
    def grupo_cargo(self, cenario_code) -> GrupoCargo:
        return GrupoCargo(self.header_auth, cenario_code)
    
    def grupo_centro_custo(self, cenario_code) -> GrupoCentroCusto:
        return GrupoCentroCusto(self.header_auth, cenario_code)
    
    def grupo_empregado(self, cenario_code) -> GrupoEmpregado:
        return GrupoEmpregado(self.header_auth, cenario_code)
    
    def grupo_nivel_salarial(self, cenario_code) -> GrupoNivelSalarial:
        return GrupoNivelSalarial(self.header_auth, cenario_code)
    
    def grupo_verba(self, cenario_code) -> GrupoVerba:
        return GrupoVerba(self.header_auth, cenario_code)
    
    def moeda(self, cenario_code) -> Moeda:
        return Moeda(self.header_auth, cenario_code)
    
    def nivel_salarial(self, cenario_code) -> NivelSalarial:
        return NivelSalarial(self.header_auth, cenario_code)
    
    def plano(self, cenario_code) -> Plano:
        return Plano(self.header_auth, cenario_code)
    
    def plano_contas(self, cenario_code) -> PlanoContas:
        return PlanoContas(self.header_auth, cenario_code)
    
    def posicao(self, cenario_code) -> Posicao:
        return Posicao(self.header_auth, cenario_code)
    
    def reajuste_alcance(self, cenario_code) -> ReajusteAlcance:
        return ReajusteAlcance(self.header_auth, cenario_code)
    
    def reajuste_alcance_excecao(self, cenario_code) -> ReajusteAlcanceExcecao:
        return ReajusteAlcanceExcecao(self.header_auth, cenario_code)

    def reajuste_alcance_motivo(self, cenario_code) -> ReajusteAlcanceMotivo:
        return ReajusteAlcanceMotivo(self.header_auth, cenario_code)

    def reajuste_alcance_excecao(self, cenario_code) -> ReajusteAlcanceMotivo:
        return ReajusteAlcanceMotivo(self.header_auth, cenario_code)
    
    def report_calculated_field(self, cenario_code) -> ReportCalculatedField:
        return ReportCalculatedField(self.header_auth, cenario_code)
    
    def verba(self, cenario_code) -> Verba:
        return Verba(self.header_auth, cenario_code)
    
    def verba_categoria(self, cenario_code) -> VerbaCategoria:
        return VerbaCategoria(self.header_auth, cenario_code)
    
    def verba_centro_custo_depara(self, cenario_code) -> VerbaCentroCustoDepara:
        return VerbaCentroCustoDepara(self.header_auth, cenario_code)
    
    def verba_conta_contabil_alcance(self, cenario_code) -> VerbaContaContabilAlcance:
        return VerbaContaContabilAlcance(self.header_auth, cenario_code)
    
    def verba_reajuste_conta_contabil(self, cenario_code) -> VerbaReajusteContaContabil:
        return VerbaReajusteContaContabil(self.header_auth, cenario_code)

class EntidadesCustomizadas():
    def __init__(self, header_auth) -> None:
        self.header_auth = header_auth
    
    def entidade_customizada(self, cenario_code, custom):
        return EntidadeCustomizada(header_auth=self.header_auth, cenario_code=cenario_code, custom=custom)

class TabelasCustomizadas():
    def __init__(self, header_auth) -> None:
        self.header_auth = header_auth

    def tabela_customizada(self, cenario_code, custom):
        return TabelaCustomizada(header_auth=self.header_auth, cenario_code=cenario_code, custom=custom)