import requests
import json
import os
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY  = os.getenv("RAPIDAPI_KEY")
HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {
    "x-rapidapi-key" : API_KEY,
    "x-rapidapi-host": HOST
}

CACHE_FILE = "match_cache.json"

# Current playoff contenders only
PLAYOFF_TEAMS = [
    'Royal Challengers Bengaluru',
    'Gujarat Titans',
    'Sunrisers Hyderabad',
    'Rajasthan Royals',
    'Punjab Kings'
]

# All 10 IPL teams for manual prediction
IPL_TEAMS = [
    'Chennai Super Kings',
    'Delhi Capitals',
    'Gujarat Titans',
    'Kolkata Knight Riders',
    'Lucknow Super Giants',
    'Mumbai Indians',
    'Punjab Kings',
    'Rajasthan Royals',
    'Royal Challengers Bengaluru',
    'Sunrisers Hyderabad'
]

API_VENUE_MAP = {
    'M.Chinnaswamy Stadium'                                              : 'Chinnaswamy Stadium',
    'Wankhede Stadium'                                                   : 'Wankhede Stadium',
    'Barsapara Cricket Stadium'                                          : 'Barsapara Stadium Guwahati',
    'Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur' : 'Mullanpur Stadium',
    'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium'      : 'Ekana Stadium Lucknow',
    'Eden Gardens'                                                       : 'Eden Gardens',
    'MA Chidambaram Stadium'                                             : 'Chepauk Stadium',
    'Arun Jaitley Stadium'                                               : 'Arun Jaitley Stadium',
    'Narendra Modi Stadium'                                              : 'Narendra Modi Stadium',
    'Rajiv Gandhi International Stadium'                                 : 'Rajiv Gandhi Stadium',
    'Sawai Mansingh Stadium'                                             : 'Sawai Mansingh Stadium',
    'Shaheed Veer Narayan Singh International Stadium'                   : 'SVNS Stadium Raipur',
    'Himachal Pradesh Cricket Association Stadium'                       : 'HPCA Stadium Dharamsala',
}





# Helper Functions 

def extract_toss(toss_status):
    """Extract toss winner and decision from toss string"""
    if not toss_status:
        return None, None
    if 'opt to bat' in toss_status:
        return toss_status.replace(' opt to bat', '').strip(), 'bat'
    elif 'opt to bowl' in toss_status:
        return toss_status.replace(' opt to bowl', '').strip(), 'field'
    elif 'elected to bat' in toss_status:
        return toss_status.replace(' elected to bat', '').strip(), 'bat'
    elif 'elected to field' in toss_status:
        return toss_status.replace(' elected to field', '').strip(), 'field'
    return None, None


def get_toss_data(match_id):
    try:
        url      = f"https://{HOST}/mcenter/v1/{match_id}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        data     = response.json()
        toss_status           = data.get('tossstatus', '')
        toss_winner, decision = extract_toss(toss_status)
        return toss_winner, decision
    except:
        return None, None


def is_cache_fresh(max_age_hours=6):
    if not os.path.exists(CACHE_FILE):
        return False

    modified_time = datetime.fromtimestamp(
        os.path.getmtime(CACHE_FILE)
    )
    age = datetime.now() - modified_time

    return age < timedelta(hours=max_age_hours)


def save_cache(match_data):
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(match_data, f)
        print("Match data cached successfully!")
    except Exception as e:
        print(f"Cache save error: {e}")


def load_cache():
    #Load match data from cache file
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except:
        return None


# ── Main API Functions ────────────────────────────────

def get_all_ipl_matches():
    """
    Fetch all IPL 2026 matches from series endpoint
    Uses 1 API call only
    """
    try:
        url      = f"https://{HOST}/series/v1/9241"
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code == 429:
            print("API limit reached! Using cache...")
            return []

        data = response.json()

        matches = []
        for item in data.get('matchDetails', []):
            match_map = item.get('matchDetailsMap', {})
            for match in match_map.get('match', []):
                info  = match.get('matchInfo', {})
                state = info.get('state', '')

                team1 = info.get('team1', {}).get('teamName', '')
                team2 = info.get('team2', {}).get('teamName', '')

                # Skip TBC matches
                if team1 == 'TBC' or team2 == 'TBC':
                    continue

                venue_raw = info.get('venueInfo', {}).get('ground', '')
                venue     = API_VENUE_MAP.get(venue_raw, venue_raw)

                matches.append({
                    'match_id'  : info.get('matchId'),
                    'match_desc': info.get('matchDesc', ''),
                    'team1'     : team1,
                    'team2'     : team2,
                    'venue'     : venue,
                    'status'    : info.get('status', ''),
                    'state'     : state,
                })
        return matches

    except Exception as e:
        print(f"API Error: {e}")
        return []


def get_todays_match_from_api():
    matches = get_all_ipl_matches()

    if not matches:
        return None

    # Priority 1 — Live match
    for m in matches:
        if m['state'] == 'In Progress':
            tw, td = get_toss_data(m['match_id'])
            m['toss_winner']   = tw
            m['toss_decision'] = td
            m['match_type']    = 'LIVE'
            return m

    # Priority 2 — Preview (toss done)
    for m in matches:
        if m['state'] == 'Preview':
            tw, td = get_toss_data(m['match_id'])
            m['toss_winner']   = tw
            m['toss_decision'] = td
            m['match_type']    = 'PREVIEW'
            return m

    # Priority 3 — Upcoming
    for m in matches:
        if m['state'] == 'Upcoming':
            m['toss_winner']   = None
            m['toss_decision'] = None
            m['match_type']    = 'UPCOMING'
            return m

    # Priority 4 — Latest completed
    completed = [m for m in matches if m['state'] == 'Complete']
    if completed:
        m      = completed[-1]
        tw, td = get_toss_data(m['match_id'])
        m['toss_winner']   = tw
        m['toss_decision'] = td
        m['match_type']    = 'RECENT'
        return m

    return None




def get_todays_match():
    
    # Smart caching based on match situation:
    # Live match   → refresh every 30 minutes
    # Match day    → refresh every 1 hour  
    # No match day → refresh every 12 hours
    
    old_cache = load_cache()

    if old_cache:
        state = old_cache.get('state', '')
        match_type = old_cache.get('match_type', '')

        if state == 'In Progress':
            # live match refresh every 30 min
            max_age = 0.5
        elif match_type in ['PREVIEW', 'UPCOMING']:
            # match today ->refresh every 1 hour
            max_age = 1
        else:
            # No match refresh every 12 hour
            max_age = 12
    else:
        # no cache at all fetch immediately
        max_age = 0

    #check if cache is still fresh
    if is_cache_fresh(max_age_hours=max_age):
        print(f"Using cache (max age: {max_age}h)")
        return old_cache

    print("fetching fresh data from API")
    match = get_todays_match_from_api()

    if match:
        save_cache(match)
        return match

    # API failed → use old cache
    if old_cache:
        print("API failed — using old cache")
        old_cache['match_type'] = 'CACHED'
        return old_cache

    return None

