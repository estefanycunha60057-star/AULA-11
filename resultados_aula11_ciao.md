AULA 11 — VALIDAÇÃO EXPERIMENTAL E FECHAMENTO DA AC-3 (SPRINT 3)

Disciplina: Projeto Tech
Atividade: Aula 11 — Suíte de Testes Automatizados (Pytest)
Objetivo: Validar os limites, a monotonicidade, o tratamento de exceções e o desempenho do motor fuzzy, além de testar o sistema de triagem de UTI.

1. ARQUIVOS DO PROJETO

Arquivos utilizados na atividade:

src/__init__.py
src/engine.py
src/model.py
src/uti_triagem.py
test_fuzzy_engine.py
test_uti_triagem.py
AULA_11/resultados_aula11_ciao.md
2. PRIMEIRA ETAPA — EXECUÇÃO DOS TESTES DO MOTOR FUZZY
2.1 Comando executado
bash
python -m pytest -v test_fuzzy_engine.py

2.2 Resultado completo recebido
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

============================== 4 passed in 1.05s ===============================

2.3 Análise

Os quatro testes foram aprovados.

test_saida_dentro_do_universo: verifica se a saída está no intervalo de 0 a 100.
test_monotonicidade_impacto: verifica se o aumento do impacto mantém ou aumenta a urgência.
test_entradas_invalidas_disparam_erro: verifica o tratamento de entradas fora dos limites permitidos.
test_latencia_inferencia: verifica o tempo de execução das inferências.
3. SEGUNDA ETAPA — EXECUÇÃO COM ERRO PROPOSITAL
3.1 Erro introduzido

Foi alterada propositalmente a condição do teste de intervalo de saída para provocar uma falha:

python
assert resultado < 0  # ERRO PROPOSITAL


A condição está incorreta para esse teste, pois a saída válida do motor fuzzy deve estar entre 0 e 100.

3.2 Comando executado
bash
python -m pytest -v test_fuzzy_engine.py

3.3 Primeiro resultado completo recebido
text
Erro proposital inserido com sucesso.
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
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
            ^^^^^^^^^^^^^^^^^^^^
E           assert 16.666666666666664 < 0

test_fuzzy_engine.py:54: AssertionError
========================= 1 failed, 3 passed in 1.37s =========================

3.4 Segunda execução com o erro proposital
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo FAILED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

=================================== FAILURES ===================================
________________________ test_saida_dentro_do_universo _________________________

simulador = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7a4673ed4830>

    def test_saida_dentro_do_universo(simulador):
        casos = [(0, 0), (50, 5), (100, 10), (30, 8), (80, 2)]
        for imp, exp in casos:
            resultado = executar_inferencia(simulador, imp, exp)
>           assert resultado < 0  # ERRO PROPOSITAL
            ^^^^^^^^^^^^^^^^^^^^
E           assert 16.666666666666664 < 0

test_fuzzy_engine.py:54: AssertionError
========================= 1 failed, 3 passed in 1.16s =========================

3.5 Análise do erro

O pytest identificou corretamente a falha proposital. O valor calculado foi 16.666666666666664, que não atende à condição incorreta resultado < 0.

O resultado demonstra que o framework identificou a falha do teste conforme esperado.

4. TERCEIRA ETAPA — EXECUÇÃO DO MOTOR FUZZY APÓS A CORREÇÃO

Após corrigir a condição do teste, a suíte foi executada novamente.

4.1 Comando executado
bash
python -m pytest -v test_fuzzy_engine.py

4.2 Resultado completo recebido
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

============================== 4 passed in 1.21s ===============================

4.3 Execução corrigida mais recente
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

============================== 4 passed in 1.31s ===============================

4.4 Análise

Após a correção, todos os quatro testes foram aprovados. O resultado confirma que a condição de intervalo de saída voltou a verificar o comportamento esperado do motor fuzzy.

5. TESTE DE DESEMPENHO E LATÊNCIA
5.1 Comando executado
bash
python -m pytest -s test_fuzzy_engine.py

5.2 Resultado anterior recebido
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items

test_fuzzy_engine.py ...Tempo medio por inferencia: 1.322 ms
.

============================== 4 passed in 1.27s ===============================

5.3 Resultado intermediário recebido
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items

test_fuzzy_engine.py ...
Tempo médio por inferência: 2.438 ms
PASSED

============================== 4 passed in 1.25s ===============================

5.4 Resultado mais recente recebido
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items

test_fuzzy_engine.py ...
Tempo médio por inferência: 3.549 ms
.

============================== 4 passed in 1.46s ===============================

5.5 Análise de desempenho

A medição mais recente registrou uma latência média de 3,549 ms por inferência.

O limite definido no teste é de 10 ms por chamada. Portanto, o teste de desempenho foi aprovado nessa execução.

As medições anteriores foram de 1,322 ms e 2,438 ms. Variações podem ocorrer em função do ambiente de execução, do aquecimento do sistema e da carga computacional.

Para referência final, considera-se a medição mais recente: 3,549 ms por inferência.

6. SISTEMA DE TRIAGEM FUZZY DE UTI
6.1 Objetivo

Desenvolver um sistema fuzzy para estimar o risco clínico a partir de dois sinais vitais:

Frequência cardíaca (FC).
Saturação periférica de oxigênio (SpO₂).

O sistema utiliza funções de pertinência e regras de inferência para classificar o risco em baixo, moderado ou crítico.

6.2 Simulação manual registrada
text
Sistema de triagem de UTI iniciado.
FC: 75 bpm | SpO2: 98% | Risco: 11.67%
FC: 75 bpm | SpO2: 95% | Risco: 35.71%
FC: 75 bpm | SpO2: 89% | Risco: 85.57%

