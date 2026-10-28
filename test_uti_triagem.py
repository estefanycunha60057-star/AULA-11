import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl


def criar_sistema_triagem_uti():
    """Cria o sistema fuzzy de classificação de risco clínico da UTI."""

    # 1. Universos de discurso
    fc = ctrl.Antecedent(
        np.arange(40, 161, 1),
        "frequencia_cardiaca"
    )

    spo2 = ctrl.Antecedent(
        np.arange(70, 101, 1),
        "saturacao_oxigenio"
    )

    risco = ctrl.Consequent(
        np.arange(0, 101, 1),
        "risco",
        defuzzify_method="centroid"
    )

    # 2. Funções de pertinência da frequência cardíaca
    fc["bradicardia"] = fuzzy.trimf(
        fc.universe, [40, 40, 60]
    )

    fc["normal"] = fuzzy.trimf(
        fc.universe, [50, 75, 100]
    )

    fc["taquicardia"] = fuzzy.trapmf(
        fc.universe, [90, 110, 160, 160]
    )

    # 3. Funções de pertinência da saturação de oxigênio
    spo2["critica"] = fuzzy.trapmf(
        spo2.universe, [70, 70, 88, 91]
    )

    spo2["limitrofe"] = fuzzy.trimf(
        spo2.universe, [89, 93, 96]
    )

    spo2["normal"] = fuzzy.trapmf(
        spo2.universe, [94, 97, 100, 100]
    )

    # 4. Funções de pertinência do risco clínico
    risco["baixo"] = fuzzy.trimf(
        risco.universe, [0, 0, 35]
    )

    risco["moderado"] = fuzzy.trimf(
        risco.universe, [25, 50, 75]
    )

    risco["critico"] = fuzzy.trapmf(
        risco.universe, [65, 85, 100, 100]
    )

    # 5. Regras clínicas especificadas no enunciado
    r1 = ctrl.Rule(
        spo2["critica"],
        risco["critico"]
    )

    r2 = ctrl.Rule(
        fc["bradicardia"] & spo2["limitrofe"],
        risco["critico"]
    )

    r3 = ctrl.Rule(
        fc["taquicardia"] & spo2["limitrofe"],
        risco["critico"]
    )

    r4 = ctrl.Rule(
        fc["normal"] & spo2["limitrofe"],
        risco["moderado"]
    )

    r5 = ctrl.Rule(
        fc["normal"] & spo2["normal"],
        risco["baixo"]
    )

    sistema = ctrl.ControlSystem([r1, r2, r3, r4, r5])

    return ctrl.ControlSystemSimulation(sistema)


def avaliar_paciente(simulador, fc_valor, spo2_valor):
    """Valida os sinais vitais e calcula o risco clínico."""

    if not 40 <= fc_valor <= 160:
        raise ValueError(
            "Frequência cardíaca deve estar entre 40 e 160 bpm."
        )

    if not 70 <= spo2_valor <= 100:
        raise ValueError(
            "SpO2 deve estar entre 70% e 100%."
        )

    simulador.input["frequencia_cardiaca"] = fc_valor
    simulador.input["saturacao_oxigenio"] = spo2_valor

    simulador.compute()

    return simulador.output["risco"]


if __name__ == "__main__":
    simulador = criar_sistema_triagem_uti()

    print("Sistema de triagem de UTI iniciado.")

    for fc_valor, spo2_valor in [
        (75, 98),
        (75, 95),
        (75, 89),
    ]:
        resultado = avaliar_paciente(
            simulador, fc_valor, spo2_valor
        )

        print(
            f"FC: {fc_valor} bpm | "
            f"SpO2: {spo2_valor}% | "
            f"Risco: {resultado:.2f}%"
        )
