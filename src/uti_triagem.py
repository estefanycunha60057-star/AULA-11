import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl


def criar_sistema_triagem_uti():
    """Cria o sistema fuzzy para triagem de pacientes em UTI."""

    # 1. Definição das entradas e da saída
    freq_cardiaca = ctrl.Antecedent(
        np.arange(40, 161, 1), "freq_cardiaca"
    )

    spo2 = ctrl.Antecedent(
        np.arange(70, 100.1, 0.1), "spo2"
    )

    risco = ctrl.Consequent(
        np.arange(0, 101, 1),
        "risco",
        defuzzify_method="centroid"
    )

    # 2. Funções de pertinência da frequência cardíaca
    freq_cardiaca["bradicardia"] = fuzzy.trimf(
        freq_cardiaca.universe, [40, 40, 60]
    )

    freq_cardiaca["normal"] = fuzzy.trimf(
        freq_cardiaca.universe, [50, 75, 100]
    )

    freq_cardiaca["taquicardia"] = fuzzy.trapmf(
        freq_cardiaca.universe, [90, 110, 160, 160]
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

    # 5. Regras clínicas da atividade
    r1 = ctrl.Rule(
        spo2["critica"],
        risco["critico"]
    )

    r2 = ctrl.Rule(
        freq_cardiaca["bradicardia"] & spo2["limitrofe"],
        risco["critico"]
    )

    r3 = ctrl.Rule(
        freq_cardiaca["taquicardia"] & spo2["limitrofe"],
        risco["critico"]
    )

    r4 = ctrl.Rule(
        freq_cardiaca["normal"] & spo2["limitrofe"],
        risco["moderado"]
    )

    r5 = ctrl.Rule(
        freq_cardiaca["normal"] & spo2["normal"],
        risco["baixo"]
    )

    # 6. Compilação do sistema fuzzy
    sistema = ctrl.ControlSystem([r1, r2, r3, r4, r5])

    return ctrl.ControlSystemSimulation(sistema)


def avaliar_paciente(simulador, bpm, spo2_val):
    """Valida os sinais vitais e calcula o risco fuzzy."""

    if not 40 <= bpm <= 160:
        raise ValueError(
            "A frequência cardíaca deve estar entre 40 e 160 bpm."
        )

    if not 70 <= spo2_val <= 100:
        raise ValueError(
            "A saturação de oxigênio deve estar entre 70% e 100%."
        )

    simulador.input["freq_cardiaca"] = float(bpm)
    simulador.input["spo2"] = float(spo2_val)

    simulador.compute()

    return float(simulador.output["risco"])


if __name__ == "__main__":
    simulador = criar_sistema_triagem_uti()

    print("Sistema de triagem de UTI iniciado.")

    for bpm, saturacao in [(75, 98), (75, 95), (75, 89)]:
        try:
            risco_calculado = avaliar_paciente(
                simulador, bpm, saturacao
            )

            print(
                f"FC: {bpm} bpm | "
                f"SpO2: {saturacao}% | "
                f"Risco: {risco_calculado:.2f}%"
            )

        except ValueError as erro:
            print(f"Erro: {erro}")
