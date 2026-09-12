from pydantic import BaseModel

# Response Schema:
class CrewResponse(BaseModel):
    answer: str
    source: str
    grounded: bool
    escalation_recommended: bool

# Validation Function:
def validate_crew_response(
    answer,
    source,
    grounded,
    escalation_recommended
):
    response = CrewResponse(
        answer=answer,
        source=source,
        grounded=grounded,
        escalation_recommended=escalation_recommended
    )

    return response.model_dump()