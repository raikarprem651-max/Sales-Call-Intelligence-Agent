import json
from datetime import datetime
import streamlit as st
from briefing import get_briefing, memory_client
from config import BANK

st.set_page_config(page_title="Deal Intelligence Agent", page_icon="🧠", layout="wide")

st.title("🧠 Deal Intelligence Agent")
st.caption("A sales assistant that remembers every call, powered by Hindsight memory")

# Build the prospect list from data.json
with open("data.json") as f:
    calls = json.load(f)
prospects = sorted({c["prospect"] for c in calls})

# ---------- Sidebar ----------
st.sidebar.header("Choose a prospect")
prospect = st.sidebar.selectbox("Prospect", prospects)
company = next(c["company"] for c in calls if c["prospect"] == prospect)
st.sidebar.write(f"**Company:** {company}")

mode = st.sidebar.radio(
    "Briefing mode",
    ["Memory ON", "Memory OFF", "Side by side"],
)

tab1, tab2 = st.tabs(["📋 Pre-call briefing", "📞 Log a call"])

# ---------- Tab 1: Briefing ----------
with tab1:
    if st.button("Generate pre-call briefing", type="primary"):
        if mode == "Side by side":
            left, right = st.columns(2)
            with left:
                st.subheader("❌ Without memory")
                with st.spinner("Thinking..."):
                    text, _ = get_briefing(prospect, use_memory=False)
                st.write(text)
            with right:
                st.subheader("✅ With Hindsight memory")
                with st.spinner("Recalling and thinking..."):
                    text, memories = get_briefing(prospect, use_memory=True)
                st.write(text)
                with st.expander(f"🧠 Memories recalled ({len(memories)})"):
                    for m in memories:
                        st.markdown(f"- {m}")
        else:
            use_memory = mode == "Memory ON"
            with st.spinner("Working..."):
                text, memories = get_briefing(prospect, use_memory=use_memory)
            st.subheader("✅ With Hindsight memory" if use_memory else "❌ Without memory")
            st.write(text)
            if use_memory:
                with st.expander(f"🧠 Memories recalled ({len(memories)})"):
                    for m in memories:
                        st.markdown(f"- {m}")

# ---------- Tab 2: Log a call ----------
with tab2:
    st.write(f"Log a new call with **{prospect}**. Hindsight will remember it.")
    call_date = st.date_input("Call date", datetime.today())
    notes = st.text_area(
        "Call notes",
        height=150,
        placeholder="e.g. Priya said her CFO approved the pilot. She wants the security review finished by Friday.",
    )
    if st.button("Save call to memory"):
        if notes.strip():
            with st.spinner("Saving to Hindsight..."):
                memory_client.retain(
                    bank_id=BANK,
                    content=notes,
                    context=f"Sales call with {prospect} of {company}",
                    timestamp=datetime.combine(call_date, datetime.min.time()),
                    document_id=f"{prospect}-{datetime.now().isoformat()}",
                )
            st.success("Saved! Wait about 20 seconds, then generate a new briefing to see it included.")
        else:
            st.warning("Please type some call notes first.")