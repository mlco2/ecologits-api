PROVIDERS_RESPONSES = {
    200: {
        "description": "List of provider identifiers.",
        "content": {
            "application/json": {
                "example": {
                    "providers": [
                        "anthropic",
                        "mistralai",
                        "openai",
                        "huggingface_hub",
                        "cohere",
                        "google_genai",
                    ]
                }
            }
        },
    },
}
