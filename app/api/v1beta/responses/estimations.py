ESTIMATIONS_RESPONSES = {
    200: {
        "description": "Environmental impact estimation with min/max intervals.",
        "content": {
            "application/json": {
                "example": {
                    "impacts": {
                        "energy": {
                            "type": "energy",
                            "name": "Energy",
                            "value": {
                                "min": 0.00001740232832301384,
                                "max": 0.000021502108309942407,
                            },
                            "unit": "kWh",
                        },
                        "gwp": {
                            "type": "GWP",
                            "name": "Global Warming Potential",
                            "value": {
                                "min": 0.000008448613075332601,
                                "max": 0.000010387850006949683,
                            },
                            "unit": "kgCO2eq",
                        },
                        "adpe": {
                            "type": "ADPe",
                            "name": "Abiotic Depletion Potential (elements)",
                            "value": {
                                "min": 1.2955834115064265e-11,
                                "max": 1.3011140147087931e-11,
                            },
                            "unit": "kgSbeq",
                        },
                        "pe": {
                            "type": "PE",
                            "name": "Primary Energy",
                            "value": {
                                "min": 0.0000476420806326274,
                                "max": 0.0000582486214368103,
                            },
                            "unit": "MJ",
                        },
                        "wcf": {
                            "type": "WCF",
                            "name": "Water Consumption Footprint",
                            "value": {
                                "min": 0.00009151188371940057,
                                "max": 0.00011307098675866313,
                            },
                            "unit": "L",
                        },
                        "usage": {
                            "type": "usage",
                            "name": "Usage",
                            "energy": {
                                "type": "energy",
                                "name": "Energy",
                                "value": {
                                    "min": 0.00001740232832301384,
                                    "max": 0.000021502108309942407,
                                },
                                "unit": "kWh",
                            },
                            "gwp": {
                                "type": "GWP",
                                "name": "Global Warming Potential",
                                "value": {
                                    "min": 0.000008231475320068776,
                                    "max": 0.000010170712251685857,
                                },
                                "unit": "kgCO2eq",
                            },
                            "adpe": {
                                "type": "ADPe",
                                "name": "Abiotic Depletion Potential (elements)",
                                "value": {
                                    "min": 2.3475740907745673e-13,
                                    "max": 2.9006344110112307e-13,
                                },
                                "unit": "kgSbeq",
                            },
                            "pe": {
                                "type": "PE",
                                "name": "Primary Energy",
                                "value": {
                                    "min": 0.000045021563604469106,
                                    "max": 0.000055628104408652,
                                },
                                "unit": "MJ",
                            },
                            "wcf": {
                                "type": "WCF",
                                "name": "Water Consumption Footprint",
                                "value": {
                                    "min": 0.00009151188371940057,
                                    "max": 0.00011307098675866313,
                                },
                                "unit": "L",
                            },
                        },
                        "embodied": {
                            "type": "embodied",
                            "name": "Embodied",
                            "gwp": {
                                "type": "GWP",
                                "name": "Global Warming Potential",
                                "value": {
                                    "min": 2.1713775526382546e-7,
                                    "max": 2.1713775526382546e-7,
                                },
                                "unit": "kgCO2eq",
                            },
                            "adpe": {
                                "type": "ADPe",
                                "name": "Abiotic Depletion Potential (elements)",
                                "value": {
                                    "min": 1.2721076705986809e-11,
                                    "max": 1.2721076705986809e-11,
                                },
                                "unit": "kgSbeq",
                            },
                            "pe": {
                                "type": "PE",
                                "name": "Primary Energy",
                                "value": {
                                    "min": 0.0000026205170281582953,
                                    "max": 0.0000026205170281582953,
                                },
                                "unit": "MJ",
                            },
                        },
                        "warnings": [
                            {
                                "code": "model-arch-not-released",
                                "message": "The model architecture has not been released, expect lower precision.",
                            },
                            {
                                "code": "model-arch-multimodal",
                                "message": "The model architecture is multimodal, expect lower precision.",
                            },
                        ],
                        "errors": None,
                    }
                }
            }
        },
    },
}
