# ============================================================
#  AI Study Buddy — Claude-Powered Chatbot
#  Skills: Anthropic SDK, prompt engineering, Flask, REST API
#  Run:    python study_buddy.py
#          Open → http://127.0.0.1:5000
#
#  HOW TO GET YOUR API KEY:
#  1. Go to https://console.anthropic.com
#  2. Sign up / log in → click "API Keys" → "Create Key"
#  3. Paste it below or set env variable: ANTHROPIC_API_KEY=your_key
# ============================================================

# ── 1. IMPORTS ───────────────────────────────────────────────
import os
import json
import anthropic
from flask import Flask, request, jsonify, render_template_string

# ── 2. CONFIGURATION ─────────────────────────────────────────
# Your Claude API key — get one free at https://console.anthropic.com
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "YOUR_API_KEY_HERE")

# The Claude model to use
MODEL = "claude-sonnet-4-20250514"

# ── 3. STUDY TOPICS — PROMPT ENGINEERING ────────────────────
# Each topic has a carefully crafted system prompt.
# The system prompt is what SHAPES how Claude behaves.
# This is the core of "prompt engineering".

TOPICS = {
    "general": {
        "name": "General Study Buddy",
        "emoji": "📚",
        "color": "#4f8ef7",
        "system": """You are a friendly, encouraging study buddy helping a student learn effectively.
Your personality: warm, patient, and genuinely enthusiastic about knowledge.

Your approach:
- Explain concepts clearly using simple language first, then build complexity
- Use analogies and real-world examples whenever possible
- If a student seems confused, try a completely different explanation angle
- Celebrate their progress and curiosity
- Ask follow-up questions to check understanding
- Break complex topics into digestible steps
- Never make the student feel bad for not knowing something

Keep responses focused and not too long — students have limited attention spans.
End responses with an engaging follow-up question when appropriate."""
    },
    "python": {
        "name": "Python Tutor",
        "emoji": "🐍",
        "color": "#3dc97a",
        "system": """You are an expert Python programming tutor for beginners and intermediate learners.
Your personality: precise, practical, and code-first.

Your approach:
- Always include working code examples with every explanation
- Format all code in proper Python with comments
- Explain what each line does in simple terms
- Point out common mistakes and how to avoid them
- Suggest best practices (PEP 8, naming conventions, etc.)
- When debugging, ask to see the exact error message
- Relate programming concepts to real-world scenarios

Rules:
- Never give code without explaining it
- Always test your examples mentally before sharing
- Highlight important Python gotchas (mutable defaults, indentation, etc.)"""
    },
    "math": {
        "name": "Math Tutor",
        "emoji": "🔢",
        "color": "#f7a94f",
        "system": """You are a patient and brilliant math tutor who makes numbers feel intuitive.
Your personality: methodical, encouraging, and Socratic.

Your approach:
- Always show step-by-step working — never skip steps
- Explain the WHY behind each step, not just the HOW
- Use visual descriptions when helpful (imagine a number line, picture a triangle...)
- Offer multiple solution methods when they exist
- Check understanding by asking students to try a similar problem
- Relate abstract math to concrete real-world situations
- If a student gets it wrong, guide them to discover the mistake themselves

Never just give the answer — guide the student to find it."""
    },
    "science": {
        "name": "Science Explainer",
        "emoji": "🔬",
        "color": "#e05adb",
        "system": """You are a passionate science communicator who makes complex science accessible and exciting.
Your personality: curious, rigorous, and wonder-inducing.

Your approach:
- Start with the big picture before diving into details
- Use thought experiments and analogies liberally
- Connect science to everyday phenomena students already know
- Acknowledge scientific uncertainty honestly
- Distinguish between well-established science and cutting-edge research
- Use the Feynman technique: if you can't explain it simply, you don't understand it
- Share surprising or counterintuitive facts to spark curiosity

Cover physics, chemistry, biology, astronomy — whatever the student needs."""
    },
    "history": {
        "name": "History Guide",
        "emoji": "🏛️",
        "color": "#c97b3d",
        "system": """You are a captivating history teacher who brings the past to life through storytelling.
Your personality: narrative-driven, contextual, and thought-provoking.

Your approach:
- Frame historical events as human stories with causes and consequences
- Always provide context — what was happening in the world at that time?
- Draw connections between past events and the present day
- Present multiple historical perspectives, not just the "winner's" view
- Use specific vivid details to make history feel real
- Pose counterfactual questions to stimulate critical thinking
- Help students see patterns and themes across different periods

Make history feel relevant and alive, not a list of dates to memorize."""
    },
}

