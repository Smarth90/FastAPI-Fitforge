import json
from jsonschema import validate, ValidationError


def validate_and_fix(output, schema, llm, retries=3):
    for attempt in range(retries):
        try:
            parsed = json.loads(output)
            validate(instance=parsed, schema=schema)
            return parsed

        except (json.JSONDecodeError, ValidationError) as e:
            repair_prompt = f"""
Fix this JSON to match the schema exactly.

ERROR:
{str(e)}

JSON:
{output}

Return ONLY valid JSON.
"""
            output = llm.invoke(repair_prompt)

    raise Exception("Failed to generate valid JSON")