# Process flowchart
```
┌─────────────────────────┐                     ┌─────────────────────────────┐          
│Step No.1                │                     │Aux process: A               │          
│ Creating docker image   │                     │ Creating docker image       │          
│  docker-base/alpine     │                     │  wheels                     │          
│      base:3.24-2026.06.1│                     │musllinux_1_2/cp314:2026.07.0│          
└────────────┬────────────┘                     └──────────────┬──────────────┘          
             │                                                 │                         
             │                                                 │                         
┌────────────▼────────────────────────┐            ┌───────────▼───────────┐             
│Step No.2                            │            │Aux process: B         │             
│ Creating docker image               │            │ Workflow:create wheels│             
│  docker-base/python/3.14            │            │  core                 │             
│base-python:3.14-alpine3.24-2026.06.1│            └───────────┬───────────┘             
└────────────┬────────────────────────┘                        │                         
             │                    ▲                            │                         
             │                    │                            ▼                         
┌────────────▼───────────────┐    │   ┌─────────────────────────────────────────────────┐
│Step No.3.                  │    └───┤                                                 │
│ Creating docker image      │◄───────┤https://wheels.home-assistant.io/musllinux-index/│
│  docker                    │    ┌───┤                                                 │
│homeassistant-base:2026.07.0│    │   └─────────────────────────────────────────────────┘
└────────────┬───────────────┘    │                                                      
             │                    │                                                      
             │                    │                                                      
┌────────────▼────────────┐       │                                                      
│Step No.4.               │       │                                                      
│ Creating docker image   │◄──────┘                                                      
│  core                   │                                                              
│                         │                                                              
└─────────────────────────┘                                                                                                                                                                                                                                
```


**2026-SEP-7**