# ── 4. INITIALIZE ANTHROPIC CLIENT ───────────────────────────
# This creates the connection to Claude's API
client = anthropic.Anthropic(api_key=API_KEY)

# ── 5. CORE CHAT FUNCTION ────────────────────────────────────
def chat_with_claude(messages: list, topic: str = "general") -> str:
    """
    Send a conversation to Claude and get a response.

    messages: list of {"role": "user"/"assistant", "content": "..."}
              This is the full conversation history — Claude has no memory
              between calls, so we send the entire history every time.

    topic:    which system prompt / persona to use
    """
    system_prompt = TOPICS.get(topic, TOPICS["general"])["system"]

    # THE API CALL — this is the heart of the project
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=system_prompt,      # ← shapes Claude's personality & behaviour
        messages=messages          # ← full conversation history
    )

    # Extract the text from Claude's response
    return response.content[0].text

# ── 6. FLASK WEB APP ─────────────────────────────────────────
app = Flask(__name__)

# ── 7. HTML TEMPLATE — POLISHED CHAT UI ─────────────────────
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Study Buddy AI</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<style>
:root {
  --bg:       #0c0c10;
  --surface:  #13131a;
  --border:   #1e1e2e;
  --text:     #e8e8f0;
  --muted:    #5a5a78;
  --accent:   #4f8ef7;
  --user-bg:  #1a1a2e;
  --bot-bg:   #13131a;
  --radius:   14px;
  --font-display: 'Syne', sans-serif;
  --font-body:    'DM Sans', sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:var(--bg);color:var(--text);font-family:var(--font-body)}

/* ── layout ── */
.shell{display:grid;grid-template-columns:260px 1fr;height:100vh;overflow:hidden}

/* ── sidebar ── */
.sidebar{background:var(--surface);border-right:1px solid var(--border);
  display:flex;flex-direction:column;padding:1.5rem 1rem;gap:0.5rem;overflow-y:auto}
.sidebar-logo{font-family:var(--font-display);font-size:1.25rem;font-weight:800;
  color:var(--text);padding:0 0.5rem 1.2rem;border-bottom:1px solid var(--border);margin-bottom:0.5rem;
  letter-spacing:-0.02em}
.sidebar-logo span{color:var(--accent)}
.topic-btn{display:flex;align-items:center;gap:0.75rem;padding:0.7rem 0.85rem;
  border-radius:10px;border:1px solid transparent;cursor:pointer;
  font-family:var(--font-body);font-size:0.88rem;font-weight:500;color:var(--muted);
  background:transparent;transition:all .2s;text-align:left;width:100%}
.topic-btn:hover{background:var(--border);color:var(--text)}
.topic-btn.active{background:var(--border);color:var(--text);border-color:var(--border)}
.topic-btn .dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.topic-emoji{font-size:1.1rem;width:20px;text-align:center}
.sidebar-footer{margin-top:auto;padding-top:1rem;border-top:1px solid var(--border);
  font-size:0.75rem;color:var(--muted);line-height:1.6;padding-left:0.5rem}
.sidebar-footer strong{color:var(--text)}

/* ── main area ── */
.main{display:flex;flex-direction:column;height:100vh;overflow:hidden}

/* ── header ── */
.topbar{padding:1rem 1.5rem;border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
.topbar-title{font-family:var(--font-display);font-size:1.1rem;font-weight:700;
  display:flex;align-items:center;gap:0.6rem}
.topbar-pill{font-size:0.72rem;font-weight:600;padding:0.25rem 0.65rem;
  border-radius:20px;background:var(--border);color:var(--muted);letter-spacing:0.05em;text-transform:uppercase}
.clear-btn{background:transparent;border:1px solid var(--border);color:var(--muted);
  padding:0.4rem 0.9rem;border-radius:8px;cursor:pointer;font-size:0.8rem;
  font-family:var(--font-body);transition:all .2s}
.clear-btn:hover{border-color:var(--muted);color:var(--text)}

/* ── messages ── */
.messages{flex:1;overflow-y:auto;padding:1.5rem;display:flex;flex-direction:column;gap:1rem;
  scrollbar-width:thin;scrollbar-color:var(--border) transparent}
.messages::-webkit-scrollbar{width:4px}
.messages::-webkit-scrollbar-track{background:transparent}
.messages::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}

