AULA 11 — VALIDAÇÃO EXPERIMENTAL E FECHAMENTO DA AC-3
Sprint 3 — Suíte de Testes Automatizados com Pytest

Disciplina: Projeto TECH
Atividade: Aula 11 — AC-3, Etapa 3 (Final)
Objetivo: Validar o motor de inferência fuzzy por meio de testes de limites, monotonicidade, tratamento de exceções e desempenho, além de implementar e testar um sistema de triagem de UTI.

1. Estrutura dos arquivos do projeto

Arquivos utilizados:

src/__init__.py
src/engine.py
src/model.py
src/uti_triagem.py
test_fuzzy_engine.py
test_uti_triagem.py
AULA_11/resultados_aula11_ciao.md
2. Motor fuzzy — Primeira execução sem erros

Comando executado:

bash
python -m pytest -v test_fuzzy_engine.py


Resultado completo:

text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

============================== 4 passed in 1.05s ===============================


Conclusão: os quatro testes passaram, validando o intervalo de saída, a monotonicidade, o tratamento de entradas inválidas e o desempenho do motor fuzzy.

3. Motor fuzzy — Segunda execução com erro proposital

Foi inserido um erro intencional no teste de intervalo de saída, substituindo a condição original por assert resultado < 0.

Comando executado:

bash
python -m pytest -v test_fuzzy_engine.py


Resultado completo:

text
Erro proposital inserido com sucesso.
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo FAILED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

=================================== FAILURES ===================================
________________________ test_saida_dentro_do_universo _________________________

simulador = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7b3d95654980>

    def test_saida_dentro_do_universo(simulador):
        casos = [(0, 0), (50, 5), (100, 10), (30, 8), (80, 2)]
        for imp, exp in casos:
            resultado = executar_inferencia(simulador, imp, exp)
>           assert resultado < 0  # ERRO PROPOSITAL
E           assert 16.666666666666664 < 0

test_fuzzy_engine.py:54: AssertionError

=========================== short test summary info ============================
FAILED test_fuzzy_engine.py::test_saida_dentro_do_universo
========================= 1 failed, 3 passed in 1.37s ==========================


Conclusão: o Pytest identificou a falha proposital. Um teste falhou e três passaram, demonstrando que a suíte detectou a condição inválida.

4. Motor fuzzy — Terceira execução após a correção

O erro proposital foi removido e a asserção original foi restaurada.

Comando executado:

bash
python -m pytest -v test_fuzzy_engine.py


Resultado completo:

text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

============================== 4 passed in 1.21s ===============================


Conclusão: após a correção, os quatro testes passaram.

5. Teste de desempenho e latência

Comando executado:

bash
python -m pytest -s test_fuzzy_engine.py

Primeira medição
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
collected 4 items

test_fuzzy_engine.py ...
Tempo medio por inferencia: 1.322 ms
.

============================== 4 passed in 1.27s ===============================

Segunda medição
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
collected 4 items

test_fuzzy_engine.py ...
Tempo médio por inferência: 3.549 ms
.

============================== 4 passed in 1.46s ===============================

Terceira medição
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
collected 4 items

test_fuzzy_engine.py ...
Tempo médio por inferência: 2.438 ms
PASSED

============================== 4 passed in 1.25s ===============================


Análise do desempenho:

Execução	Tempo médio por inferência	Resultado
1ª medição	1,322 ms	Aprovado
2ª medição	3,549 ms	Aprovado
3ª medição	2,438 ms	Aprovado

O limite definido no teste é inferior a 10 ms por inferência. Todas as medições registradas ficaram abaixo desse limite.

Os valores correspondem a execuções distintas e podem variar conforme o ambiente.

6. Triagem de UTI — Resultados iniciais com falhas

Comando executado:

bash
python -m pytest -v test_uti_triagem.py


Resultado completo registrado:

text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
collected 3 items

test_uti_triagem.py::test_paciente_saudavel_baixo_risco FAILED           [ 33%]
test_uti_triagem.py::test_salto_nao_linear_queda_spo2 FAILED             [ 66%]
test_uti_triagem.py::test_validacao_limites_fisiologicos PASSED          [100%]

=================================== FAILURES ===================================
______________________ test_paciente_saudavel_baixo_risco ______________________

simulador_uti = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7a456eb986e0>

    def test_paciente_saudavel_baixo_risco(simulador_uti):
        resultado = avaliar_paciente(simulador_uti, 75.0, 98.0)
>       assert resultado < 30.0
E       assert 50.81006575787557 < 30.0

test_uti_triagem.py:49: AssertionError

_______________________ test_salto_nao_linear_queda_spo2 _______________________

simulador_uti = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7a456ecebc50>

    def test_salto_nao_linear_queda_spo2(simulador_uti):
        risco_95 = avaliar_paciente(simulador_uti, 75.0, 95.0)
        risco_89 = avaliar_paciente(simulador_uti, 75.0, 89.0)
