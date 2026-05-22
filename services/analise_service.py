import pandas as pd


def analisar_desempenho(df):

    resultados = []

    # PEGAR TODOS OS CONTEÚDOS
    conteudos = df["Conteúdo"].unique()

    for conteudo in conteudos:

        # FILTRAR SOMENTE O CONTEÚDO ATUAL
        df_conteudo = df[df["Conteúdo"] == conteudo]

        # CALCULAR MÉDIA GERAL
        media_geral = df_conteudo["Média"].mean()

        # ANALISAR CADA TURMA
        for _, linha in df_conteudo.iterrows():

            turma = linha["Turma"]
            media = linha["Média"]

            # REGRA DE ALERTA
            if media < media_geral - 1.5:

                alerta = f"""
⚠️ ALERTA PEDAGÓGICO

A turma {turma} apresentou desempenho
muito abaixo da média em {conteudo}.

📉 Média da turma: {media:.1f}
📊 Média geral: {media_geral:.1f}

Sugestões de intervenção:
• reforço direcionado
• revisão diagnóstica
• acompanhamento pedagógico
• retomada de pré-requisitos
"""

                resultados.append(alerta)

    return resultados