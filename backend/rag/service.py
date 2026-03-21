from backend.rag.chain import rag_generate_plan, llm
from backend.schemas.workout_plan import WeeklyWorkoutPlan
from backend.rag.validator import validate_and_fix



def generate_plan_safe(context):
    raw_output = rag_generate_plan(context)
    if hasattr(raw_output, "content"):
        raw_output = raw_output.content
    elif hasattr(raw_output, "text"):
        raw_output = raw_output.text

    validated_output = validate_and_fix(
        raw_output,
        WeeklyWorkoutPlan.model_json_schema(),
        llm
    )

    return validated_output