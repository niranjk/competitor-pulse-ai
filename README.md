# PulseAI: Autonomous GTM Intelligence Agent

**PulseAI** is an AI-powered Go-To-Market (GTM) intelligence platform that autonomously researches competitors in real-time, surfaces critical business signals, and generates personalized sales outreach—enabling GTM teams to act on competitive intelligence at scale.

## 🎯 Problem & Solution

### The Challenge
Sales, marketing, and revenue operations teams need real-time competitive intelligence to win deals. The web has this data, but most GTM teams lack reliable access at scale. Manual research is slow, inconsistent, and doesn't provide structured intelligence that can be actioned.

**PulseAI solves this by:**
- 🔍 **Autonomously researching competitors** in real-time using live web data
- 📊 **Extracting structured intelligence** (pricing changes, hiring signals, market moves)
- 🤖 **Analyzing with AI** to surface actionable GTM insights
- ✉️ **Generating sales outreach** based on real competitive signals
- 🔌 **Integrating with GTM workflows** via structured CRM-ready data

---

## ✨ Key Features

### 1. **Real-Time Competitor Research**
- Live web search with Google/Bing/Yandex
- Automated website scraping with bot detection bypass
- LinkedIn hiring and company data extraction
- Batch processing for scale

### 2. **Intelligent Signal Extraction**
- **Pricing Changes**: Detects tier updates and pricing model shifts
- **Hiring Signals**: Identifies headcount expansion and strategic department growth
- **Market Moves**: Surfaces business direction from real data
- **Strategic Intent**: AI-powered analysis of competitor moves

### 3. **AI-Powered Analysis**
- GPT-4o powered analysis via AI/ML API
- Structured JSON output for seamless CRM integration
- Guardrail-protected validation to eliminate hallucinations
- Confidence scoring and source attribution

### 4. **Personalized Sales Outreach**
- Autonomous SDR copywriting based on competitive signals
- High-intent email sequences
- Multi-variant personalization
- CRM-ready data export

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   User Interface (Streamlit)                 │
│              Toggle MCP Mode | Configure Target              │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
    [MCP Mode]                     [Standard Mode]
        │                                 │
        ▼                                 ▼
┌──────────────────────────┐    ┌─────────────────┐
│ Bright Data MCP Server   │    │ Fallback Data   │
│ - Search Engine          │    │ - Mock Data     │
│ - Web Scraping           │    │ - Cached Intel  │
│ - LinkedIn Data          │    └─────────────────┘
│ - Batch Processing       │              │
└──────────────┬───────────┘              │
               │                          │
               └──────────────┬───────────┘
                              │
                    ┌─────────▼────────────┐
                    │  Research Pipeline   │
                    │  (MCP Tools)         │
                    │  Collect & Aggregate │
                    └──────────┬───────────┘
                              │
                    ┌─────────▼────────────┐
                    │   AI/ML API (GPT-4o) │
                    │   Extract Signals    │
                    │   Validate Data      │
                    │   Apply Guardrails   │
                    └──────────┬───────────┘
                              │
                    ┌─────────▼────────────┐
                    │ Outreach Generation  │
                    │ Sales Copywriting    │
                    │ CRM Data Package     │
                    └──────────┬───────────┘
                              │
                    ┌─────────▼────────────┐
                    │ CRM-Ready Output     │
                    │ JSON Export          │
                    │ Email Sequences      │
                    └──────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- API Keys:
  - **Bright Data Token**: Get from https://brightdata.com/cp/setting/users
  - **AI/ML API Key**: Get from https://aimlapi.com

### Installation

```bash
# Clone/navigate to project
cd CompetitorPulseAI

# Install dependencies (already in pyproject.toml)
pip install -r requirements.txt

# Or with uv
uv sync
```

### Configuration

Create `.env` file:
```bash
# Required for real-time MCP research
BRIGHTDATA_API_TOKEN=your_bright_data_api_token

# Required for AI analysis
AIML_API_KEY=your_aiml_api_key

# Optional settings
MCP_ENABLED=true
USE_REAL_TIME_RESEARCH=true
```

### Run the App

```bash
python -m streamlit run src/app.py
```

