# 🗓 myRoster

> **From copy-paste chaos to 2-minute submissions**  
> *"The best automation isn't flashy — it's invisible.  It just works."*

[![Live Demo](https://img.shields.io/badge/demo-live-success? style=for-the-badge)](https://myroster.streamlit.app/)
[![Read Article](https://img.shields.io/badge/dev.to-article-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white)(https://dev.to/lfariaus/myroster-from-copypaste-to-2-minute-submissions-dao)
[![Python](https://img.shields.io/badge/python-3.10+-blue? style=for-the-badge&logo=python)(https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)

A lightweight, interactive web app that transforms shift availability submission from a 15-20 minute chore into a **2-minute task**. Built with Streamlit for Excel Building Management and similar shift-based operations.

**📖 [Read the full story on dev.to](https://dev.to/lfariaus/myroster-from-copypaste-to-2-minute-submissions-dao) →**

---

## 🎯 The Problem

Every roster cycle, the same tedious ritual: 
- ❌ Open a spreadsheet, manually tick boxes for 28+ days
- ❌ Triple-check you didn't miss anything
- ❌ Export, draft email, attach file, send
- ❌ 15-20 minutes per employee, every cycle
- ❌ Inconsistent formats causing HR coordination nightmares

**There had to be a better way.**

---

## ✨ The Solution

myRoster automates the entire workflow with a clean, intuitive interface that anyone can use without training. 

### **Key Features**

| Feature | Benefit |
|---------|---------|
| 🤖 **Smart Period Calculation** | Automatically computes the next 4-week roster cycle based on HR's schedule logic |
| 📊 **Spreadsheet-Like Interface** | Familiar grid layout with collapsible weeks—just click checkboxes for available shifts |
| ⚡ **One-Click Weekly Shortcuts** | Fill entire weeks instantly (e.g., "All mornings", "Clear all") |
| 📈 **Real-Time Progress Tracking** | See total shifts selected, coverage percentage, and visual progress bar |
| 📧 **Automated Email Submission** | One button generates CSV + sends professional HTML email to HR with optional CC |

---

## 🚀 Quick Start

### **Try the Live Demo**
👉 **[myroster.streamlit.app](https://myroster.streamlit.app/)**

### **Run Locally**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lfariabr/roster.git
   cd roster
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the app:**
   ```bash
   streamlit run app.py
   ```

4. **Open in your browser:**  
   Navigate to `http://localhost:8501`

### **Using Dev Container (VS Code)**

Open the repository in VS Code and click "Reopen in Container" when prompted.  Everything is pre-configured! 

---

## 📝 How to Use

1. **Enter your name** (and optional email for CC)
2. **Select your available shifts** for each day using the interactive grid
3. **Use weekly shortcuts** to speed up entry (e.g., select all morning shifts)
4. **Preview your submission** with real-time counters showing coverage
5. **Click "Submit"** → CSV generated + email sent automatically

**That's it.  2 minutes, start to finish.**

---

## 🛠️ Tech Stack

### **Current**

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | Python 3.10+ | Core logic, date calculations |
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive web UI (zero JavaScript needed) |
| **Data Processing** | [Pandas](https://pandas.pydata.org/) | Shift matrices, CSV export |
| **Email** | Gmail SMTP (GCP) | Automated delivery with HTML templates |
| **Deployment** | Streamlit Cloud | One-click deploy from GitHub |

### **Future**

Roadmap includes:  **Supabase** (auth + database), **Resend** (transactional emails), **ML** (pattern recognition + RAG assistant), **EmploymentHero API** (direct integration)

📖 [Read about future plans in the article](https://dev.to/lfariaus/myroster-from-copypaste-to-2-minute-submissions-dao#heading-future-roadmap) | 🎯 [View roadmap issue](https://github.com/lfariabr/roster/issues/6)

---

## 📂 Project Structure

```
roster/
│
├── app. py                    # Main Streamlit entry point
├── views/
│   └── rosterView. py         # UI components and logic
├── helpers/
│   └── roster.py             # Roster period calculation
├── services/
│   └── emailService.py       # Email automation
├── requirements.txt          # Python dependencies
└── docs/
    └── CHANGELOG.md          # Development timeline
```

---

## 📊 Impact

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Submission Time** | 15-20 min | ~2 min | **90% reduction** |
| **Format Consistency** | Varies | 100% | **Zero errors** |
| **User Training** | Required | None | **Zero onboarding** |
| **Employee Satisfaction** | Dreaded task | Quick & painless | **🎉** |

---

## 🚀 Future Roadmap

myRoster is evolving from a standalone tool into a comprehensive workforce management platform: 

- **🔔 Multi-Provider Notifications** — Automated reminders via Resend
- **🧠 ML Pattern Recognition** — Predict coverage gaps, identify submission behavior
- **💬 RAG-Powered AI Assistant** — Conversational knowledge base for policies & FAQs
- **🔐 Supabase Backend** — Authentication, saved preferences, historical data
- **🔗 EmploymentHero Integration** — Direct API sync, eliminate CSV copy-paste

**[View detailed roadmap →](https://github.com/lfariabr/roster/issues/6)**

---

## 📖 Learn More

- **📝 [Read the full case study on dev.to](https://dev.to/lfariaus/myroster-from-copypaste-to-2-minute-submissions-dao)** — From problem identification to production deployment
- **📜 [View the changelog](docs/CHANGELOG.md)** — Complete development timeline from Aug-Oct 2025
- **🎯 [See the roadmap issue](https://github.com/lfariabr/roster/issues/6)** — Future features and integrations

---

## 🤝 Contributing

Found a bug or have a feature idea? 

- **🐛 [Open an issue](https://github.com/lfariabr/roster/issues/new)**
- **💡 Check the [roadmap](https://github.com/lfariabr/roster/issues/6)** for planned features
- **🔀 Submit a pull request** with improvements

---

## 👨‍💻 Author

**Luis Faria**  
Building practical tools that solve real problems. 

- 🌐 Portfolio: [luisfaria.dev](https://luisfaria.dev)
- 💼 LinkedIn: [linkedin.com/in/lfariabr](https://www.linkedin.com/in/lfariabr/)
- 🐙 GitHub: [github.com/lfariabr](https://github.com/lfariabr)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## ⭐ Support

If myRoster saved you time or inspired your own automation project: 

- ⭐ Star this repository
- 📝 [Share the article](https://dev.to/lfariaus/myroster-from-copypaste-to-2-minute-submissions-dao)
- 💬 Let me know what you built!

---

**Built with ☕ and automation**  
*"The best automation isn't flashy — it's invisible. It just works."*
