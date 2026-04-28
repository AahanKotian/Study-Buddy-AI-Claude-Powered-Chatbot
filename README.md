# 📚 Study Buddy AI — Claude-Powered Chatbot

A Python chatbot that uses the **Anthropic Claude API** to act as a personal study tutor. Switch between 5 expert personas — Python tutor, math coach, science explainer, history guide, or general study buddy. Features a polished dark-themed chat UI with full conversation memory.

---

## 🖥️ App Preview

> Run → open `http://127.0.0.1:5000`

- **5 topic modes** — each with a custom system prompt shaping Claude's personality
- **Full conversation memory** — Claude remembers everything you said in the session
- **Markdown rendering** — code blocks, bold text formatted beautifully in chat
- **Typing indicator** — animated dots while Claude is thinking
- **Example prompts** — click chips to get started instantly

---

## 🤖 The 5 Study Personas

| Topic | Persona | Style |
|---|---|---|
| 📚 General | Study Buddy | Warm, encouraging, uses analogies |
| 🐍 Python | Python Tutor | Code-first, explains every line |
| 🔢 Math | Math Tutor | Step-by-step, Socratic method |
| 🔬 Science | Science Explainer | Wonder-inducing, thought experiments |
| 🏛️ History | History Guide | Storytelling, cause and consequence |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `anthropic` SDK | Connect to Claude API, send/receive messages |
| **Prompt Engineering** | System prompts that shape Claude's personality |
| **Conversation History** | Full chat history sent on every API call |
| `flask` | Web server + REST API at `/chat` |
| HTML/CSS/JS | Dark-themed chat UI with markdown rendering |

---

## 🚀 How to Run

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/study-buddy-ai.git
cd study-buddy-ai
```

**2. Install dependencies**
```bash
pip install anthropic flask
```

**3. Get your Claude API key**
- Go to [https://console.anthropic.com](https://console.anthropic.com)
- Sign up → click **API Keys** → **Create Key**
- Copy the key

**4. Add your API key**

Open `study_buddy.py` and replace:
```python
API_KEY = "YOUR_API_KEY_HERE"
```
with your actual key. Or set it as an environment variable:
```bash
# Windows
set ANTHROPIC_API_KEY=your_key_here

# Mac/Linux
export ANTHROPIC_API_KEY=your_key_here
```

**5. Run the app**
```bash
python study_buddy.py
```

**6. Open your browser**
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
study-buddy-ai/
│
├── study_buddy.py    # Full chatbot — Claude API + Flask + UI
└── README.md
```

---

## 🧠 Key Concepts Demonstrated

### 1. Anthropic SDK
```python
client = anthropic.Anthropic(api_key=API_KEY)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=system_prompt,   # shapes the AI's personality
    messages=messages       # full conversation history
)
reply = response.content[0].text
```

### 2. Prompt Engineering
Each topic has a crafted system prompt that controls Claude's behavior:
```python
"system": """You are an expert Python tutor for beginners.
- Always include working code examples
- Explain what each line does in simple terms
- Point out common mistakes and how to avoid them..."""
```

### 3. Conversation Memory
Claude has no built-in memory — we maintain it ourselves by sending the full chat history on every call:
```python
history.append({"role": "user",      "content": user_message})
# ... get Claude's reply ...
history.append({"role": "assistant", "content": claude_reply})
# Next call sends the entire history again
```

### 4. REST API with Flask
```python
@app.route("/chat", methods=["POST"])
def api_chat():
    data     = request.get_json()
    messages = data.get("messages", [])
    topic    = data.get("topic", "general")
    reply    = chat_with_claude(messages, topic)
    return jsonify({"reply": reply})
```

---

## 💡 Example Conversations

**Python Tutor:**
> *"Explain Python decorators"*
> → Gets a clear explanation with a working `@decorator` example and line-by-line breakdown

**Math Tutor:**
> *"Solve x² - 5x + 6 = 0"*
> → Walks through factoring step by step, then asks you to try a similar problem

**History Guide:**
> *"What caused World War 1?"*
> → A narrative about Franz Ferdinand, alliance systems, and the powder-keg metaphor

---

## 🧠 What I Learned

- How to use the **Anthropic Python SDK** to call Claude
- What **prompt engineering** is — how system prompts shape AI behavior
- How to implement **conversation memory** by managing history manually
- How to build a **REST API** that wraps an AI model
- How to connect a **JavaScript frontend** to a Python Flask backend
- Error handling for **API authentication** and **rate limits**

---

*This is Project 5 of 5 in my Python Data/ML learning roadmap.*

---

## 🗺️ Full Learning Roadmap

| # | Project | Skills |
|---|---|---|
| 1 | EDA Dashboard | pandas, matplotlib, seaborn |
| 2 | House Price Predictor | scikit-learn, regression, ML pipeline |
| 3 | Movie Recommender | cosine similarity, collaborative filtering, Flask |
| 4 | Sentiment Analyzer | NLP, TF-IDF, text preprocessing, Flask |
| **5** | **Study Buddy AI** | **Claude API, prompt engineering, chatbot architecture** |