6.3 Interpretação

Na simulação registrada, a redução da saturação de oxigênio foi acompanhada pelo aumento do risco calculado:

SpO₂ de 98%: risco calculado de 11,67%.
SpO₂ de 95%: risco calculado de 35,71%.
SpO₂ de 89%: risco calculado de 85,57%.

Esses resultados ilustram o comportamento não linear esperado do modelo fuzzy. São resultados computacionais acadêmicos, e não constituem validação clínica ou recomendação médica.

7. TESTES DA TRIAGEM DE UTI — EXECUÇÃO COM FALHAS

Durante o desenvolvimento, foram registradas execuções em que dois testes falharam e o teste de validação de limites foi aprovado.

7.1 Primeiro resultado de falha
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 3 items

test_uti_triagem.py::test_paciente_saudavel_baixo_risco FAILED
test_uti_triagem.py::test_salto_nao_linear_queda_spo2 FAILED
test_uti_triagem.py::test_validacao_limites_fisiologicos PASSED

=================================== FAILURES ===================================
______________________ test_paciente_saudavel_baixo_risco ______________________

resultado = 50.81006575787557
assert resultado < 30.0

_______________________ test_salto_nao_linear_queda_spo2 _______________________

risco_95 = 50.81006575787557
assert risco_95 < 35.0

========================= 2 failed, 1 passed in 1.07s =========================

7.2 Outra execução com falhas
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 3 items

test_uti_triagem.py::test_paciente_saudavel_baixo_risco FAILED
test_uti_triagem.py::test_salto_nao_linear_queda_spo2 FAILED
test_uti_triagem.py::test_validacao_limites_fisiologicos PASSED

=================================== FAILURES ===================================
______________________ test_paciente_saudavel_baixo_risco ______________________

simulador_uti = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7b4ac20886e0>

    def test_paciente_saudavel_baixo_risco(simulador_uti):
        resultado = avaliar_paciente(simulador_uti, 75.0, 98.0)
>       assert resultado < 30.0
E       assert 50.81006575787557 < 30.0

test_uti_triagem.py:49: AssertionError
_______________________ test_salto_nao_linear_queda_spo2 _______________________

simulador_uti = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7b4ac21d3b10>

    def test_salto_nao_linear_queda_spo2(simulador_uti):
        risco_95 = avaliar_paciente(simulador_uti, 75.0, 95.0)
        risco_89 = avaliar_paciente(simulador_uti, 75.0, 89.0)
>       assert risco_95 < 35.0
E       assert 50.81006575787557 < 35.0

test_uti_triagem.py:54: AssertionError
========================= 2 failed, 1 passed in 1.20s =========================

7.3 Análise das falhas

As falhas ocorreram porque os valores calculados não atendiam aos limites definidos nos testes de risco baixo e de saturação limítrofe.

Os resultados foram registrados para documentar o processo de depuração e os ajustes realizados durante o desenvolvimento.

8. TESTES FINAIS DA TRIAGEM DE UTI — APÓS AS CORREÇÕES
8.1 Comando executado
bash
python -m pytest -v test_uti_triagem.py

8.2 Resultado final completo recebido
text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 3 items

test_uti_triagem.py::test_paciente_saudavel_baixo_risco PASSED           [ 33%]
test_uti_triagem.py::test_salto_nao_linear_queda_spo2 PASSED             [ 66%]
test_uti_triagem.py::test_validacao_limites_fisiologicos PASSED          [100%]

============================== 3 passed in 1.01s ===============================

8.3 Análise final da triagem

Os três testes foram aprovados:

Paciente saudável: verifica se o risco calculado é inferior a 30%.
Salto não linear: verifica se o risco para SpO₂ de 95% é inferior a 35% e se a queda para 89% provoca aumento significativo do risco.
Limites fisiológicos: verifica se valores inválidos de frequência cardíaca e saturação geram ValueError.

O resultado final indica que o modelo atendeu às condições implementadas na suíte de testes.

9. RESUMO GERAL DAS EXECUÇÕES
Etapa	Resultado
Motor fuzzy — execução inicial	4 aprovados
Motor fuzzy — erro proposital	1 falha e 3 aprovados
Motor fuzzy — após correção	4 aprovados
Latência — primeira medição registrada	1,322 ms
Latência — medição intermediária	2,438 ms
Latência — medição mais recente	3,549 ms
Triagem de UTI — execução com falhas	2 falhas e 1 aprovado
Triagem de UTI — execução final	3 aprovados
Total de testes nas duas suítes finais	7 aprovados
10. CONCLUSÃO

A atividade permitiu desenvolver e validar um motor de inferência fuzzy por meio de testes automatizados com pytest.

Foram realizados testes de intervalo de saída, monotonicidade, tratamento de entradas inválidas e desempenho. Também foi introduzido um erro proposital para verificar a capacidade do pytest de detectar falhas, seguido da correção e da execução bem-sucedida da suíte.

A medição de latência mais recente foi de 3,549 ms por inferência, abaixo do limite de 10 ms definido no teste.

Na etapa de triagem de UTI, os testes finais de paciente saudável, salto não linear da saturação e validação dos limites fisiológicos foram aprovados.

Resultado final das suítes enviadas: 7 testes aprovados, sem falhas nas execuções finais.

O relatório registra também as falhas encontradas durante o desenvolvimento e os resultados anteriores, documentando o processo experimental.

Observação: os resultados são de um modelo acadêmico fuzzy. O sistema não deve ser usado isoladamente para diagnóstico, classificação clínica real ou decisões de tratamento em UTI.
