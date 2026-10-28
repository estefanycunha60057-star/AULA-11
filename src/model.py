
import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl


def criar_modelo_fuzzy():
    """Cria o sistema fuzzy de avaliação de urgência."""

    impacto = ctrl.Antecedent(
        np.arange(0, 101, 1), "impacto"
    )
    explorabilidade = ctrl.Antecedent(
        np.arange(0, 11, 1), "explorabilidade"
    )
    urgencia = ctrl.Consequent(
        np.arange(0, 101, 1),
        "urgencia",
        defuzzify_method="centroid",
    )

    # Funções de pertinência do impacto
    impacto["baixo"] = fuzzy.trimf(
        impacto.universe, [0, 0, 50]
    )
    impacto["medio"] = fuzzy.trimf(
        impacto.universe, [25, 50, 75]
    )
    impacto["alto"] = fuzzy.trapmf(
        impacto.universe, [50, 75, 100, 100]
    )

    # Funções de pertinência da explorabilidade
    explorabilidade["baixa"] = fuzzy.trapmf(
        explorabilidade.universe, [0, 0, 3, 6]
    )
    explorabilidade["alta"] = fuzzy.trapmf(
        explorabilidade.universe, [4, 7, 10, 10]
    )

    # Funções de pertinência da urgência
    urgencia["baixa"] = fuzzy.trimf(
        urgencia.universe, [0, 0, 40]
    )
    urgencia["media"] = fuzzy.trimf(
        urgencia.universe, [25, 50, 75]
    )
    urgencia["alta"] = fuzzy.trapmf(
        urgencia.universe, [60, 80, 100, 100]
    )

    # Regras para cada nível de impacto e explorabilidade
    regras = [
        ctrl.Rule(
            impacto["baixo"] & explorabilidade["baixa"],
            urgencia["baixa"],
        ),
        ctrl.Rule(
            impacto["baixo"] & explorabilidade["alta"],
            urgencia["baixa"],
        ),
        ctrl.Rule(
            impacto["medio"] & explorabilidade["baixa"],
            urgencia["media"],
        ),
        ctrl.Rule(
            impacto["medio"] & explorabilidade["alta"],
            urgencia["media"],
        ),
        ctrl.Rule(
            impacto["alto"] & explorabilidade["baixa"],
            urgencia["alta"],
        ),
        ctrl.Rule(
            impacto["alto"] & explorabilidade["alta"],
            urgencia["alta"],
        ),
    ]

    return ctrl.ControlSystem(regras)