/* welcome screen */
.welcome{display:flex;flex-direction:column;align-items:center;justify-content:center;
  height:100%;text-align:center;gap:1rem;opacity:0;animation:fadeIn .5s .1s forwards}
.welcome-emoji{font-size:3.5rem;margin-bottom:0.5rem}
.welcome h2{font-family:var(--font-display);font-size:1.6rem;font-weight:800;letter-spacing:-0.03em}
.welcome p{color:var(--muted);max-width:380px;line-height:1.6;font-size:0.9rem}
.welcome-chips{display:flex;flex-wrap:wrap;gap:0.5rem;justify-content:center;margin-top:0.5rem;max-width:420px}
.chip{background:var(--surface);border:1px solid var(--border);border-radius:20px;
  padding:0.45rem 1rem;font-size:0.82rem;cursor:pointer;color:var(--muted);
  transition:all .2s;font-family:var(--font-body)}
.chip:hover{border-color:var(--accent);color:var(--text)}

/* message bubbles */
.msg{display:flex;gap:0.85rem;max-width:82%;animation:slideUp .25s ease}
.msg.user{align-self:flex-end;flex-direction:row-reverse}
.msg.bot {align-self:flex-start}
.avatar{width:32px;height:32px;border-radius:10px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:0.9rem;margin-top:2px}
.avatar.bot-av {background:var(--border)}
.avatar.user-av{background:var(--accent);color:white;font-weight:700;font-size:0.75rem;font-family:var(--font-display)}
.bubble{padding:0.85rem 1.1rem;border-radius:var(--radius);line-height:1.65;font-size:0.9rem;word-break:break-word}
.msg.user .bubble{background:var(--user-bg);border:1px solid var(--border);border-top-right-radius:4px}
.msg.bot  .bubble{background:var(--bot-bg);border:1px solid var(--border);border-top-left-radius:4px}

/* code blocks inside bubbles */
.bubble pre{background:#0a0a0f;border:1px solid var(--border);border-radius:8px;
  padding:0.85rem;margin:0.6rem 0;overflow-x:auto;font-size:0.82rem;line-height:1.5}
.bubble code{font-family:'Fira Code','Courier New',monospace;font-size:0.82rem}
.bubble p:not(:last-child){margin-bottom:0.5rem}
.bubble strong{color:#fff;font-weight:600}

/* typing indicator */
.typing-dot{display:inline-block;width:7px;height:7px;border-radius:50%;
  background:var(--muted);margin:0 2px;animation:blink 1.2s infinite}
.typing-dot:nth-child(2){animation-delay:.2s}
.typing-dot:nth-child(3){animation-delay:.4s}
@keyframes blink{0%,80%,100%{opacity:0.2}40%{opacity:1}}

/* ── input bar ── */
.input-bar{padding:1rem 1.5rem 1.2rem;border-top:1px solid var(--border);flex-shrink:0}
.input-wrap{display:flex;gap:0.75rem;align-items:flex-end;background:var(--surface);
  border:1px solid var(--border);border-radius:12px;padding:0.6rem 0.6rem 0.6rem 1rem;
  transition:border-color .2s}
.input-wrap:focus-within{border-color:var(--accent)}
textarea#msg{flex:1;background:transparent;border:none;outline:none;resize:none;
  color:var(--text);font-family:var(--font-body);font-size:0.92rem;line-height:1.5;
  max-height:140px;min-height:24px;padding-top:2px}
textarea#msg::placeholder{color:var(--muted)}
.send-btn{width:36px;height:36px;border-radius:9px;border:none;cursor:pointer;
  background:var(--accent);color:white;display:flex;align-items:center;justify-content:center;
  flex-shrink:0;transition:opacity .2s;font-size:1rem}
.send-btn:hover{opacity:0.85}
.send-btn:disabled{opacity:0.3;cursor:not-allowed}
.input-hint{font-size:0.72rem;color:var(--muted);margin-top:0.5rem;text-align:center}

