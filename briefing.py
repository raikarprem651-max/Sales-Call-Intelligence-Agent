import time
from groq import Groq
from hindsight_client import Hindsight
from config import HINDSIGHT_KEY, GROQ_KEY, HINDSIGHT_URL, BANK

memory_client = Hindsight(base_url=HINDSIGHT_URL, api_key=HINDSIGHT_KEY)
llm = Groq(api_key=GROQ_KEY)
MODEL = "openai/gpt-oss-120b"


def ask_llm(prompt):
    """Ask Groq, and retry once if it fails."""
    for attempt in range(2):
        try:
            response = llm.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print("LLM error, retrying:", e)
            time.sleep(2)
    return "Sorry, the AI could not respond. Please try again."


def recall_memories(prospect):
    """Get the memories Hindsight has about this prospect."""
    query = f"Everything about {prospect}: objections, competitors, promises made, stakeholders, and next steps"
    results = memory_client.recall(bank_id=BANK, query=query)
    seen = []
    for r in results.results:
        if r.text not in seen:
            seen.append(r.text)
    return seen[:20]


def get_briefing(prospect, use_memory):
    """Returns (briefing_text, list_of_recalled_memories)."""
    if use_memory:
        memories = recall_memories(prospect)
        memory_text = "\n".join(f"- {m}" for m in memories)
        prompt = f"""You are a sales assistant. I have a call with {prospect} soon.
Here is everything my memory system remembers about them:

{memory_text}

Write a short pre-call briefing with these sections:
1. Where the deal stands
2. Open objections and concerns
3. Competitors mentioned
4. Promises I made (flag any that were missed)
5. Suggested talking points for this call
Use only facts from the memories above. Mention the date of the call each point came from when known."""
        return ask_llm(prompt), memories

    prompt = f"""You are a sales assistant. I have a call with {prospect} soon.
Write a short pre-call briefing with these sections:
1. Where the deal stands
2. Open objections and concerns
3. Competitors mentioned
4. Promises I made
5. Suggested talking points for this call"""
    return ask_llm(prompt), []


if __name__ == "__main__":
    name = "Priya Nair"

    print("=" * 60)
    print("MEMORY OFF")
    print("=" * 60)
    text, _ = get_briefing(name, use_memory=False)
    print(text)

    print()
    print("=" * 60)
    print("MEMORY ON")
    print("=" * 60)
    text, memories = get_briefing(name, use_memory=True)
    print(text)
    print(f"\n(Used {len(memories)} memories)")