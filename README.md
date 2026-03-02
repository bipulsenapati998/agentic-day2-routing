# agentic-day2-routing
Design a **minimal but production-minded LangGraph workflow** that:  
- Tracks conversation state in a typed `SupportState` 
- Routes users to different paths based on **user tier** (`vip` vs `standard`) 
- Makes the routing logic **explicit, testable, and auditable**

# How to run the App 
1. Clone the Repository:
```
    git clone https://github.com/bipulsenapati998/agentic-day2-routing.git
```
2. Create & Activate the virtual environment:
```
    Use conda	
    conda create -n llms python=3.11 && conda activate llms  
```
3. Update the .env file with your OpenAI API key:
```
    OPENAI_API_KEY=<your_actual_api_key_here>
```
4. Install Dependencies:
```
    pip install -r requirement.txt
```
5. Run the Application:
```
   python app.py 
```