/* ── animations ── */
@keyframes fadeIn {from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes slideUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
</style>
</head>
<body>
<div class="shell">

  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="sidebar-logo">Study<span>Buddy</span> <span style="color:var(--muted);font-weight:400">AI</span></div>

    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);padding:0 0.5rem;margin-bottom:0.25rem">Topics</div>

    {% for key, t in topics.items() %}
    <button class="topic-btn {% if key == 'general' %}active{% endif %}"
            onclick="setTopic('{{ key }}')" id="btn-{{ key }}">
      <span class="topic-emoji">{{ t.emoji }}</span>
      <span>{{ t.name }}</span>
      <span class="dot" style="background:{{ t.color }};margin-left:auto"></span>
    </button>
    {% endfor %}

    <div class="sidebar-footer">
      <strong>How to use</strong><br>
      Pick a topic → ask anything.<br>
      The AI remembers your full<br>
      conversation until you clear it.
      <br><br>
      <strong>Model:</strong> Claude Sonnet<br>
      <strong>Project 5 of 5</strong> · Python ML Roadmap
    </div>
  </aside>

  <!-- MAIN -->
  <main class="main">
    <div class="topbar">
      <div class="topbar-title">
        <span id="topicEmoji">📚</span>
        <span id="topicName">General Study Buddy</span>
        <span class="topbar-pill" id="topicPill">general</span>
      </div>
      <button class="clear-btn" onclick="clearChat()">Clear chat</button>
    </div>

    <div class="messages" id="messages">
      <div class="welcome" id="welcome">
        <div class="welcome-emoji" id="welcomeEmoji">📚</div>
        <h2>What are we studying today?</h2>
        <p>Pick a topic from the sidebar, then ask me anything. I'll explain it clearly, step by step.</p>
        <div class="welcome-chips">
          <span class="chip" onclick="sendChip(this)">What is machine learning?</span>
          <span class="chip" onclick="sendChip(this)">Explain Python lists</span>
          <span class="chip" onclick="sendChip(this)">How does photosynthesis work?</span>
          <span class="chip" onclick="sendChip(this)">What caused World War 1?</span>
          <span class="chip" onclick="sendChip(this)">Solve x² + 5x + 6 = 0</span>
          <span class="chip" onclick="sendChip(this)">Explain recursion simply</span>
        </div>
      </div>
    </div>

    <div class="input-bar">
      <div class="input-wrap">
        <textarea id="msg" rows="1" placeholder="Ask anything..." onkeydown="handleKey(event)" oninput="autoResize(this)"></textarea>
        <button class="send-btn" id="sendBtn" onclick="sendMessage()">➤</button>
      </div>
      <div class="input-hint">Enter to send · Shift+Enter for new line</div>
    </div>
  </main>
</div>

<script>
// ── State ──────────────────────────────────────────────────
let history = [];   // full conversation history sent to Claude
let currentTopic = 'general';
const topics = {{ topics_json | safe }};

// ── Topic switching ────────────────────────────────────────
function setTopic(key) {
  currentTopic = key;
  const t = topics[key];
  document.querySelectorAll('.topic-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('btn-' + key).classList.add('active');
  document.getElementById('topicEmoji').textContent  = t.emoji;
  document.getElementById('topicName').textContent   = t.name;
  document.getElementById('topicPill').textContent   = key;
  document.getElementById('welcomeEmoji').textContent = t.emoji;
  document.documentElement.style.setProperty('--accent', t.color);
  clearChat(false);
}

// ── Clear chat ─────────────────────────────────────────────
function clearChat(showWelcome = true) {
  history = [];
  const el = document.getElementById('messages');
  el.innerHTML = showWelcome ? '' : '';
  if (showWelcome) {
    el.innerHTML = `<div class="welcome" id="welcome">
      <div class="welcome-emoji">${topics[currentTopic].emoji}</div>
      <h2>What are we studying today?</h2>
      <p>Ask me anything about <strong>${topics[currentTopic].name}</strong>. I'll explain clearly, step by step.</p>
      <div class="welcome-chips">
        <span class="chip" onclick="sendChip(this)">What is machine learning?</span>
        <span class="chip" onclick="sendChip(this)">Explain Python lists</span>
        <span class="chip" onclick="sendChip(this)">How does photosynthesis work?</span>
        <span class="chip" onclick="sendChip(this)">What caused World War 1?</span>
        <span class="chip" onclick="sendChip(this)">Solve x² + 5x + 6 = 0</span>
        <span class="chip" onclick="sendChip(this)">Explain recursion simply</span>
      </div>
    </div>`;
  }
}

// ── Send helpers ───────────────────────────────────────────
function sendChip(el) { sendMessage(el.textContent); }
function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
}
function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 140) + 'px';
}

