
import streamlit as st
import openai
import os
import json

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY") or "your-openai-api-key"

st.set_page_config(page_title="Origin", layout="centered")

st.title("Origin: Create Your AI Team from a Myth")
st.markdown("_Upload a story. Birth an intelligent system._")

story_input = st.text_area("Paste your myth or origin story here:", height=300)

if st.button("Generate Agents") and story_input:
    with st.spinner("Invoking Origin..."):
        response = openai.ChatCompletion.create(
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
        st.subheader("Generated Agents:")
        st.code(output, language="json")

        # Optional: save output
        with open("origin_agents.json", "w") as f:
            json.dump(output, f)
