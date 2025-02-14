import requests
import time
from valclient.client import Client
from valclient.exceptions import HandshakeError

# Function to fetch all available agents from the Valorant API
def get_all_agents():
    response = requests.get("https://valorant-api.com/v1/agents")
    agents_info = response.json()

    agents = []
    for agent in agents_info['data']:
        if agent['isPlayableCharacter']:
            agents.append((agent['uuid'], agent['displayName']))
    return agents

# Function to check if the game is in pregame
def is_in_pregame(client):
    try:
        match_info = client.pregame_fetch_match()
        return match_info and match_info.get('PregameState') == 'character_select_active'
    except Exception as e:
        print(f"Error fetching match info: {e}")
        return False

# Function to lock an agent
def lock_agent(agent_id, agent_name):
    client = Client(region="eu")

    # Attempt to activate the client
    try:
        client.activate()  # Activate the client
    except HandshakeError:
        print("Unable to activate; is VALORANT running? Exiting...")
        return

    print("Waiting for pregame...")

    while True:
        if is_in_pregame(client):
            print("In pregame phase!")
                # Attempt to lock the agent
            client.pregame_lock_character(agent_id)
            print(f"Successfully locked agent: {agent_name}")  # Print the agent's name
            break  # Exit after locking the agent
        else:
            pass
        
        time.sleep(3)  # Wait for 3 seconds before checking again

# Main execution
if __name__ == "__main__":
    agents = get_all_agents()

    print("Available Agents:")
    for _, agent_name in agents:
        print(agent_name)  # Display agent names only

    agent_name_input = input("Enter the name of the agent you want to lock: ").strip()  # Get user input

    # Find the selected agent by name
    selected_agent = next((agent for agent in agents if agent[1].lower() == agent_name_input.lower()), None)

    if selected_agent:
        selected_agent_id = selected_agent[0]  # Get the selected agent ID
        selected_agent_name = selected_agent[1]  # Get the selected agent name
        lock_agent(selected_agent_id, selected_agent_name)  # Lock the selected agent
    else:
        print("Invalid agent name. Exiting...")
