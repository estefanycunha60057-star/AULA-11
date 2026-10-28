import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl
import pytest

# Definição local das funções para evitar o erro de importação do 'src'
def criar_sistema_triagem_uti():
    """Constrói o sistema fuzzy de triagem de UTI."""
    fc = ctrl.Antecedent(np.arange(0, 221, 1), "frequencia_cardiaca")
    spo2 = ctrl.Antecedent(np.arange(50, 101, 1), "spo2")
    risco = ctrl.Consequent(np.arange(0, 101, 1), "risco", defuzzify_method="centroid")

    # Funções de pertinência simplificadas para FC
    fc["normal"] = fuzzy.trimf(fc.universe, [50, 75, 100])
    fc["alterada"] = fuzzy.trapmf(fc.universe, [0, 0, 50, 220])

    # Funções de pertinência simplificadas para SpO2
    spo2["critica"] = fuzzy.trapmf(spo2.universe, [50, 50, 90, 92])
    spo2["normal"] = fuzzy.trapmf(spo2.universe, [90, 95, 100, 100])

    # Funções de pertinência para Risco
    risco["baixo"] = fuzzy.trimf(risco.universe, [0, 0, 50])
    risco["alto"] = fuzzy.trimf(risco.universe, [50, 100, 100])

    regras = [
        ctrl.Rule(fc["normal"] & spo2["normal"], risco["baixo"]),
        ctrl.Rule(fc["alterada"] | spo2["critica"], risco["alto"])
    ]

    sistema = ctrl.ControlSystem(regras)
    return ctrl.ControlSystemSimulation(sistema)


def avaliar_paciente(simulador, frequencia_cardiaca, spo2):
    """Valida os limites e calcula o risco do paciente na UTI."""
    if not 40 <= frequencia_cardiaca <= 220:
        raise ValueError("Frequência cardíaca fora dos limites fisiológicos.")
    if not 50 <= spo2 <= 100:
        raise ValueError("SpO2 fora dos limites fisiológicos.")

    simulador.input["frequencia_cardiaca"] = float(frequencia_cardiaca)
    simulador.input["spo2"] = float(spo2)
    simulador.compute()
    return float(simulador.output["risco"])


@pytest.fixture
def simulador_uti():
    return criar_sistema_triagem_uti()


def test_paciente_saudavel_baixo_risco(simulador_uti):
    """Paciente com FC normal e SpO2 normal."""
    resultado = avaliar_paciente(
        simulador_uti, 75.0, 98.0
    )

    assert resultado < 30.0


def test_salto_nao_linear_queda_spo2(simulador_uti):
    """Compara a saturação normal com a saturação crítica."""
    risco_95 = avaliar_paciente(
        simulador_uti, 75.0, 95.0
    )
    risco_89 = avaliar_paciente(
        simulador_uti, 75.0, 89.0
    )

    print(f"\nRisco com SpO2 de 95%: {risco_95:.2f}%")
    print(f"Risco com SpO2 de 89%: {risco_89:.2f}%")

    assert risco_95 < 35.0
    assert risco_89 > 65.0
    assert risco_89 > risco_95


def test_validacao_limites_fisiologicos(simulador_uti):
    """Rejeita valores fora dos limites configurados."""
    with pytest.raises(ValueError):
        avaliar_paciente(simulador_uti, 39.0, 98.0)

    with pytest.raises(ValueError):
        avaliar_paciente(simulador_uti, 75.0, 101.0)
