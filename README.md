# KPI-AI-agent-Langchain
A comprehensive AI-powered system for KPI analysis, predictive analytics, and decision support using LangChain.

## Features

- **Multi-source Data Integration**: CSV files and Power BI datasets
- **Exploratory Data Analysis**: Automated EDA with insights
- **Predictive Analytics**: Forecasting and trend analysis
- **Decision Support**: AHP-based multi-criteria decision making
- **Memory System**: Context retention and learning
- **Interactive Dashboard**: Streamlit-based UI
- **Modular Architecture**: Extensible and maintainable design

## 🏗️ Architecture

┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    KPI AI AGENT SYSTEM                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                        MAIN ENTRY                                           │
│                                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                         │
│  │   Dashboard     │    │     CLI         │    │     API         │                         │
│  │  (Streamlit)    │    │   (Terminal)    │    │   (Web API)     │                         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                         │
└─────────────────────────────────┬───────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    CORE ORCHESTRATOR                                        │
│  ┌──────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                                    KPIAgentOrchestrator                              │   │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                   │   │
│  │  │   KPIAgent      │    │   Config        │    │   Factory       │                   │   │
│  │  │                 │    │  (settings.py)  │    │  (factory.py)   │                   │   │
│  │  │ ┌─────────────┐ │    └─────────────────┘    └─────────────────┘                   │   │
│  │  │ │LLM + Tools  │ │                                                                   │   │
│  │  │ │+ Memory     │ │                                                                   │   │
│  │  │ │+ AgentExec  │ │                                                                   │   │
│  │  │ └─────────────┘ │                                                                   │   │
│  │  └─────────────────┘                                                                   │   │
│  └──────────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┬───────────────────────────────────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────────────┐
        ▼                         ▼                                 ▼
