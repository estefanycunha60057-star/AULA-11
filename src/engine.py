import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl


def criar_sistema_fuzzy():
    """Constrói o sistema fuzzy de urgência."""
    impacto = ctrl.Antecedent(
        np.arange(0, 101, 1), "impacto"
    )
    explorabilidade = ctrl.Antecedent(
        np.arange(0, 10.1, 0.1), "explorabilidade"
    )
    urgencia = ctrl.Consequent(
        np.arange(0, 101, 1), "urgencia",
        defuzzify_method="centroid"
    )

    # Funções de pertinência do impacto
    impacto["baixo"] = fuzzy.trimf(
        impacto.universe, [0, 0, 50]
    )
    impacto["medio"] = fuzzy.trimf(
        impacto.universe, [25, 50, 75]
    )
    impacto["alto"] = fuzzy.trimf(
        impacto.universe, [50, 100, 100]
    )

    # Funções de pertinência da explorabilidade
    explorabilidade["baixa"] = fuzzy.trimf(
        explorabilidade.universe, [0, 0, 5]
    )
    explorabilidade["media"] = fuzzy.trimf(
        explorabilidade.universe, [2.5, 5, 7.5]
    )
    explorabilidade["alta"] = fuzzy.trimf(
        explorabilidade.universe, [5, 10, 10]
    )

    # Funções de pertinência da urgência
    urgencia["baixa"] = fuzzy.trimf(
        urgencia.universe, [0, 0, 50]
    )
    urgencia["media"] = fuzzy.trimf(
        urgencia.universe, [25, 50, 75]
    )
    urgencia["alta"] = fuzzy.trimf(
        urgencia.universe, [50, 100, 100]
    )

    regras = []

    for termo_exp in ("baixa", "media", "alta"):
        regras.append(
            ctrl.Rule(
                impacto["baixo"] & explorabilidade[termo_exp],
                urgencia["baixa"]
            )
        )
        regras.append(
            ctrl.Rule(
                impacto["medio"] & explorabilidade[termo_exp],
                urgencia["media"]
            )
        )
        regras.append(
            ctrl.Rule(
                impacto["alto"] & explorabilidade[termo_exp],
                urgencia["alta"]
            )
        )

    sistema = ctrl.ControlSystem(regras)
    return sistema


def construir_motor_inferencia():
    """Cria uma simulação independente do motor fuzzy."""
    sistema = criar_sistema_fuzzy()
    return ctrl.ControlSystemSimulation(sistema)


def executar_inferencia(simulador, impacto, explorabilidade):
    """Valida entradas e calcula a urgência."""
    if not 0 <= impacto <= 100:
        raise ValueError(
            f"Impacto fora da escala [0, 100]: {impacto}"
        )

    if not 0 <= explorabilidade <= 10:
        raise ValueError(
            "Explorabilidade fora da escala [0, 10]: "
            f"{explorabilidade}"
        )

    simulador.input["impacto"] = float(impacto)
    simulador.input["explorabilidade"] = float(explorabilidade)
    simulador.compute()

    return float(simulador.output["urgencia"])
