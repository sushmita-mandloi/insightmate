# 🤖 InsightMate
### AI-powered Data Analysis + Placement Assistant

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2.16-green)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37.0-red)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA3.3-orange)](https://groq.com)
[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://insightmate-ckkujyhmwn6gubm7yo6pp8.streamlit.app)

---

## 🚀 Live Demo

**Try it now:** [InsightMate Live App](https://insightmate-ckkujyhmwn6gubm7yo6pp8.streamlit.app)

---

## 🎯 What is InsightMate?

InsightMate is a production-ready dual-mode AI agent that combines:

**📊 Data Analyst Mode**
Upload any CSV dataset and ask questions in plain English. The AI agent autonomously writes and executes Python/SQL code, returns real insights, and generates interactive charts.

**🎯 Placement Assistant Mode**
Upload your resume PDF and get structured extraction of your skills, education, experience, projects, and certifications — powered by LLaMA 3.

---

## ✨ Features

- Natural language data analysis on any CSV
- Auto Python/Pandas code generation and execution
- SQL queries via DuckDB on CSV files
- Interactive Plotly charts (bar, pie, line, scatter)
- PDF resume parsing and structured information extraction
- Dual-mode Streamlit interface
- Deployed on Streamlit Cloud

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| LangChain 0.2.16 | AI Agent framework (ReAct loop) |
| Groq LLaMA 3.3-70b | Free, fast LLM inference |
| Python REPL Tool | Executes Pandas code on CSV data |
| DuckDB | In-memory SQL engine on CSV files |
| Plotly | Interactive data visualizations |
| PyMuPDF | PDF resume text extraction |
| Streamlit | Web UI framework |
| Python-dotenv | Secure API key management |
| Git + GitHub | Version control and CI/CD |

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/sushmita-mandloi/insightmate.git
cd insightmate

# 2. Create virtual environment
python -m venv venv
venv\Scripts\Activate    # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Create a .env file and add:
GROQ_API_KEY=your_groq_api_key_here

# 5. Run the app
streamlit run app/main.py
```

---

## 🔑 API Keys Required

| Key | Where to get | Cost |
|---|---|---|
| GROQ_API_KEY | [console.groq.com](https://console.groq.com) | Free |

---

## 💡 How to Use

**Data Analyst Mode:**
1. Click "Data Analyst Mode"
2. Upload any CSV file
3. Ask questions in the chat: `"What is the average sales by category?"`
4. Use Quick Charts to generate visualizations

**Placement Mode:**
1. Click "Placement Assistant Mode"
2. Upload your resume PDF
3. Click "Parse Resume"
4. View extracted skills, education, experience

---

## 🎯 Sample Queries

---

## 📊 Interview Topics This Project Covers

- AI Agents and ReAct (Reason + Act) loop
- LangChain tools and agent framework
- LLM integration (Groq, LLaMA 3)
- Pandas and DuckDB for data analysis
- PDF parsing with PyMuPDF
- Streamlit for rapid ML app deployment
- Git/GitHub version control
- Environment variable management

---

## 👩‍💻 Author

**Sushmita Mandloi**
- 🎓 Integrated M.Tech in Computer Science (Data Science), VIT Chennai (2022-2027)
- 💼 Data Science Intern at CodeSoft | GSSoC 2026 Contributor
- 🔗 [GitHub](https://github.com/sushmita-mandloi)
- 💻 [LeetCode](https://leetcode.com/sushmita-mandloi08)
- 🏆 [HackerRank](https://hackerrank.com/sushmitamandloi1) — 5 Star SQL

---

## 📄 License

MIT License — feel free to use and modify!

---

## 📁 Project Structure
