import re

def responder_pergunta(pergunta, dados, campus):
    pergunta = pergunta.lower()
    
    sinonimos = {
        "evadidos": ["evadidos", "evasão", "desistentes", "abandono", "evasões"],
        "concluintes": ["concluintes", "concluídos", "conclusão"],
        "em curso": ["em curso", "matrícula ativa", "matriculados"],
    }

    def identificar_situacao(pergunta):
        for situacao, termos in sinonimos.items():
            if any(termo in pergunta for termo in termos):
                return situacao
        return None

    def extrair_numero(texto):
        match = re.search(r'\d+', texto)
        return int(match.group()) if match else None

    def aplicar_recortes(dados, pergunta):
        ano = extrair_numero(pergunta)
        turno = next((s for s in dados["turno_do_curso"].unique() if s.lower() in pergunta), None)
        tipo_curso = next((s for s in dados["tipo_de_curso"].unique() if s.lower() in pergunta), None)

        if ano:
            dados = dados[dados["ano"] == ano]
        if turno:
            dados = dados[dados["turno_do_curso"].str.lower() == turno.lower()]
        if tipo_curso:
            dados = dados[dados["tipo_de_curso"].str.lower() == tipo_curso.lower()]
        return dados, tipo_curso

    dados, tipo_curso_mencionado = aplicar_recortes(dados.copy(), pergunta)

    def modalidade_situacao(dados, tipo, situacao):
        situacao_dados = dados[dados["situacao"] == situacao.capitalize()].groupby("tipo_de_curso")["matriculas"].sum()
        if tipo == "mais":
            modalidade = situacao_dados.idxmax()
            max_valor = situacao_dados.max()
            return f"A modalidade com mais {situacao.lower()} no campus {campus} foram os cursos de {modalidade} com {max_valor} {situacao.lower()}."
        elif tipo == "menos":
            modalidade = situacao_dados.idxmin()
            min_valor = situacao_dados.min()
            return f"A modalidade com menos {situacao.lower()} no campus {campus} foram os cursos de {modalidade} com {min_valor} {situacao.lower()}."
        else:
            return None

    situacao = identificar_situacao(pergunta)

    if any(termo in pergunta for termo in ["qual modalidade", "qual tipo de curso", "qual curso"]) and situacao:
        if "mais" in pergunta:
            return modalidade_situacao(dados, "mais", situacao)
        elif "menos" in pergunta:
            return modalidade_situacao(dados, "menos", situacao)

    if "total" in pergunta and "matrículas" in pergunta:
        total_matriculas = dados["matriculas"].sum()
        
        total_em_curso = dados[dados["situacao"] == "Em curso"]["matriculas"].sum()
        total_concluintes = dados[dados["situacao"] == "Concluintes"]["matriculas"].sum()
        total_evadidos = dados[dados["situacao"] == "Evadidos"]["matriculas"].sum()

        resposta = (
            f"Para o campus {campus}, o total de matrículas é {total_matriculas}, com {total_em_curso} alunos em curso, "
            f"{total_concluintes} concluintes e {total_evadidos} evadidos."
        )

        if not any(filtro in pergunta for filtro in ["ano", "turno", "tipo de curso"]):
            media_matriculas = dados["matriculas"].mean()
            desvio_matriculas = dados["matriculas"].std()
            ano_maior_matriculas = dados.groupby("ano")["matriculas"].sum().idxmax()
            maior_matriculas = dados.groupby("ano")["matriculas"].sum().max()
            resposta += (
                f" O ano com o maior número de matrículas foi "
                f"{ano_maior_matriculas} com {maior_matriculas} matrículas."
            )
        return resposta

    elif "total" in pergunta:
        if situacao:
            total = dados[dados["situacao"] == situacao.capitalize()]["matriculas"].sum()
            ano_maior = dados[dados["situacao"] == situacao.capitalize()].groupby("ano")["matriculas"].sum().idxmax()
            maior = dados[dados["situacao"] == situacao.capitalize()].groupby("ano")["matriculas"].sum().max()

            resposta = f"Para o campus {campus}, o total de {situacao} é {total}. "
            if not "ano" in pergunta:  
                resposta += f"O ano com o maior número de {situacao} foi {ano_maior} com {maior}."
            return resposta

    elif any(termo in pergunta for termo in ["maior número", "mais", "maior quantidade"]):
        situacao = situacao or "matrículas"
        if situacao != "matrículas":
            dados = dados[dados["situacao"] == situacao.capitalize()]

        ano_maior = dados.groupby("ano")["matriculas"].sum().idxmax()
        maior = dados.groupby("ano")["matriculas"].sum().max()
        tipo_curso_resposta = tipo_curso_mencionado if tipo_curso_mencionado else "curso geral"
        return f"No campus {campus}, o ano com o maior número de {situacao} para o {tipo_curso_resposta} foi {ano_maior} com {maior}."

    elif any(termo in pergunta for termo in ["menor número", "menos", "menor quantidade"]):
        situacao = situacao or "matrículas"
        if situacao != "matrículas":
            dados = dados[dados["situacao"] == situacao.capitalize()]

        ano_menor = dados.groupby("ano")["matriculas"].sum().idxmin()
        menor = dados.groupby("ano")["matriculas"].sum().min()
        tipo_curso_resposta = tipo_curso_mencionado if tipo_curso_mencionado else "curso geral"
        return f"No campus {campus}, o ano com o menor número de {situacao} para o {tipo_curso_resposta} foi {ano_menor} com {menor}."

    elif "média" in pergunta and "matrículas" in pergunta and "entre" in pergunta:
        anos = re.findall(r"\d+", pergunta)
        if len(anos) == 2:
            ano_inicio = int(anos[0])
            ano_fim = int(anos[1])
            media = dados[(dados["ano"] >= ano_inicio) & (dados["ano"] <= ano_fim)]["matriculas"].mean()
            return f"A média de matrículas no campus {campus} entre {ano_inicio} e {ano_fim} foi de {media:.2f}."
        else:
            return "Por favor, especifique o intervalo de anos corretamente (ex: entre 2010 e 2015)."

    else:
        return "Desculpe, não entendi a pergunta. Tente perguntar sobre o total, a média ou o ano com maior ou menor número de matrículas, evadidos, concluintes ou alunos em curso, especificando o ano, turno e/ou tipo de curso, se desejar."
