from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# CrewBase implementation for our translation system with all required agents
@CrewBase
class TranslationCrew():
    """TranslationCrew for handling large context document translations between languages"""

    # Configuration files for our agents and tasks
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Define all required agents with proper configuration
    @agent
    def coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config['coordinator'],
            verbose=True
        )

    @agent
    def linguist(self) -> Agent:
        return Agent(
            config=self.agents_config['linguist'],
            verbose=True
        )

    @agent
    def context_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['context_expert'],
            verbose=True
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],
            verbose=True
        )

    @agent
    def technical_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_specialist'],
            verbose=True
        )

    @agent
    def cultural_consultant(self) -> Agent:
        return Agent(
            config=self.agents_config['cultural_consultant'],
            verbose=True
        )

    # Define all required tasks with proper configuration
    @task
    def initial_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['initial_analysis_task']
        )

    @task
    def context_preparation_task(self) -> Task:
        return Task(
            config=self.tasks_config['context_preparation_task']
        )

    @task
    def translation_task(self) -> Task:
        return Task(
            config=self.tasks_config['translation_task']
        )

    @task
    def technical_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_review_task']
        )

    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['editing_task']
        )

    @task
    def cultural_adaptation_task(self) -> Task:
        return Task(
            config=self.tasks_config['cultural_adaptation_task']
        )

    @task
    def final_assembly_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_assembly_task'],
            output_file='translated_document.txt'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TranslationCrew with all required agents and tasks"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # Can switch to hierarchical process if preferred for complex translations
            # process=Process.hierarchical,
        )