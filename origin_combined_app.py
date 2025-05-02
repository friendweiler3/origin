
import streamlit as st
from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Origin System", layout="centered")

st.title("Origin: Create and Command Your AI Agents")
st.markdown("_Generate agents from myth, then assign them tasks — all in one interface._")

# --- PART 1: Generate Agents from a Myth ---
st.subheader("1. Upload Myth to Generate Agents")

story_input = st.text_area("Paste your myth or origin story here:", height=300)
agents = []

if st.button("Generate Agents") and story_input:
    with st.spinner("Invoking Origin..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Origin, an AI architect that reads creation myths and generates structured agent intelligence. "
                            "Each agent should have: name, role, tone, alignment, and tasks. All agents must be aligned to the Founder (Friend)."
                        )
                    },
                    {"role": "user", "content": story_input}
                ],
                temperature=0.6
            )
            output = response.choices[0].message.content
            agents = eval(output) if isinstance(output, str) else output

            # Save agents to file (optional)
            with open("origin_agents.json", "w") as f:
                json.dump({"output": output}, f)

            st.success("Agents generated from myth:")
            st.code(output, language="json")

        except Exception as e:
            st.error(f"Failed to generate agents: {e}")

# --- PART 2: Assign Tasks to Generated Agents ---
if agents:
    st.subheader("2. Assign a Task to Any Agent")

    agent_names = [agent["name"] for agent in agents if "name" in agent]
    selected_agent = st.selectbox("Choose an agent to activate:", agent_names)
    task_input = st.text_area("Describe the task for this agent:")

    if st.button("Send Task") and selected_agent and task_input:
        selected_profile = next(agent for agent in agents if agent["name"] == selected_agent)
        prompt = (
            f"You are {selected_agent}, an AI agent created by Origin. "
            f"Your role is: {selected_profile.get('role', '')}. "
            f"Your tone is: {selected_profile.get('tone', '')}. "
            f"You are aligned to the Founder, Friend. "
            f"Your current task is: {task_input}"
        )

        with st.spinner(f"{selected_agent} is working..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": task_input}
                    ],
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.success(f"{selected_agent}'s response:")
                st.write(reply)

            except Exception as e:
                st.error(f"Task failed: {e}")
else:
    st.info("Generate your agents above first.")