// ── Render markdown-lite ───────────────────────────────────
function renderText(text) {
  // code blocks
  text = text.replace(/```([a-z]*)\n?([\s\S]*?)```/g, (_, lang, code) =>
    `<pre><code>${code.replace(/</g,'&lt;').replace(/>/g,'&gt;')}</code></pre>`);
  // inline code
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
  // bold
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  // newlines → paragraphs
  text = text.split('\n\n').map(p => p.trim() ? `<p>${p.replace(/\n/g,'<br>')}</p>` : '').join('');
  return text || text;
}

// ── Main send function ─────────────────────────────────────
async function sendMessage(text) {
  const input = document.getElementById('msg');
  const userText = text || input.value.trim();
  if (!userText) return;

  // Hide welcome
  const welcome = document.getElementById('welcome');
  if (welcome) welcome.remove();

  // Clear input
  input.value = '';
  input.style.height = 'auto';

  // Show user bubble
  appendMessage('user', userText);

  // Add to history
  history.push({ role: 'user', content: userText });

  // Disable send button + show typing
  const btn = document.getElementById('sendBtn');
  btn.disabled = true;
  const typingId = appendTyping();

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: history, topic: currentTopic })
    });
    const data = await res.json();

    removeTyping(typingId);

    if (data.error) {
      appendMessage('bot', '⚠️ ' + data.error);
    } else {
      appendMessage('bot', data.reply);
      history.push({ role: 'assistant', content: data.reply });
    }
  } catch (err) {
    removeTyping(typingId);
    appendMessage('bot', '⚠️ Could not reach the server. Make sure the app is running.');
  }

  btn.disabled = false;
  input.focus();
}

// ── DOM helpers ────────────────────────────────────────────
function appendMessage(role, text) {
  const el = document.getElementById('messages');
  const isUser = role === 'user';
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.innerHTML = `
    <div class="avatar ${isUser ? 'user-av' : 'bot-av'}">${isUser ? 'YOU' : topics[currentTopic].emoji}</div>
    <div class="bubble">${isUser ? escHtml(text) : renderText(text)}</div>`;
  el.appendChild(div);
  el.scrollTop = el.scrollHeight;
}

function appendTyping() {
  const el = document.getElementById('messages');
  const id = 'typing-' + Date.now();
  const div = document.createElement('div');
  div.className = 'msg bot'; div.id = id;
  div.innerHTML = `
    <div class="avatar bot-av">${topics[currentTopic].emoji}</div>
    <div class="bubble"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div>`;
  el.appendChild(div);
  el.scrollTop = el.scrollHeight;
  return id;
}

function removeTyping(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function escHtml(text) {
  return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
</script>
</body>
</html>"""

# ── 8. FLASK ROUTES ──────────────────────────────────────────
@app.route("/")
def index():
    import json
    # Pass topics data to template (without the system prompt — keep it server-side)
    topics_safe = {k: {"name": v["name"], "emoji": v["emoji"], "color": v["color"]}
                   for k, v in TOPICS.items()}
    return render_template_string(
        HTML,
        topics=TOPICS,
        topics_json=json.dumps(topics_safe)
    )

@app.route("/chat", methods=["POST"])
def api_chat():
    """
    REST API endpoint — receives conversation history + topic,
    calls Claude, returns the reply.
    """
    data     = request.get_json()
    messages = data.get("messages", [])
    topic    = data.get("topic", "general")

    # Guard: check API key is set
    if API_KEY == "YOUR_API_KEY_HERE":
        return jsonify({"error":
            "API key not set! Open study_buddy.py and replace YOUR_API_KEY_HERE "
            "with your key from https://console.anthropic.com"})

    try:
        reply = chat_with_claude(messages, topic)
        return jsonify({"reply": reply})
    except anthropic.AuthenticationError:
        return jsonify({"error": "Invalid API key. Check your key at https://console.anthropic.com"})
    except anthropic.RateLimitError:
        return jsonify({"error": "Rate limit hit. Wait a moment and try again."})
    except Exception as e:
        return jsonify({"error": f"API error: {str(e)}"})

# ── 9. RUN ────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  📚 Study Buddy AI — Starting up")
    print("=" * 55)
    if API_KEY == "YOUR_API_KEY_HERE":
        print("\n  ⚠️  API KEY NOT SET")
        print("  Get your free key at: https://console.anthropic.com")
        print("  Then open study_buddy.py and replace YOUR_API_KEY_HERE\n")
    else:
        print(f"\n  ✅ API key loaded")
    print(f"  📡 Model : {MODEL}")
    print(f"  🌐 Open  : http://127.0.0.1:5000\n")
    app.run(debug=True)
