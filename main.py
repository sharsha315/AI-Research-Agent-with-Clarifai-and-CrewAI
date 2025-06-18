import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
import streamlit as st

# Load environment variables from .env file
load_dotenv()

CLARIFAI_PAT = os.getenv("CLARIFAI_PAT")

# Configure Clarifai LLM
clarifai_llm = LLM(
    model="openai/deepseek-ai/deepseek-chat/models/DeepSeek-R1-Distill-Qwen-7B",   
    base_url="https://api.clarifai.com/v2/ext/openai/v1",
    api_key=CLARIFAI_PAT 
)

# Define the Researcher Agent
researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments and facts on a given topic",
    backstory="""You are a meticulous and insightful research analyst at a tech think tank.
    You specialize in identifying trends, gathering verified information,
    and presenting concise insights.""",    
    verbose=True, # Set to False to disable verbose output 
    allow_delegation=False,
    llm=clarifai_llm
)

def create_research_task(topic):
    return Task(
        description=f"""Conduct a comprehensive analysis of '{topic}'.
        Identify key trends, breakthrough technologies, important figures, and potential industry impacts.
        Focus on factual and verifiable information.""",
        expected_output="A detailed analysis report in bullet points, including sources if possible.",
        agent=researcher
    )

def run_research(topic):
    task = create_research_task(topic)

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    return crew.kickoff() # Starts the execution of the crew

st.set_page_config(page_title="AI Research Chatbot", page_icon=":robot_face:")

st.title("AI Research Chatbot")
st.write("Ask for a research report on any topic!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Enter the topic to research:", key="input")

if st.button("Research") and user_input:
    with st.spinner(f"Researching '{user_input}'..."):
        result = run_research(user_input)
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", result))

for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**AI Researcher:**\n{message}")
