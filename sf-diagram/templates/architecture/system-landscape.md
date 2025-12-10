# System Landscape Diagram Template

Flowchart template for visualizing high-level Salesforce system architecture using the sf-skills standard styling.

## When to Use
- Architecture overview presentations
- Integration landscape documentation
- System inventory
- Stakeholder communication

## Mermaid Template - Sales Cloud Integration Landscape

```mermaid
flowchart TB
    subgraph users["👥 Users"]
        direction LR
        U1["📱 Sales Reps<br/><small>Mobile App</small>"]
        U2["💻 Managers<br/><small>Desktop</small>"]
        U3["🌐 Partners<br/><small>Portal</small>"]
    end

    subgraph salesforce["☁️ Salesforce Platform"]
        direction TB

        subgraph core["Core CRM"]
            SF1["💼 Sales Cloud<br/><small>Leads, Opps</small>"]
            SF2["🎧 Service Cloud<br/><small>Cases, Knowledge</small>"]
            SF3["🌐 Experience Cloud<br/><small>Portals</small>"]
        end

        subgraph automation["⚡ Automation"]
            FL["🔄 Flows<br/><small>Process Builder</small>"]
            AP["⚡ Apex<br/><small>Triggers, Services</small>"]
            PE["📢 Platform Events<br/><small>CDC, Streaming</small>"]
        end

        subgraph ai["🤖 AI & Analytics"]
            EIN["🧠 Einstein<br/><small>Predictions</small>"]
            TB["📊 Tableau<br/><small>Dashboards</small>"]
            CRM["📈 CRM Analytics<br/><small>Reports</small>"]
        end
    end

    subgraph integration["🔄 Integration Layer"]
        direction LR
        MW["🔗 MuleSoft<br/><small>Anypoint Platform</small>"]
        API["🔐 API Gateway<br/><small>Named Credentials</small>"]
    end

    subgraph external["🏢 External Systems"]
        direction TB

        subgraph erp["ERP Systems"]
            SAP["🏭 SAP S/4HANA<br/><small>Finance, Inventory</small>"]
            NET["📦 NetSuite<br/><small>Orders</small>"]
        end

        subgraph marketing["Marketing"]
            MC["📧 Marketing Cloud<br/><small>Campaigns</small>"]
            PAR["🎯 Account Engagement<br/><small>Pardot</small>"]
        end

        subgraph data["Data & Storage"]
            DW["❄️ Snowflake<br/><small>Data Warehouse</small>"]
            S3["☁️ AWS S3<br/><small>Files</small>"]
        end
    end

    %% User connections
    U1 -->|"Salesforce Mobile"| SF1
    U2 -->|"Lightning"| SF1
    U2 -->|"Lightning"| SF2
    U3 -->|"Portal"| SF3

    %% Internal SF connections
    SF1 <--> FL
    SF2 <--> FL
    FL <--> AP
    AP <--> PE

    SF1 --> EIN
    SF1 --> TB
    SF2 --> CRM

    %% Integration connections
    PE --> MW
    AP <--> API
    MW <--> API

    %% External connections
    API <-->|"REST/SOAP"| SAP
    API <-->|"REST"| NET
    MW <-->|"CDC"| MC
    MW --> PAR
    MW -->|"ETL"| DW
    API -->|"Files"| S3

    %% Node Styling - Users (purple pastel)
    style U1 fill:#ede9fe,stroke:#6d28d9,color:#1f2937
    style U2 fill:#ede9fe,stroke:#6d28d9,color:#1f2937
    style U3 fill:#ede9fe,stroke:#6d28d9,color:#1f2937

    %% Node Styling - Salesforce Core (cyan pastel)
    style SF1 fill:#cffafe,stroke:#0e7490,color:#1f2937
    style SF2 fill:#cffafe,stroke:#0e7490,color:#1f2937
    style SF3 fill:#cffafe,stroke:#0e7490,color:#1f2937

    %% Node Styling - Automation (indigo pastel)
    style FL fill:#e0e7ff,stroke:#4338ca,color:#1f2937
    style AP fill:#ede9fe,stroke:#6d28d9,color:#1f2937
    style PE fill:#ccfbf1,stroke:#0f766e,color:#1f2937

    %% Node Styling - AI (pink pastel)
    style EIN fill:#fce7f3,stroke:#be185d,color:#1f2937
    style TB fill:#fce7f3,stroke:#be185d,color:#1f2937
    style CRM fill:#fce7f3,stroke:#be185d,color:#1f2937

    %% Node Styling - Integration (orange pastel)
    style MW fill:#ffedd5,stroke:#c2410c,color:#1f2937
    style API fill:#ffedd5,stroke:#c2410c,color:#1f2937

    %% Node Styling - External (green pastel)
    style SAP fill:#d1fae5,stroke:#047857,color:#1f2937
    style NET fill:#d1fae5,stroke:#047857,color:#1f2937
    style MC fill:#d1fae5,stroke:#047857,color:#1f2937
    style PAR fill:#d1fae5,stroke:#047857,color:#1f2937
    style DW fill:#fef3c7,stroke:#b45309,color:#1f2937
    style S3 fill:#fef3c7,stroke:#b45309,color:#1f2937

    %% Subgraph Styling - transparent with dark dashed borders
    style users fill:transparent,stroke:#6d28d9,stroke-dasharray:5
    style salesforce fill:transparent,stroke:#0e7490,stroke-dasharray:5
    style core fill:transparent,stroke:#0e7490,stroke-dasharray:5
    style automation fill:transparent,stroke:#4338ca,stroke-dasharray:5
    style ai fill:transparent,stroke:#be185d,stroke-dasharray:5
    style integration fill:transparent,stroke:#c2410c,stroke-dasharray:5
    style external fill:transparent,stroke:#047857,stroke-dasharray:5
    style erp fill:transparent,stroke:#047857,stroke-dasharray:5
    style marketing fill:transparent,stroke:#047857,stroke-dasharray:5
    style data fill:transparent,stroke:#b45309,stroke-dasharray:5
```

