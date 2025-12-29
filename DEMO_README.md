# Magentic Multi-Agent Demo Scripts

This folder contains demonstration scripts showcasing the power of the **Magentic Pattern** - where multiple specialized AI agents collaborate to solve complex tasks.

## 🎯 What is Magentic?

Magentic is a multi-agent orchestration pattern where:
- **Multiple AI agents** with different specializations work together
- A **Manager agent** coordinates and delegates tasks
- Agents **communicate** and share information
- Complex problems are **solved collaboratively**

Think of it as creating an AI team instead of relying on a single AI!

---

## 📁 Demo Files

### 1. `magentic_quick_demo.py` ⚡ (RECOMMENDED START)
**Duration:** ~2 minutes  
**Purpose:** Fast introduction to Magentic

Shows a simple example where:
- Researcher finds cloud provider information
- Analyst calculates market share and revenue
- Manager coordinates the collaboration

**Run it:**
```powershell
python magentic_quick_demo.py
```

### 2. `magentic_demo.py` 🎪 (COMPREHENSIVE)
**Duration:** ~10-15 minutes  
**Purpose:** Full showcase with 5 different scenarios

Demonstrates:
1. **Quick Research** - Single agent focused work
2. **Cost Calculator** - Financial analysis with code
3. **Math Analysis** - Complex calculations
4. **Business Analysis** - Research + Analysis collaboration
5. **Technical Report** - Full team (Research + Analysis + Writing)

**Run it:**
```powershell
python magentic_demo.py
```

### 3. `Magentic.py` 📊 (ORIGINAL)
**Duration:** ~3-5 minutes  
**Purpose:** Real-world example - ML model energy efficiency report

This is the original script that generates a detailed technical report comparing:
- ResNet-50, BERT-base, and GPT-2
- Energy consumption and CO2 emissions
- Recommendations by task type

**Run it:**
```powershell
python Magentic.py
```

---

## 🚀 Quick Start

1. **Make sure you're authenticated to Azure:**
   ```powershell
   az login
   ```

2. **Run the quick demo first:**
   ```powershell
   python magentic_quick_demo.py
   ```

3. **If you want to see more scenarios:**
   ```powershell
   python magentic_demo.py
   ```

---

## 🎓 What You'll Learn

### Key Concepts Demonstrated:

1. **🤝 Agent Specialization**
   - Researcher: Information gathering
   - Analyst: Data analysis and computation
   - Writer: Content creation
   - Manager: Team coordination

2. **🔄 Workflow Orchestration**
   - Manager breaks down complex tasks
   - Delegates to appropriate specialists
   - Coordinates information flow

3. **💪 Collaborative Problem Solving**
   - Tasks too complex for single agents
   - Agents share findings and build on each other's work
   - Results are more comprehensive and accurate

4. **⚙️ Configuration & Control**
   - `max_round_count`: Limit total interactions
   - `max_stall_count`: Prevent infinite loops
   - `max_reset_count`: Allow recovery from errors

---

## 📊 Use Cases Shown

| Demo | Agents Used | Real-World Application |
|------|-------------|------------------------|
| Quick Demo | Researcher + Analyst | Market research reports |
| Business Analysis | Researcher + Analyst | Competitive analysis |
| Technical Report | All 3 specialists | White paper generation |
| Cost Calculator | Analyst only | Financial modeling |
| Math Analysis | Analyst only | Scientific computation |

---

## 🛠️ Customization

Want to create your own demo? Here's the pattern:

```python
# 1. Create specialized agents
researcher = ChatAgent(name="Researcher", ...)
analyst = ChatAgent(name="Analyst", tools=HostedCodeInterpreterTool(), ...)
manager = ChatAgent(name="Manager", ...)

# 2. Build workflow
workflow = (
    MagenticBuilder()
    .participants(researcher=researcher, analyst=analyst)
    .with_standard_manager(agent=manager, max_round_count=15)
    .build()
)

# 3. Define task
task = "Your complex task here..."

# 4. Run and get results
async for event in workflow.run_stream(task):
    if isinstance(event, WorkflowOutputEvent):
        # Process results
```

---

## 🎯 Best Practices

1. **Start Simple**: Use `magentic_quick_demo.py` to understand the basics
2. **Choose Right Agents**: Match agent skills to task requirements
3. **Set Limits**: Configure `max_round_count` to prevent runaway execution
4. **Clear Instructions**: Give each agent clear role descriptions
5. **Specific Tasks**: Well-defined tasks get better results

---

## 🔍 Troubleshooting

**Script runs but no output?**
- Check that the event handler is extracting `message.text`
- Ensure `WorkflowOutputEvent` is being processed

**Too many API calls / rate limiting?**
- Reduce `max_round_count`
- Simplify the task
- Add delays between demos

**Agents not collaborating well?**
- Review agent instructions for clarity
- Ensure task requires multiple skills
- Check that manager has good coordination instructions

---

## 📚 Learn More

- **Agent Framework Docs**: [Agent Framework Documentation]
- **Magentic Pattern**: Multi-agent orchestration for complex tasks
- **Azure OpenAI**: Powering the underlying AI models

---

## 🎬 Demo Tips for Presentations

1. **Start with Quick Demo** - Gets audience engaged quickly
2. **Show the Code** - Let people see how simple the setup is
3. **Highlight Collaboration** - Point out when agents work together
4. **Compare to Single Agent** - Show what's hard for one AI
5. **Live Modify Tasks** - Change the task to show flexibility

---

## 🌟 Key Takeaway

**The Magentic pattern enables AI systems to work like human teams** - with specialized roles collaborating towards a common goal. This is more powerful than a single generalist AI!

---

*Happy Demoing! 🎉*