Opens at: `http://localhost:8501`

### How to Use

1. **Enable MCP Research** (toggle in sidebar)
2. **Enter Competitor Name** (e.g., "Linear", "Notion", "Figma")
3. **Enter Company URL** (e.g., "https://linear.app")
4. **Trigger Agent Framework** (click button)
5. **Monitor Logs** in real-time
6. **View Results**:
   - Market Analyst: Key intelligence
   - Guardrail Audit Logs: Execution trace
   - MCP Research Data: Raw tool outputs
   - CRM Data Package: Export-ready format

---

## 📊 Example Output

### Input
- Competitor: `Linear`
- URL: `https://linear.app`

### MCP Research Results
```
✅ MCP Tools Used: search_engine, scrape_as_markdown, web_data_linkedin

Search Results: [Current news, pricing changes, recent announcements]
Pricing Information: [Extracted tiers: Free, Starter, Professional, Enterprise]
LinkedIn Profile: [Company size growth, hiring in engineering]
```

### Intelligence Extracted
```json
{
  "has_pricing_changed": true,
  "detected_tiers": ["Free", "Starter", "Professional", "Enterprise"],
  "pricing_metrics": ["$0", "$20/user/month", "$80/user/month", "Custom"],
  "hiring_signals": [
    "5 Software Engineers",
    "2 Product Managers",
    "3 Sales Engineers"
  ],
  "raw_justification_quotes": [
    "Linear recently updated Professional tier pricing",
    "Expanding engineering team indicates product development focus"
  ]
}
```

### Generated Outreach
```
Subject: We noticed your expansion into enterprise sales

Hi [Name],

I noticed Linear recently strengthened your enterprise team with new sales engineering hires. 
This tells me you're targeting larger deals with more complex implementations.

Our platform has helped similar companies reduce implementation time by 40% - potentially 
critical as you scale your enterprise motion.

Would a brief 15-min chat make sense to explore?

Best,
[Your Name]
```

---

## 🔧 Technical Stack

### Core Technologies
- **Framework**: LangChain + LangGraph (agentic workflows)
- **UI**: Streamlit (real-time interface)
- **LLM**: OpenAI GPT-4o (via AI/ML API)
- **Data Source**: Bright Data MCP Server (live web intelligence)
- **Async**: Python asyncio (non-blocking operations)
- **Validation**: Pydantic (data integrity)

### Key Components

| Component | Purpose |
|-----------|---------|
| `src/core/mcp_client.py` | Bright Data MCP integration |
| `src/core/graph.py` | Async research + analysis pipeline |
| `src/core/state.py` | Type-safe state management |
| `src/core/llm_client.py` | AI/ML API configuration |
| `src/config.py` | Environment configuration |
| `src/ui/app_ui.py` | Streamlit dashboard |

---

## 🌐 Available MCP Tools

When connected to Bright Data MCP, PulseAI can access:

| Tool | Data Type | Use Case |
|------|-----------|----------|
| `search_engine` | Web search results | News, announcements |
| `scrape_as_markdown` | Website content | Pricing pages, features |
| `search_engine_batch` | Bulk searches | Multi-query research |
| `scrape_batch` | Bulk scraping | Homepage, about, careers |
| `web_data_linkedin` | Company profiles | Hiring, growth |
| `web_data_amazon` | Product data | E-commerce research |
| `browser_automation` | Complex navigation | Dynamic content |

---

## 🎯 Use Cases

### Sales Development
- Research accounts before outreach
- Identify buying signals and expansion
- Generate personalized cold emails

### Competitive Intelligence
- Monitor competitor pricing changes
- Track hiring and team expansion
- Identify market positioning shifts

### Marketing Intelligence
- Analyze competitor messaging
- Track market trends
- Monitor share of voice

### Revenue Operations
- Build account enrichment pipelines
- Create buying signal detection systems
- Surface market opportunities

---

## 📈 Performance

### Speed
- **Standard Mode**: Instant (cached data)
- **MCP Mode**: 30-60 seconds (real-time data)

### Accuracy
- **Data Validation**: Guardrail-protected (Pydantic)
- **Hallucination Prevention**: Source attribution required
- **Confidence Scoring**: Evidence-based signals

