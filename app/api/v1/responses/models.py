MODELS_RESPONSES = {
    200: {
        "description": "List of models for the provider.",
        "content": {
            "application/json": {
                "example": {
                    "models": [
                        {
                            "provider": "openai",
                            "name": "gpt-4o-mini",
                            "architecture": {
                                "type": "moe",
                                "parameters": {
                                    "total": 440,
                                    "active": {"min": 44, "max": 132},
                                },
                            },
                            "warnings": [
                                {
                                    "code": "model-arch-not-released",
                                    "message": "The model architecture has not been released, expect lower precision.",
                                }
                            ],
                            "sources": [],
                        }
                    ]
                }
            }
        },
    },
    404: {
        "description": "Provider not found.",
        "content": {"application/json": {"example": {"detail": "Provider not found"}}},
    },
}
