import time

import numpy as np
import pytest

from src.engine import (
    construir_motor_inferencia,
    executar_inferencia,
)


@pytest.fixture
def simulador():
    return construir_motor_inferencia()


def test_saida_dentro_do_universo(simulador):
    casos = [
        (0, 0),
        (50, 5),
        (100, 10),
        (30, 8),
        (80, 2),
    ]

    for impacto, explorabilidade in casos:
        resultado = executar_inferencia(
            simulador, impacto, explorabilidade
        )
        assert 0 <= resultado <= 100


def test_monotonicidade_impacto(simulador):
    explorabilidade = 5.0

    baixa = executar_inferencia(
        simulador, 20, explorabilidade
    )
    media = executar_inferencia(
        simulador, 50, explorabilidade
    )
    alta = executar_inferencia(
        simulador, 90, explorabilidade
    )

    assert baixa <= media <= alta


def test_entradas_invalidas_disparam_erro(simulador):
    with pytest.raises(ValueError):
        executar_inferencia(simulador, -10, 5)

    with pytest.raises(ValueError):
        executar_inferencia(simulador, 150, 5)

    with pytest.raises(ValueError):
        executar_inferencia(simulador, 50, 12)


def test_latencia_inferencia(simulador):
    rng = np.random.default_rng(42)

    # Aquecimento para reduzir o efeito da inicialização.
    executar_inferencia(simulador, 50, 5)

    inicio = time.perf_counter()

    for _ in range(100):
        impacto = float(rng.uniform(0, 100))
        explorabilidade = float(rng.uniform(0, 10))
        executar_inferencia(
            simulador, impacto, explorabilidade
        )

    tempo_total = time.perf_counter() - inicio
    tempo_medio_ms = tempo_total * 1000 / 100

    print(
        f"\nTempo médio por inferência: "
        f"{tempo_medio_ms:.3f} ms"
    )

    assert tempo_medio_ms < 10.0, (
        f"Inferência lenta: {tempo_medio_ms:.3f} ms/op"
    )