┌─────────────────────┐  ┌─────────────────────┐       ┌─────────────────────────────────────┐
│      TOOLS          │  │      MEMORY         │       │      CHAINS                        │
│                     │  │                     │       │                                    │
│  ┌──────────────┐   │  │  ┌──────────────┐   │       │  ┌───────────────────────────────┐ │
│  │ PowerBI      │   │  │  │ Core         │   │       │  │ KPIAnalysisChain             │ │
│  │ ┌──────────┐ │   │  │  │ (core.py)    │   │       │  │ (kpi_analysis.py)            │ │
│  │ │Core      │ │   │  │  └──────────────┘   │       │  └───────────────────────────────┘ │
│  │ │Processor │ │   │  │  ┌──────────────┐   │       │  ┌───────────────────────────────┐ │
│  │ │Queries   │ │   │  │  │ Conversation │   │       │  │ AHPReasoningChain            │ │
│  │ │Tool      │ │   │  │  │ (conversation.│   │       │  │ (ahp_reasoning.py)           │ │
│  │ └──────────┘ │   │  │  │  py)         │   │       │  └───────────────────────────────┘ │
│  └──────────────┘   │  │  └──────────────┘   │       │  ┌───────────────────────────────┐ │
│  ┌──────────────┐   │  │  ┌──────────────┐   │       │  │ EDAAnalysisChain             │ │
│  │ AHP          │   │  │  │ Vector       │   │       │  │ (eda_analysis.py)            │ │
│  │ ┌──────────┐ │   │  │  │ (vector.py)  │   │       │  └───────────────────────────────┘ │
│  │ │Core      │ │   │  │  └──────────────┘   │       │  ┌───────────────────────────────┐ │
│  │ │Config    │ │   │  │  ┌──────────────┐   │       │  │ RecommendationChain          │ │
│  │ │Reasoning │ │   │  │  │ Working      │   │       │  │ (recommendation.py)          │ │
│  │ │Tool      │ │   │  │  │ (working.py) │   │       │  └───────────────────────────────┘ │
│  │ └──────────┘ │   │  │  └──────────────┘   │       │                                    │
│  └──────────────┘   │  │  ┌──────────────┐   │       └─────────────────────────────────────┘
│  ┌──────────────┐   │  │  │ Persistent   │   │
│  │ EDA          │   │  │  │ (persistent. │   │
│  │ ┌──────────┐ │   │  │  │  py)         │   │
│  │ │Core      │ │   │  │  └──────────────┘   │
│  │ │Tool      │ │   │  └──────────────────────┘
│  │ └──────────┘ │   │
│  └──────────────┘   │
│  ┌──────────────┐   │
│  │ Predictive   │   │
│  │ ┌──────────┐ │   │
│  │ │Core      │ │   │
│  │ │Tool      │ │   │
│  │ └──────────┘ │   │
│  └──────────────┘   │
│  ┌──────────────┐   │
│  │ Data         │   │
│  │ ┌──────────┐ │   │
│  │ │Core      │ │   │
│  │ │Tool      │ │   │
│  │ └──────────┘ │   │
│  └──────────────┘   │
│                     │
│  ┌──────────────┐   │
│  │ Factory      │   │
│  │ (factory.py) │   │
│  └──────────────┘   │
└─────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      UTILITIES                                              │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                         │
│  │ DataProcessor   │    │ Validator       │    │ Formatter       │                         │
│  │ (data_processor.│    │ (validator.py)  │    │ (formatter.py)  │                         │
│  │  py)            │    │                 │    │                 │                         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                         │
└─────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    CONFIGURATION                                            │
│  ┌─────────────────┐    ┌─────────────────┐                                                │
│  │ Settings        │    │ AHP Config      │                                                │
│  │ (settings.py)   │    │ (ahp_config.    │                                                │
│  │                 │    │  json)          │                                                │
│  └─────────────────┘    └─────────────────┘                                                │
└─────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      TESTING                                                │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐   │
│  │ Test Tools      │    │ Test Memory     │    │ Test Chains     │    │ Integration     │   │
│  │                 │    │                 │    │                 │    │                 │   │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   DATA SOURCES                                              │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                         │
│  │ CSV Files       │    │ Power BI        │    │ JSON API        │                         │
│  │ (data/*.csv)    │    │ (REST API)      │    │ (External)      │                         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                         │
└─────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   PERSISTENCE                                               │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                         │
│  │ SQLite DB       │    │ Chroma Vector   │    │ Session Files   │                         │
│  │ (kpi_memory.db) │    │ Store           │    │ (.session)      │                         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                         │
└─────────────────────────────────────────────────────────────────────────────────────────────┘

FLOW OF DATA AND CONTROL:
User Input → Main Entry → Core Orchestrator ↔ Tools (PowerBI, AHP, EDA, etc.)
                                    ↕
                          Memory System (Context Retention)
                                    ↕
                          Chain Processing (Reasoning)
                                    ↕
                          Utilities (Processing/Formatting)
                                    ↕
                          Configuration & Data Sources

Component Interaction Flow:
1. User Interface Layer

Dashboard (Streamlit) ──┐
CLI (Terminal) ─────────┤──→ Core Orchestrator
API (Web) ──────────────┘

2. Core Processing Layer

Core Orchestrator
├── KPIAgent (LLM + Tools + Memory)
├── Configuration Management
└── Factory Pattern

3. Tool Ecosystem

Tools Factory
├── PowerBI Tools
│   ├── Core API Client
│   ├── Data Processor
│   ├── Query Builder
│   └── LangChain Tools
├── AHP Tools
│   ├── Core Calculator
│   ├── Config Manager
│   ├── Reasoning Components
│   └── LangChain Tool
├── EDA Tools
│   ├── Core Processor
│   └── LangChain Tool
├── Predictive Tools
│   ├── Core Analyzer
│   └── LangChain Tool
└── Data Tools
    ├── Core Retriever
    └── LangChain Tool

4. Memory System

Memory Factory
├── Core Memory Abstractions
├── Conversation Memory
├── Vector Memory (Semantic)
├── Working Memory (Short-term)
└── Persistent Memory (Long-term)

5. Reasoning Chains

Chain Factory
├── KPI Analysis Chain
├── AHP Reasoning Chain
├── EDA Analysis Chain
└── Recommendation Chain

6. Data Flow

Data Sources → Tools → Memory → Chains → LLM → Response → User Interface
     ↑                                            ↓
Configuration & Utilities ←──────────────────────┘

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/kpi-ai-agent.git
cd kpi-ai-agent
