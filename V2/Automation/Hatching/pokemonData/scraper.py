import urllib.request
import json
from alive_progress import alive_bar


def get_mon_list():
    # Get a list of all pokemon from swsh
    dexlist_url = "https://www.serebii.net/pokedex-swsh/"
    dex_names = set()

    for line in urllib.request.urlopen(dexlist_url):
        decoded = line.decode('latin-1')
        # Get pokemon from dropdown
        # Checks the line is an option with the right url and a dex number 
        if all([mon_text in decoded for mon_text in ["<option", "/pokedex-swsh/"]]) and decoded.split(' ')[1][-1].isnumeric():
            mon_name = decoded.split(' ', 2)[2].split('<')[0]
            # Lowercase and spaces
            mon_name = mon_name.lower().replace(' ', '')
            # Fix gender symbols
            mon_name = mon_name.replace('&#9792;', 'm').replace('&#9794;', 'f')
            # Save
            dex_names.add(mon_name)
    dex_names = sorted(dex_names)
    return dex_names

def get_steps(name):
    # Get step counts
    mon_url = f"https://www.serebii.net/pokedex-swsh/{name}/"

    # Get line
    for line in urllib.request.urlopen(mon_url):
        decoded = line.decode('latin-1')
        if "(SWSH)" in decoded:
            steps = decoded
            break
    # Get steps
    steps = int(steps.split('(SWSH)')[0].split('>')[-1].strip().replace(',',''))
    return steps

def get_step_counts():
    # Get names
    names = get_mon_list()
    step_counts = {}

    # Get steps
    with alive_bar(len(names)) as bar:
        for mon in names:
            step_counts[mon] = get_steps(mon)
            bar()
    
    # Save
    with open(f"step_counts.py", 'w+', encoding="utf-8") as file:
        file.write("pokedex="+json.dumps(step_counts, indent=4))    
    return


if __name__ == "__main__":
    get_step_counts()