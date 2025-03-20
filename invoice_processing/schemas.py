"""This module contains JSON schemas for invoice parsing and detection."""

# Schema for invoice parsing.
AI_INVOICE_JSON_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "strict": True,
        "name": "parsed_invoice",
        "schema": {
            "type": "object",
            "properties": {
                "companyName": {"type": "string", "nullable": True},
                "date": {"type": "string", "nullable": True},
                "amount": {"type": "string", "nullable": True},
                "invoiceId": {"type": "string", "nullable": True},
            },
            "required": ["companyName", "date", "amount", "invoiceId"],
            "additionalProperties": False,
        },
    },
}

# Schema for invoice detection (boolean response).
AI_BOOLEAN_SCHEMA = {"type": "text"}
