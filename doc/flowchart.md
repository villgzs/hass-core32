# Process flowchart
```
┌─────────────────────────┐                     ┌─────────────────────────────┐          
│Step No.1                │                     │Aux process: A               │          
│ Creating docker image   │    ┌───────────────►│ Creating docker image       │          
│  docker-base/alpine     │    │          ┌────►│  wheels                     │          
│      base               │    │          │     │musllinux_1_2/cp314          │          
└────────────┬────────────┘    │          │     └──────────────┬──────────────┘          
             │                 │          │                    │                         
             │                 │          │                    │                         
┌────────────▼─────────────────┴──────┐   │        ┌───────────▼───────────┐             
│Step No.2                            │   │        │Aux process: B         │             
│ Creating docker image               │   │        │ Workflow:create wheels│             
│  docker-base/python/3.14            │   │        │  core                 │             
│      base-python                    │   │        └───────────┬───────────┘             
└────────────┬────────────────────────┘   │                    │                         
             │                            │                    │                         
             │                            │                    ▼                         
┌────────────▼───────────────┐        ┌───┴─────────────────────────────────────────────┐
│Step No.3.                  │        │                                                 │
│ Creating docker image      │◄───────┤https://wheels.home-assistant.io/musllinux-index/│
│  docker                    │    ┌───┤                                                 │
│    homeassistant-base      │    │   └─────────────────────────────────────────────────┘
└────────────┬───────────────┘    │                                                      
             │                    │                                                      
             │                    │                                                      
┌────────────▼────────────┐       │                                                      
│Step No.4.               │       │                                                      
│ Creating docker image   │◄──────┘                                                      
│         core            │                                                              
│                         │                                                              
└─────────────────────────┘                                                              
```


**2026-NOV-24**