## Mermaid Template - Agentforce Architecture

```mermaid
flowchart TB
    subgraph channels["📱 Channels"]
        WEB["🌐 Web Chat<br/><small>Embedded</small>"]
        SMS["💬 SMS<br/><small>Twilio</small>"]
        WHATS["📱 WhatsApp<br/><small>Business</small>"]
        SLACK["💼 Slack<br/><small>Enterprise</small>"]
    end

    subgraph agentforce["🤖 Agentforce"]
        direction TB

        subgraph agents["AI Agents"]
            SA["🎧 Service Agent<br/><small>Customer Support</small>"]
            SDA["📞 SDR Agent<br/><small>Lead Qualification</small>"]
            COACH["🎯 Sales Coach<br/><small>Guidance</small>"]
        end

        subgraph topics["Topics & Actions"]
            T1["📦 Order Status<br/><small>Track, Update</small>"]
            T2["🔄 Return Request<br/><small>RMA, Refund</small>"]
            T3["✅ Lead Qualify<br/><small>Score, Route</small>"]
            A1["⚡ Apex Actions<br/><small>Custom Logic</small>"]
            A2["🔄 Flow Actions<br/><small>Automation</small>"]
        end

        subgraph foundation["Foundation"]
            DM["☁️ Data Cloud<br/><small>Unified Profile</small>"]
            TRUST["🔐 Trust Layer<br/><small>Guardrails</small>"]
            PROMPT["📝 Prompt Builder<br/><small>Templates</small>"]
        end
    end

    subgraph backend["⚙️ Backend"]
        APEX["⚡ Apex Services<br/><small>Business Logic</small>"]
        FLOW["🔄 Flow Orchestration<br/><small>Processes</small>"]
        INT["🔗 Integrations<br/><small>Named Creds</small>"]
    end

    subgraph datasources["💾 Data Sources"]
        CRM[("💼 CRM Data<br/><small>Accounts, Cases</small>")]
        EXT[("🏭 External Data<br/><small>ERP, APIs</small>")]
        KB[("📚 Knowledge Base<br/><small>Articles</small>")]
    end

    %% Channel to Agent
    WEB --> SA
    SMS --> SA
    WHATS --> SA
    SLACK --> SDA
    SLACK --> COACH

    %% Agent to Topics
    SA --> T1
    SA --> T2
    SDA --> T3

    %% Topics to Actions
    T1 --> A1
    T2 --> A2
    T3 --> A1

    %% Foundation connections
    agents --> DM
    agents --> TRUST
    topics --> PROMPT

    %% Backend connections
    A1 --> APEX
    A2 --> FLOW
    APEX --> INT

    %% Data connections
    DM --> CRM
    DM --> EXT
    TRUST --> KB

    %% Node Styling - Channels (slate pastel)
    style WEB fill:#f1f5f9,stroke:#334155,color:#1f2937
    style SMS fill:#f1f5f9,stroke:#334155,color:#1f2937
    style WHATS fill:#f1f5f9,stroke:#334155,color:#1f2937
    style SLACK fill:#f1f5f9,stroke:#334155,color:#1f2937

    %% Node Styling - Agents (pink pastel)
    style SA fill:#fce7f3,stroke:#be185d,color:#1f2937
    style SDA fill:#fce7f3,stroke:#be185d,color:#1f2937
    style COACH fill:#fce7f3,stroke:#be185d,color:#1f2937

    %% Node Styling - Topics (purple pastel)
    style T1 fill:#ede9fe,stroke:#6d28d9,color:#1f2937
    style T2 fill:#ede9fe,stroke:#6d28d9,color:#1f2937
    style T3 fill:#ede9fe,stroke:#6d28d9,color:#1f2937

    %% Node Styling - Actions (indigo pastel)
    style A1 fill:#e0e7ff,stroke:#4338ca,color:#1f2937
    style A2 fill:#e0e7ff,stroke:#4338ca,color:#1f2937

    %% Node Styling - Foundation (teal pastel)
    style DM fill:#ccfbf1,stroke:#0f766e,color:#1f2937
    style TRUST fill:#ccfbf1,stroke:#0f766e,color:#1f2937
    style PROMPT fill:#ccfbf1,stroke:#0f766e,color:#1f2937

    %% Node Styling - Backend (cyan pastel)
    style APEX fill:#cffafe,stroke:#0e7490,color:#1f2937
    style FLOW fill:#cffafe,stroke:#0e7490,color:#1f2937
    style INT fill:#ffedd5,stroke:#c2410c,color:#1f2937

    %% Node Styling - Data (amber pastel)
    style CRM fill:#fef3c7,stroke:#b45309,color:#1f2937
    style EXT fill:#fef3c7,stroke:#b45309,color:#1f2937
    style KB fill:#fef3c7,stroke:#b45309,color:#1f2937

    %% Subgraph Styling - transparent with dark dashed borders
    style channels fill:transparent,stroke:#334155,stroke-dasharray:5
    style agentforce fill:transparent,stroke:#be185d,stroke-dasharray:5
    style agents fill:transparent,stroke:#be185d,stroke-dasharray:5
    style topics fill:transparent,stroke:#6d28d9,stroke-dasharray:5
    style foundation fill:transparent,stroke:#0f766e,stroke-dasharray:5
    style backend fill:transparent,stroke:#0e7490,stroke-dasharray:5
    style datasources fill:transparent,stroke:#b45309,stroke-dasharray:5
```

