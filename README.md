# 🧠 Deal Intelligence Agent

An AI sales assistant that **remembers every call** and briefs a rep before the next one, powered by [Hindsight](https://hindsight.vectorize.io/) memory.

## The problem

Sales reps waste time re-reading CRM notes before calls, and things slip through: a promised case study never gets sent, a pricing objection is forgotten, a competitor mention is lost. A generic AI cannot help, because it knows nothing about the deal.

## What it does

- **Pre-call briefing:** pick a prospect and get a briefing with where the deal stands, open objections, competitors, promises made (missed ones flagged), and suggested talking points.
- **Memory ON / OFF / Side by side:** the same request answered without memory (generic) and with Hindsight memory (specific, grounded in past calls).
- **Memories recalled panel:** shows the exact memories Hindsight retrieved, so the briefing is never a black box.
- **Log a call:** paste new call notes; they are saved to memory and appear in the next briefing.

## How Hindsight memory is used

1. **Retain:** each call note is saved with `client.retain()`, along with a context line (who and which company), the real call date as a timestamp, and a unique document ID. Hindsight automatically extracts individual facts from each note (12 call notes became 70+ memories).
2. **Recall:** before writing a briefing, the app calls `client.recall()` with a question about the prospect's objections, competitors, promises, stakeholders, and next steps. Hindsight returns the most relevant memories, with dates and people involved.
3. **Generate:** the recalled memories are given to an LLM (`openai/gpt-oss-120b` on Groq), which writes the briefing using only those facts.
4. **Learn over time:** when a new call is logged, it is retained and the next recall includes it, so the briefing changes with no code changes.

**Without memory** the briefing is generic and invents details. **With memory** it knows the $48,000 vs $35,000 budget gap, the competitor Zentro, the CFO's approval condition, and the case study that was promised but never sent.

## Demo data

The data in `data.json` is synthetic: 3 prospects with 4 calls each across August and September 2026.

## Tech stack

Python, Streamlit, Hindsight Cloud (`hindsight-client`), Groq.

## Run it yourself

```bash
git clone https://github.com/pranathikurmana-colab/deal-intelligence-agent.git
cd deal-intelligence-agent
pip install streamlit groq hindsight-client
```

1. Copy `config.example.py` to `config.py` and add your Hindsight and Groq API keys.
2. Load the sample data into memory (run once): `python load_data.py`
3. Start the app: `streamlit run app.py`

## Future work

- Won/lost outcome tracking, so the agent learns which tactics win deals
- Pattern insights across deals (for example, which objections respond to which proof)
- CRM integration and email drafting for follow-ups