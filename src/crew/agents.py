from src.config import Config
from langchain_openai import ChatOpenAI
from src.utils.logger import logger_set
from src.crew.serializers import OutputFile
from crewai.tasks.task_output import TaskOutput
from crewai import Agent, Process, Task, Crew
from src.agent.models import Agent as AgentModel
from src.crew.prompts import get_comment_task_prompt


class CustomAgent:
    """
    A custom agent class that creates and manages a crew of agents to perform tasks.

    This class initializes agents, creates tasks, and manages a crew to execute those tasks.
    It uses OpenAI's ChatGPT model for natural language processing.

    Attributes:
        model (ChatOpenAI): The language model used by the agents.
        role (str): The role of the primary agent.
        goal (str): The goal of the primary agent.
        backstory (str): The backstory of the primary agent.
        tools (list[Tool]): A list of tools available to the primary agent.
        agents (list[Agent]): A list of agents (primary and comment agents).
        expected_output (str): The expected output format for the primary task.
        description (str): The description of the primary task.
        tasks (list[Task]): A list of tasks to be performed.
        crew (Crew): A crew object managing the agents and tasks.
    """

    def __init__(
        self,
        agent: AgentModel,
        agent_instruction: str,
        agent_output: str,
        tools: list,
        params: dict = {},
        model: str = Config.MODEL_NAME,
    ):
        self.model = ChatOpenAI(
            model=model,
            api_key=Config.OPENAI_API_KEY,
        )
        self.agent = agent
        self.tools = tools

        self.agent_instruction = agent_instruction
        self.agent_output = agent_output
        self.params = params

    def __create_agent(self) -> list[Agent]:
        logger_set.info("Agent creation started")

        # Check for required attributes
        if self.model is None:
            logger_set.error("Model is not initialized")
            raise ValueError("Model must be initialized")

        if self.agent is None:
            logger_set.error("Agent model is not provided")
            raise ValueError("Agent model must be provided")

        agent_list = []

        try:
            custom_agent = Agent(
                role=self.agent.description,
                goal=self.agent.key_feature,
                backstory=self.agent.personality,
                llm=self.model,
                tools=self.tools,
                verbose=False,
            )
            agent_list.append(custom_agent)

            if not self.agent.is_chatbot:
                comment_agent = Agent(
                    role="Comment agent",
                    goal="Comment on the previous task completed by agents.",
                    backstory="You are an observer of tasks being completed by agents and check if tasks are being completed as expected.",
                    llm=self.model,
                    verbose=False,
                )
                agent_list.append(comment_agent)
            logger_set.info("Custom agent created successfully")

        except Exception as e:
            logger_set.error(f"Error while creating agents: {e}")
            raise

        logger_set.info(f"Agents created: {agent_list}")
        return agent_list

    def __create_tasks(self) -> list[Task]:
        logger_set.info("Task creation started")

        tasks = []
        custom_task = Task(
            description=self.agent_instruction,
            expected_output=self.agent_output,
            agent=self.custom_agent[0],
            output_json=OutputFile,
        )
        tasks.append(custom_task)

        if not self.agent.is_chatbot:
            comment_prompt = get_comment_task_prompt()
            comment_task = Task(
                description=comment_prompt,
                expected_output="Task reviewed: ",
                agent=self.custom_agent[1],
            )
            tasks.append(comment_task)

        logger_set.info(f"Task created: {tasks}")
        return tasks

    def __create_crew(self) -> Crew:
        logger_set.info("Crew creation started")
        crew = Crew(
            agents=self.custom_agent,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            output_log_file="crew.log",
        )
        logger_set.info(f"Crew created: {crew}")

        return crew

    async def main(self) -> tuple[TaskOutput, TaskOutput]:
        self.custom_agent = self.__create_agent()
        self.tasks = self.__create_tasks()
        self.crew = self.__create_crew()

        logger_set.info("Kickout started")
        self.params.update({"description": self.agent_instruction})
        if self.agent.is_chatbot:
            response = await self.crew.kickoff_async(inputs=self.params)
            return response

        response = await self.crew.kickoff_async(inputs=self.params)
        output = response.tasks_output

        custom_task_output = output[0]
        comment_task_output = output[1]

        return (custom_task_output, comment_task_output)
