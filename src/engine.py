
from skfuzzy import control as ctrl

from src.model import criar_modelo_fuzzy


def construir_motor_inferencia():
    """Cria uma instância do motor de inferência fuzzy."""
    sistema = criar_modelo_fuzzy()
    return ctrl.ControlSystemSimulation(sistema)


def executar_inferencia(simulador, impacto, explorabilidade):
    """Executa a inferência após validar as entradas."""

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