## ASCII Fallback Template

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM LANDSCAPE                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  👥 USERS                                                                   │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                   │
│  │  Sales Reps   │  │   Managers    │  │   Partners    │                   │
│  │  (Mobile)     │  │  (Desktop)    │  │   (Portal)    │                   │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘                   │
└──────────│──────────────────│──────────────────│────────────────────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ☁️ SALESFORCE PLATFORM                                                     │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  CORE CRM                                                              │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │ │
│  │  │ Sales Cloud │  │Service Cloud│  │ Experience  │                    │ │
│  │  │             │  │             │  │   Cloud     │                    │ │
│  │  └──────┬──────┘  └──────┬──────┘  └─────────────┘                    │ │
│  └─────────│────────────────│────────────────────────────────────────────┘ │
│            │                │                                               │
│  ┌─────────▼────────────────▼────────────────────────────────────────────┐ │
│  │  AUTOMATION                                                            │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │ │
│  │  │    Flows    │──│    Apex     │──│  Platform   │                    │ │
│  │  │             │  │             │  │   Events    │                    │ │
│  │  └─────────────┘  └──────┬──────┘  └──────┬──────┘                    │ │
│  └──────────────────────────│────────────────│───────────────────────────┘ │
└─────────────────────────────│────────────────│──────────────────────────────┘
                              │                │
                              ▼                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  🔄 INTEGRATION LAYER                                                       │
│  ┌─────────────────────────┐  ┌─────────────────────────┐                  │
│  │       MuleSoft          │  │      API Gateway        │                  │
│  │      Anypoint           │──│                         │                  │
│  └───────────┬─────────────┘  └───────────┬─────────────┘                  │
└──────────────│────────────────────────────│─────────────────────────────────┘
               │                            │
               ▼                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  🏢 EXTERNAL SYSTEMS                                                        │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐ │
│  │        ERP          │  │      Marketing      │  │    Data Storage     │ │
│  │  ┌───────┬───────┐  │  │  ┌───────┬───────┐  │  │  ┌───────┬───────┐  │ │
│  │  │  SAP  │NetSuit│  │  │  │  MC   │Pardot │  │  │  │Snowflk│  S3   │  │ │
│  │  └───────┴───────┘  │  │  └───────┴───────┘  │  │  └───────┴───────┘  │ │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Types (Pastel Colors)

| Category | Examples | Icon | Pastel Fill | Dark Stroke |
|----------|----------|------|-------------|-------------|
| Users | Sales, Service, Partners | 👥 | `#ede9fe` | `#6d28d9` |
| Salesforce Clouds | Sales, Service, Marketing | ☁️ | `#cffafe` | `#0e7490` |
| Automation | Flow, Apex, Events | ⚡ | `#e0e7ff` | `#4338ca` |
| AI/Analytics | Einstein, Tableau, CRM Analytics | 🤖 | `#fce7f3` | `#be185d` |
| Integration | MuleSoft, API Gateway | 🔗 | `#ffedd5` | `#c2410c` |
| External Systems | ERP, Marketing, Data | 🏢 | `#d1fae5` | `#047857` |
| Storage | Database, Data Lake, Files | 💾 | `#fef3c7` | `#b45309` |

## Connection Types

| Pattern | Description | Arrow |
|---------|-------------|-------|
| Sync Request/Response | REST API call | `<-->` |
| Async (Event-based) | Platform Events, CDC | `-->` |
| Batch/ETL | Scheduled data load | `-->` (dashed) |
| Real-time streaming | CometD, Pub/Sub | `==>` |

## Customization Points

- Replace example systems with actual integrations
- Add or remove clouds based on implementation
- Include specific API names and versions
- Show data flow direction and volumes
