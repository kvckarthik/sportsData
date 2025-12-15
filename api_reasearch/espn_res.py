"""
ESPN API Exploration Script
Day 1: Fetch and inspect NFL weekly games

Purpose:
- Prove ESPN API works
- Get game IDs, teams, dates
- Save raw JSON for inspection
- No database, no parsing complexity
"""

import requests
import json
from datetime import datetime
from pathlib import Path


def fetch_nfl_scoreboard(year=2024, week=None):
    """
    Fetch NFL scoreboard from ESPN API
    
    Args:
        year: NFL season year (default: 2024)
        week: Week number (1-18 for regular season, None for current week)
    
    Returns:
        dict: Raw JSON response from ESPN
    """
    base_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    
    params = {
        "limit": 100  # Get all games for the week
    }
    
    # If week is specified, add it to params
    if week:
        params["week"] = week
        params["seasontype"] = 2  # 2 = regular season, 3 = playoffs
    
    print(f"🏈 Fetching NFL games...")
    print(f"   URL: {base_url}")
    print(f"   Params: {params}")
    print()
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes
        
        data = response.json()
        print("✅ Successfully fetched data from ESPN API")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None


def save_raw_response(data, filename):
    """
    Save raw JSON response to file
    
    Args:
        data: JSON data to save
        filename: Name of file to save to
    """
    # Create sample_responses directory only (assuming api_research already exists)
    output_dir = Path("sample_responses")
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved raw response to: {filepath}")
    print()


def print_game_summary(data):
    """
    Print a clean, readable summary of games
    
    Args:
        data: ESPN API response data
    """
    if not data or 'events' not in data:
        print("⚠️  No games found in response")
        return
    
    events = data.get('events', [])
    season = data.get('season', {})
    week = data.get('week', {})
    
    print("=" * 80)
    print(f"📅 NFL SCHEDULE")
    print(f"   Season: {season.get('year', 'Unknown')}")
    print(f"   Week: {week.get('number', 'Unknown')}")
    print("=" * 80)
    print()
    
    if not events:
        print("No games found for this week.")
        return
    
    for idx, event in enumerate(events, 1):
        game_id = event.get('id', 'Unknown')
        name = event.get('name', 'Unknown matchup')
        date = event.get('date', 'Unknown date')
        status = event.get('status', {}).get('type', {}).get('description', 'Unknown')
        
        # Parse date to more readable format
        try:
            dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
            formatted_date = dt.strftime('%Y-%m-%d %I:%M %p')
        except:
            formatted_date = date
        
        # Get team info
        competitions = event.get('competitions', [])
        if competitions:
            competitors = competitions[0].get('competitors', [])
            if len(competitors) >= 2:
                home_team = next((c for c in competitors if c.get('homeAway') == 'home'), {})
                away_team = next((c for c in competitors if c.get('homeAway') == 'away'), {})
                
                home_name = home_team.get('team', {}).get('displayName', 'Unknown')
                away_name = away_team.get('team', {}).get('displayName', 'Unknown')
                
                print(f"Game {idx}:")
                print(f"  ID: {game_id}")
                print(f"  Matchup: {away_name} @ {home_name}")
                print(f"  Date: {formatted_date}")
                print(f"  Status: {status}")
                print()


def inspect_data_structure(data):
    """
    Print key fields available in the response
    This helps us understand what data we can use
    
    Args:
        data: ESPN API response data
    """
    print("=" * 80)
    print("🔍 DATA STRUCTURE INSPECTION")
    print("=" * 80)
    print()
    
    print("Top-level keys available:")
    for key in data.keys():
        print(f"  - {key}")
    print()
    
    if 'events' in data and data['events']:
        print("Sample event structure (first game):")
        event = data['events'][0]
        print(f"  Event keys: {list(event.keys())}")
        print()
        
        if 'competitions' in event and event['competitions']:
            comp = event['competitions'][0]
            print(f"  Competition keys: {list(comp.keys())}")
            print()
            
            if 'competitors' in comp and comp['competitors']:
                competitor = comp['competitors'][0]
                print(f"  Competitor keys: {list(competitor.keys())}")
                print()
                
                if 'team' in competitor:
                    team = competitor['team']
                    print(f"  Team keys: {list(team.keys())}")
                    print()


def main():
    """
    Main execution function
    """
    print("=" * 80)
    print("ESPN NFL API EXPLORATION - DAY 1")
    print("=" * 80)
    print()
    
    # Fetch current week's games (ESPN will return current week by default)
    data = fetch_nfl_scoreboard()
    
    if not data:
        print("Failed to fetch data. Exiting.")
        return
    
    # Save raw response
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nfl_scoreboard_{timestamp}.json"
    save_raw_response(data, filename)
    
    # Print readable summary
    print_game_summary(data)
    
    # Inspect available fields
    inspect_data_structure(data)
    
    print("=" * 80)
    print("✅ EXPLORATION COMPLETE")
    print("=" * 80)
    print()
    print("📋 NEXT STEPS:")
    print("  1. Check api_research/sample_responses/ for the full JSON")
    print("  2. Manually inspect the JSON to see all available fields")
    print("  3. Note any interesting fields for later use")
    print()


if __name__ == "__main__":
    main()