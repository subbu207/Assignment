import base64
import json
import re
from datetime import datetime

# Example log entries provided by user (truncated and simplified for this step)
log_data = """
2023-12-01T12:00:00Z INFO User login successful: userID=12345, IP=192.168.0.1
2023-12-01T12:01:00Z ERROR NullPointerException: Null value encountered in object reference.
2023-12-01T12:02:00Z INFO Data update: userID=12345, dataID=98765
2023-12-01T12:03:00Z INFO BASE64: eyJ1c2VyIjogIjEyMzQ1IiwgImV2ZW50IjogInB1cmNoYXNlIiwgImFtb3VudCI6ICIxMDAuMDAifQ==
2023-12-01T12:04:00Z ERROR IndexOutOfBoundsException: Index 10 out of bounds for length 10.
2023-12-01T12:05:00Z WARN Malformed JSON payload: {user:12345,event:"purchase",amount:100}
"""

# Regular expressions for log parsing
error_pattern = re.compile(r"(?P<timestamp>[\d\-T:Z]+) ERROR (?P<message>.+)")
info_pattern = re.compile(r"(?P<timestamp>[\d\-T:Z]+) INFO (?P<message>.+)")
base64_pattern = re.compile(r"BASE64:\s(?P<data>.+)")

# Data containers
errors = []
info_logs = []
decoded_base64 = []

# Parse logs
for line in log_data.splitlines():
    error_match = error_pattern.match(line)
    info_match = info_pattern.match(line)
    base64_match = base64_pattern.search(line)
    
    # Extract errors
    if error_match:
        errors.append({
            "timestamp": error_match.group("timestamp"),
            "message": error_match.group("message")
        })
    
    # Extract general info logs
    elif info_match:
        info_logs.append({
            "timestamp": info_match.group("timestamp"),
            "message": info_match.group("message")
        })
    
    # Decode Base64 data
    if base64_match:
        try:
            decoded = base64.b64decode(base64_match.group("data")).decode("utf-8")
            decoded_base64.append(json.loads(decoded))
        except (ValueError, json.JSONDecodeError) as e:
            decoded_base64.append({"error": f"Failed to decode Base64: {str(e)}"})

# Results
parsed_data = {
    "errors": errors,
    "info_logs": info_logs,
    "decoded_base64": decoded_base64
}

parsed_data
