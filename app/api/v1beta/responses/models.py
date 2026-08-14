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

VIDEO_MODELS_RESPONSES = {
    200: {
        "description": "List of video generation models for the provider.",
        "content": {
            "application/json": {
                "example": {
                    "models": [
                        {
                            "provider": "google",
                            "model_name": "google/veo-3.1",
                            "capabilities": {
                                "resolutions": [[1280, 720], [1920, 1080]],
                                "frames_count": [97, 145, 193],
                                "audio_generation": True,
                            },
                        }
                    ]
                }
            }
        },
    },
    404: {
        "description": "Video provider not found.",
        "content": {
            "application/json": {"example": {"detail": "Video provider not found"}}
        },
    },
}
