import pytest

from src.uti_triagem import (
    criar_sistema_triagem_uti,
    avaliar_paciente,
)


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
