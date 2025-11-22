from django.core.management.base import BaseCommand
from django.conf import settings
import os
import yaml
from pathlib import Path

class Command(BaseCommand):
    help = 'Generate OpenAPI/Swagger documentation'

    def handle(self, *args, **options):
        docs_dir = Path(settings.BASE_DIR) / 'docs'
        os.makedirs(docs_dir, exist_ok=True)
        
        openapi_spec = {
            'openapi': '3.0.3',
            'info': {
                'title': 'Tourist Destinations API',
                'description': 'API for managing tourist destinations',
                'version': '1.0.0',
                'contact': {
                    'name': 'API Support',
                    'email': 'support@example.com'
                }
            },
            'servers': [
                {
                    'url': 'http://localhost:8000/api',
                    'description': 'Development server'
                },
                {
                    'url': 'https://api.example.com',
                    'description': 'Production server'
                }
            ],
            'paths': {
                '/destinations/': {
                    'get': {
                        'summary': 'List all destinations',
                        'responses': {
                            '200': {
                                'description': 'A list of destinations',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'array',
                                            'items': {
                                                '$ref': '#/components/schemas/Destination'
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'post': {
                        'summary': 'Create a new destination',
                        'requestBody': {
                            'required': True,
                            'content': {
                                'multipart/form-data': {
                                    'schema': {
                                        '$ref': '#/components/schemas/DestinationCreate'
                                    }
                                }
                            }
                        },
                        'responses': {
                            '201': {
                                'description': 'Destination created successfully',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/Destination'
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '/destinations/{id}/': {
                    'get': {
                        'summary': 'Retrieve a destination',
                        'parameters': [
                            {
                                'name': 'id',
                                'in': 'path',
                                'required': True,
                                'schema': {
                                    'type': 'integer'
                                },
                                'description': 'A unique integer value identifying this destination'
                            }
                        ],
                        'responses': {
                            '200': {
                                'description': 'Destination details',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/Destination'
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'put': {
                        'summary': 'Update a destination',
                        'parameters': [
                            {
                                'name': 'id',
                                'in': 'path',
                                'required': True,
                                'schema': {
                                    'type': 'integer'
                                },
                                'description': 'A unique integer value identifying this destination'
                            }
                        ],
                        'requestBody': {
                            'required': True,
                            'content': {
                                'multipart/form-data': {
                                    'schema': {
                                        '$ref': '#/components/schemas/DestinationUpdate'
                                    }
                                }
                            }
                        },
                        'responses': {
                            '200': {
                                'description': 'Destination updated successfully',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            '$ref': '#/components/schemas/Destination'
                                        }
                                    }
                                }
                            }
                        }
                    },
                    'delete': {
                        'summary': 'Delete a destination',
                        'parameters': [
                            {
                                'name': 'id',
                                'in': 'path',
                                'required': True,
                                'schema': {
                                    'type': 'integer'
                                },
                                'description': 'A unique integer value identifying this destination'
                            }
                        ],
                        'responses': {
                            '204': {
                                'description': 'Destination deleted successfully'
                            }
                        }
                    }
                }
            },
            'components': {
                'schemas': {
                    'Destination': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'readOnly': True
                            },
                            'place_name': {
                                'type': 'string',
                                'example': 'Taj Mahal'
                            },
                            'slug': {
                                'type': 'string',
                                'readOnly': True,
                                'example': 'taj-mahal'
                            },
                            'weather': {
                                'type': 'string',
                                'example': 'Sunny'
                            },
                            'state': {
                                'type': 'string',
                                'example': 'Uttar Pradesh'
                            },
                            'district': {
                                'type': 'string',
                                'example': 'Agra'
                            },
                            'google_map_link': {
                                'type': 'string',
                                'format': 'uri',
                                'example': 'https://goo.gl/maps/5Hsm5'
                            },
                            'description': {
                                'type': 'string',
                                'example': 'An ivory-white marble mausoleum'
                            },
                            'images': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {
                                            'type': 'integer'
                                        },
                                        'image': {
                                            'type': 'string',
                                            'format': 'uri'
                                        },
                                        'thumbnail': {
                                            'type': 'string',
                                            'format': 'uri'
                                        },
                                        'caption': {
                                            'type': 'string'
                                        }
                                    }
                                }
                            },
                            'created_at': {
                                'type': 'string',
                                'format': 'date-time',
                                'readOnly': True
                            },
                            'updated_at': {
                                'type': 'string',
                                'format': 'date-time',
                                'readOnly': True
                            }
                        }
                    },
                    'DestinationCreate': {
                        'type': 'object',
                        'required': ['place_name', 'weather', 'state', 'district'],
                        'properties': {
                            'place_name': {
                                'type': 'string',
                                'example': 'Taj Mahal'
                            },
                            'weather': {
                                'type': 'string',
                                'example': 'Sunny'
                            },
                            'state': {
                                'type': 'string',
                                'example': 'Uttar Pradesh'
                            },
                            'district': {
                                'type': 'string',
                                'example': 'Agra'
                            },
                            'google_map_link': {
                                'type': 'string',
                                'format': 'uri',
                                'example': 'https://goo.gl/maps/5Hsm5'
                            },
                            'description': {
                                'type': 'string',
                                'example': 'An ivory-white marble mausoleum'
                            },
                            'images': {
                                'type': 'array',
                                'items': {
                                    'type': 'string',
                                    'format': 'binary'
                                },
                                'description': 'Upload multiple images'
                            }
                        }
                    },
                    'DestinationUpdate': {
                        'type': 'object',
                        'properties': {
                            'place_name': {
                                'type': 'string',
                                'example': 'Taj Mahal'
                            },
                            'weather': {
                                'type': 'string',
                                'example': 'Sunny'
                            },
                            'state': {
                                'type': 'string',
                                'example': 'Uttar Pradesh'
                            },
                            'district': {
                                'type': 'string',
                                'example': 'Agra'
                            },
                            'google_map_link': {
                                'type': 'string',
                                'format': 'uri',
                                'example': 'https://goo.gl/maps/5Hsm5'
                            },
                            'description': {
                                'type': 'string',
                                'example': 'An ivory-white marble mausoleum'
                            },
                            'images': {
                                'type': 'array',
                                'items': {
                                    'type': 'string',
                                    'format': 'binary'
                                },
                                'description': 'Upload additional images'
                            }
                        }
                    },
                    'Error': {
                        'type': 'object',
                        'properties': {
                            'detail': {
                                'type': 'string',
                                'example': 'Not found.'
                            }
                        }
                    }
                },
                'securitySchemes': {
                    'BasicAuth': {
                        'type': 'http',
                        'scheme': 'basic'
                    },
                    'BearerAuth': {
                        'type': 'http',
                        'scheme': 'bearer',
                        'bearerFormat': 'JWT'
                    }
                }
            },
            'security': [
                {
                    'BasicAuth': [],
                    'BearerAuth': []
                }
            ]
        }

        # Write YAML file
        yaml_file = docs_dir / 'openapi.yaml'
        with open(yaml_file, 'w') as f:
            yaml.dump(openapi_spec, f, sort_keys=False, default_flow_style=False)
        
        self.stdout.write(self.style.SUCCESS(f'OpenAPI specification generated at {yaml_file}'))
        
        # Write JSON file
        import json
        json_file = docs_dir / 'openapi.json'
        with open(json_file, 'w') as f:
            json.dump(openapi_spec, f, indent=2)
        
        self.stdout.write(self.style.SUCCESS(f'OpenAPI specification (JSON) generated at {json_file}'))