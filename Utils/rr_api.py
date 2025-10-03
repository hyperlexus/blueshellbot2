import json
import requests

def fetch_api_data():
    url = "https://status.rwfc.net/groups"
    # need to do ts because api checks for bots
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)

        response.raise_for_status()
        api_data = response.json()
        return api_data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching API data: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from response. The server might be down or returning HTML.")

def calculate_average_vr():
    api_data = fetch_api_data()
    rooms = api_data.get('rooms', [])
    final_vr_averages = {}

    for room in rooms:
        room_id = room.get('id')
        players = room.get('players', {})

        sum_vr = 0
        players_with_vr = 0
        for player_data in players.values():
            if 'ev' in player_data:
                try:
                    if player_data['ev'] == "-1":
                        continue
                    sum_vr += int(player_data['ev'])
                    players_with_vr += 1
                except (ValueError, TypeError):
                    continue

        if players_with_vr > 0:
            average_vr = sum_vr / players_with_vr
            final_vr_averages[room_id] = (round(average_vr), players_with_vr)

    return final_vr_averages

def readable_average_vr(vr_data):
    sorted_vr_data = sorted(vr_data.items(), key=lambda item: item[1][1], reverse=True)
    formatted_vr_data = [
        f"Room {room_id} - {player_count} players, {avg_vr} Avg VR"
        for room_id, (avg_vr, player_count) in sorted_vr_data
    ]

    return "\n".join(formatted_vr_data)

print(readable_average_vr(calculate_average_vr()))
