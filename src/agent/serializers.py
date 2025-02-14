from src.agent.models import Agent


def get_agent_serializer(agents: list[Agent]) -> list[dict]:
    agents_list = []

    if not isinstance(agents, list):
        agents = [agents]

    for agent in agents:
        agents_list.append(
            {
                "id": agent.id,
                "uuid": agent.uuid,
                "name": agent.name,
                # "cost": agent.cost,
                "description": agent.description,
                # "profile_image": agent.profile_image,
                # "video": agent.video,
                "key_feature": agent.key_feature,
                # "comment": agent.comment,
                "personality": agent.personality,
                "focus_group_survey": agent.focus_group_survey,
                "own_data": agent.own_data,
                "top_idea": agent.top_idea,
                "api_data": agent.api_data,
                "survey": agent.survey,
                # "group_id": agent.group_id,
                # "vector_id": agent.vector_id,
                # "created_by": agent.created_by,
                # "created_at": str(agent.created_at),
                # "updated_at": str(agent.updated_at),
            }
        )

    return agents_list
