import base64
import json


def lambda_handler(event, context):
    output = []

    for record in event["records"]:
        try:
            # Decode data
            payload = base64.b64decode(record["data"]).decode("utf-8")

            # Parse record (giả định là JSON)
            parsed = json.loads(payload)

            # Convert back to JSON string for .jsonl
            json_line = json.dumps(parsed)

            # Encode lại kết quả
            output_record = {
                "recordId": record["recordId"],
                "result": "Ok",
                "data": base64.b64encode((json_line + "\n").encode("utf-8")).decode(
                    "utf-8"
                ),
            }

        except Exception as e:
            output_record = {
                "recordId": record["recordId"],
                "result": "ProcessingFailed",
                "data": record["data"],
            }

        output.append(output_record)

    return {"records": output}
