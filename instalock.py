import requests
import time
from valclient.client import Client
from valclient.exceptions import HandshakeError

def get_all_agents():
    response = requests.get("https://valorant-api.com/v1/agents")
    agents_info = response.json()

    agents = []
    for agent in agents_info['data']:
        if agent['isPlayableCharacter']:
            agents.append((agent['uuid'], agent['displayName']))
    return {k: v for v, k in agents}

def is_in_pregame(client):
    try:
        match_info = client.pregame_fetch_match()
        return match_info and match_info.get('PregameState') == 'character_select_active'
    except Exception as e:
        print(f"Error fetching match info: {e}")
        return False

def lock_agent(agent_id, agent_name):
    client = Client(region="eu")

    try:
        client.activate()
    except HandshakeError:
        print("Unable to activate; is VALORANT running? Exiting...")
        return

    print("Waiting for pregame...")

    while True:
        if is_in_pregame(client):
            print("In pregame phase!")
            client.pregame_lock_character(agent_id)
            print(f"Successfully locked agent: {agent_name}")
            break
        else:
            pass
        
        time.sleep(3)

if __name__ == "__main__":
    agents_dict = get_all_agents()

    print("Available Agents:")
    for agent in agents_dict.keys():
        print(agent)


    selected_agent = input("Enter the name of the agent you want to lock: ").strip().capitalize()

    if selected_agent in agents_dict.keys():
        agent_id = agents_dict[selected_agent]
        lock_agent(agent_id, selected_agent)
    else:
        print("Invalid agent name. Exiting...")
