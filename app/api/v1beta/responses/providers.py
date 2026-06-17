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

VIDEO_PROVIDERS_RESPONSES = {
    200: {
        "description": "List of video generation provider identifiers.",
        "content": {
            "application/json": {
                "example": {
                    "providers": [
                        "klingai",
                        "openai",
                        "google",
                        "runway",
                    ]
                }
            }
        },
    },
}
