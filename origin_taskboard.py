
import streamlit as st
from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Origin TaskBoard", layout="centered")

st.title("Origin: Activate Your AI Agents")
st.markdown("_Select an agent from your myth and give them a task to complete._")

# Upload the agents from previous generation
agent_file = st.file_uploader("Upload your origin_agents.json", type="json")

if agent_file:
    try:
        agents_data = json.load(agent_file)
        if isinstance(agents_data, dict) and "output" in agents_data:
            agent_output = agents_data["output"]
            agents = eval(agent_output) if isinstance(agent_output, str) else agent_output
        else:
            agents = agents_data

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

            with st.spinner(f"Task being processed by {selected_agent}..."):
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
        st.error(f"Error loading agents or processing task: {e}")
else:
    st.info("Please upload your generated agent file from Origin (origin_agents.json)")
