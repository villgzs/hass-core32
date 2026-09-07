# Process flowchart
```
                                                                                                                                       
  ┌─────────────────────────┐   ┌─────────────────────────────────────┐  ┌────────────────────────────┐  ┌─────────────────────────┐   
  │Step No.1                │   │Step No.2                            │  │Step No.3.                  │  │Step No.4.               │   
  │ Creating docker image   │──►│ Creating docker image               │─►│ Creating docker image      │─►│ Creating docker image   │   
  │  docker-base/alpine     │   │  docker-base/python/3.14            │  │  docker                    │  │  core                   │   
  │      base:3.24-2026.06.1│   │base-python:3.14-alpine3.24-2026.06.1│  │homeassistant-base:2026.07.0│  │                         │   
  └─────────────────────────┘   └─────────────────────────────────────┘  └────────────────────────────┘  └─────────────────────────┘   
                                                  ▲                                   ▲                                ▲               
                                                  │                                   │                                │               
                                                  │           ┌─────────────────────────────────────────────────┐      │               
                                                  │           │                                                 │      │               
                                                  └───────────│https://wheels.home-assistant.io/musllinux-index/│──────┘               
                                                              │                                                 │                      
                                                              └─────────────────────────────────────────────────┘                      
                                                                                      ▲                                                
  ┌─────────────────────────┐   ┌─────────────────────────┐                           │                                                
  │Aux process: A           │   │Aux process: B           │                           │                                                
  │ Creating docker image   ├──►│ Workflow:create wheels  ├───────────────────────────┘                                                
  │  wheels                 │   │  core                   │                                                                            
  └─────────────────────────┘   └─────────────────────────┘
```

**2026-SEP-7**