### Scalability
- **Bright Data Free Tier**: 5,000 requests/month
- **Batch Processing**: Multi-competitor research
- **Async Architecture**: Non-blocking operations

---

## 🔐 Security & Compliance

- **API Keys**: Stored in `.env`, never committed to git
- **Data Privacy**: No sensitive data stored locally
- **Token Usage**: Transparent monitoring
- **Rate Limiting**: Respects Bright Data quotas

---

## 📋 Project Structure

```
CompetitorPulseAI/
├── src/
│   ├── app.py                    # Main entry point
│   ├── config.py                 # Configuration
│   ├── core/
│   │   ├── mcp_client.py         # MCP integration
│   │   ├── graph.py              # Research pipeline
│   │   ├── state.py              # State models
│   │   └── llm_client.py         # LLM config
│   └── ui/
│       └── app_ui.py             # Streamlit UI
├── pyproject.toml                # Dependencies
├── verify_mcp_setup.py           # Setup verification
└── README.md                     # This file
```

---

## 🧪 Testing

### Verify Setup
```bash
python verify_mcp_setup.py
```

Should show: ✅ All 4 tests passed

### Test with Example Data
1. Start app: `streamlit run src/app.py`
2. Leave MCP toggle OFF (standard mode)
3. Enter "Linear" as competitor
4. See instant results with mock data
5. Enable MCP toggle
6. Add Bright Data token to `.env`
7. Re-run to see live results

---

## 🚀 Deployment

### Local Development
```bash
streamlit run src/app.py
```

### Production
```bash
# Using Streamlit Cloud
streamlit deploy

# Or Docker
docker build -t pulseai .
docker run -e BRIGHTDATA_API_TOKEN=$TOKEN -e AIML_API_KEY=$KEY pulseai
```

---

## 📊 Hackathon Track: GTM Intelligence

PulseAI directly addresses the **Track 1: GTM Intelligence** challenge:

✅ **Continuously monitor competitors** in real-time
✅ **Surface intelligence directly into GTM workflows** (CRM-ready JSON)
✅ **Replace manual research** with autonomous agents
✅ **Give AI agents live web context** via Bright Data MCP
✅ **Competitive monitoring** (pricing, hiring, messaging)
✅ **Account enrichment** with structured data
✅ **Always-on intelligence** at scale

---

## 🎓 Key Innovations

1. **MCP-First Architecture**: Native Bright Data MCP integration for real-time data
2. **Async-Native Pipeline**: Non-blocking research + analysis workflow
3. **Intelligent Signal Extraction**: AI-powered structured data from unstructured web content
4. **Guardrail Validation**: Hallucination-free intelligence
5. **CRM Integration Ready**: JSON export for seamless workflow integration

---

## 🤝 Contributing

To extend PulseAI:

1. Add new MCP tools in `research_competitor()` method
2. Extend signal extraction in `analyze_with_mcp_context()`
3. Customize outreach in `generate_outreach_with_mcp()`
4. Add new research types in configuration

---

## 📞 Support

- **Bright Data Docs**: https://docs.brightdata.com/ai/mcp-server
- **AI/ML API Docs**: https://aimlapi.com/api-reference
- **LangChain Docs**: https://python.langchain.com/docs
- **GitHub Issues**: Report bugs or feature requests

---

## 📄 License

MIT License - See LICENSE file

---

## 🏆 Hackathon Submission

**Project**: PulseAI - Autonomous GTM Intelligence Agent  
**Track**: GTM Intelligence (Track 1)  
**Challenge**: Enable GTM teams with always-on, autonomous competitive intelligence  
**Technology**: LangChain + Bright Data MCP + GPT-4o + Streamlit  

**Why PulseAI Wins**:
- ✅ Fully autonomous agent (no manual intervention)
- ✅ Real-time web intelligence (Bright Data MCP integration)
- ✅ Structured intelligence (JSON for CRM)
- ✅ Production-ready code (error handling, logging, validation)
- ✅ Scalable architecture (batch processing, async)
- ✅ Hackathon-focused (complete, running, ready to demo)

---

**Built with ❤️ for GTM teams who win with intelligence.**

