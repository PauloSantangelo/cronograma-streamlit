from crewai import Agent, Task, Crew, Process

def generate_schedule(client_name, client_description, goal, video_count, static_post_count, days_selected):
    agent_analysis = Agent(
        role="Analista de Cronogramas",
        goal="Analisar cronogramas antigos e gerar ideias consistentes.",
        backstory="Você é um especialista em análise de marketing digital.",
        memory=True,
        verbose=True
    )

    agent_creative = Agent(
        role="Especialista Criativo",
        goal="Gerar ideias inovadoras para cronogramas.",
        backstory="Você é um estrategista criativo que usa insights para criar campanhas de alto impacto.",
        memory=False,
        verbose=True
    )

    schedule_task = Task(
        description=(f"Crie um cronograma para o cliente '{client_name}' com as seguintes informações:\n"
                     f"- Objetivo: {goal}\n"
                     f"- {video_count} vídeos e {static_post_count} posts estáticos.\n"
                     f"- Dias: {', '.join(days_selected)}.\n\n"
                     f"Descrição do cliente: {client_description}\n"),
        expected_output="Cronograma detalhado com datas e ideias.",
        agent=agent_creative,
    )

    crew = Crew(
        agents=[agent_analysis, agent_creative],
        tasks=[schedule_task],
        process=Process.sequential
    )

    result = crew.kickoff(inputs={})

    # Retorna o conteúdo do cronograma gerado
    return result
