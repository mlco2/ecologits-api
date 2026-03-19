ELECTRICITY_MIX_RESPONSES = {
    200: {
        "description": "Electricity mix composition for the specified zone.",
        "content": {
            "application/json": {
                "example": {
                    "electricity_mix": {
                        "zone": "FRA",
                        "adpe": 4.858e-08,
                        "pe": 9.3135,
                        "gwp": 0.04418,
                        "wue": 3.6737,
                    }
                }
            }
        },
    },
    404: {
        "description": "Zone not supported by EcoLogits.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Electricity mix zone 'XYZ' is not supported by EcoLogits"
                }
            }
        },
    },
}