>       assert risco_95 < 35.0
E       assert 50.81006575787557 < 35.0

test_uti_triagem.py:54: AssertionError

=========================== short test summary info ============================
FAILED test_uti_triagem.py::test_paciente_saudavel_baixo_risco
FAILED test_uti_triagem.py::test_salto_nao_linear_queda_spo2
========================= 2 failed, 1 passed in 1.07s ==========================

Repetição das falhas

Em outra execução, foram registrados os mesmos dois testes com falha e o teste de validação fisiológica aprovado:

text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
collected 3 items

test_uti_triagem.py::test_paciente_saudavel_baixo_risco FAILED
test_uti_triagem.py::test_salto_nao_linear_queda_spo2 FAILED
test_uti_triagem.py::test_validacao_limites_fisiologicos PASSED

========================= 2 failed, 1 passed in 1.14s ==========================


Análise: os resultados iniciais não atenderam aos limites definidos para os cenários de baixo risco e queda da saturação. O teste de validação de entradas inválidas passou.

Esses registros representam a versão inicial, anterior aos ajustes.

7. Triagem de UTI — Simulação manual

Saída registrada no console:

text
Sistema de triagem de UTI iniciado.
FC: 75 bpm | SpO2: 98% | Risco: 11.67%
FC: 75 bpm | SpO2: 95% | Risco: 35.71%
FC: 75 bpm | SpO2: 89% | Risco: 85.57%


Interpretação: a simulação registrou risco de 11,67% para saturação de 98%, 35,71% para saturação de 95% e 85,57% para saturação de 89%.

A queda da saturação de 95% para 89% produziu um aumento expressivo no risco calculado, demonstrando o comportamento não linear desejado no modelo.

Esses números são resultados de simulação acadêmica e não devem ser utilizados isoladamente para decisões clínicas reais.

8. Triagem de UTI — Execução após os ajustes

Após os ajustes no sistema e nos testes, foi registrada a execução abaixo.

Comando executado:

bash
python -m pytest -v test_uti_triagem.py


Resultado completo:

text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
collected 3 items

test_uti_triagem.py::test_paciente_saudavel_baixo_risco PASSED           [ 33%]
test_uti_triagem.py::test_salto_nao_linear_queda_spo2 PASSED             [ 66%]
test_uti_triagem.py::test_validacao_limites_fisiologicos PASSED          [100%]

============================== 3 passed in 1.01s ===============================


Conclusão: os três testes da triagem de UTI passaram após os ajustes.

9. Execução integrada — Todos os testes

Resultado completo registrado:

text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
collected 7 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 14%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 28%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 42%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [ 57%]
test_uti_triagem.py::test_paciente_saudavel_baixo_risco PASSED           [ 71%]
test_uti_triagem.py::test_salto_nao_linear_queda_spo2 PASSED             [ 85%]
test_uti_triagem.py::test_validacao_limites_fisiologicos PASSED          [100%]

============================== 7 passed in 1.36s ===============================


Conclusão: a suíte integrada registrou sete testes aprovados, sem falhas.

10. Resumo geral dos resultados
Etapa	Resultado registrado	Situação
Motor fuzzy — primeira execução	4 aprovados	Sucesso
Motor fuzzy — erro proposital	1 falhou, 3 aprovados	Erro detectado
Motor fuzzy — após correção	4 aprovados	Sucesso
Latência do motor fuzzy	1,322 ms; 3,549 ms; 2,438 ms	Abaixo de 10 ms
Triagem de UTI — versão inicial	2 falharam, 1 aprovado	Necessitou ajustes
Triagem de UTI — após ajustes	3 aprovados	Sucesso
Suíte integrada	7 aprovados	Sucesso
11. Conclusão final

A atividade permitiu desenvolver e validar testes automatizados para um motor de inferência fuzzy e para um sistema acadêmico de triagem de UTI.

Foram realizados testes de:

Limites e intervalo de saída.
Monotonicidade da inferência.
Tratamento de entradas inválidas.
Desempenho e latência.
Comportamento não linear diante da queda da saturação de oxigênio.
Detecção de erro proposital e verificação após sua correção.

Na primeira versão da triagem de UTI, dois testes falharam. Após os ajustes, os três testes específicos passaram. A execução integrada final também registrou sete testes aprovados.

As medições de desempenho ficaram abaixo do limite estabelecido de 10 ms por inferência.

Resultado final registrado: 7 testes aprovados na execução integrada.

Observação: este relatório reúne os resultados das execuções fornecidas durante o desenvolvimento. Os resultados históricos com falhas foram mantidos para documentar o processo de validação, enquanto as execuções posteriores registram a versão ajustada.
