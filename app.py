import datetime
import hashlib
import math
import random
import pandas as pd
import streamlit as st

# ==========================================
# PAGE CONFIGURATION & CUSTOM STYLING
# ==========================================
st.set_page_config(
    page_title="Player Forge | Ultimate GOAT Builder",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #090d16;
        color: #f8fafc;
    }
    .spin-banner {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 2px solid #6366f1;
        padding: 22px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.25);
    }
    .slot-card {
        background-color: #131c2e;
        border: 2px dashed #334155;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        min-height: 155px;
        margin-bottom: 10px;
        transition: all 0.2s ease-in-out;
    }
    .slot-card.filled-elite {
        border: 2px solid #eab308;
        background: linear-gradient(135deg, #422006 0%, #131c2e 100%);
    }
    .slot-card.filled-good {
        border: 2px solid #3b82f6;
        background: linear-gradient(135deg, #172554 0%, #131c2e 100%);
    }
    .slot-card.filled-trap {
        border: 2px solid #ef4444;
        background: linear-gradient(135deg, #450a0a 0%, #131c2e 100%);
    }
    .tier-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .pill-goat { background-color: #fef08a; color: #713f12; }
    .pill-star { background-color: #bfdbfe; color: #1e3a8a; }
    .pill-spec { background-color: #bbf7d0; color: #14532d; }
    .pill-trap { background-color: #fecaca; color: #7f1d1d; }
    .synergy-chip {
        display: inline-block;
        background-color: #064e3b;
        border: 1px solid #10b981;
        color: #ecfdf5;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# ==========================================
# EXPANDED 100+ ATHLETE DATABASE (4 LEAGUES)
# ==========================================
LEAGUES_DATA = {
    "🏀 Pro Basketball": {
        "icon": "🏀",
        "attributes": [
            "Inside Scoring",
            "3PT & Shooting",
            "Playmaking & IQ",
            "Perimeter Defense",
            "Rebounding & Size",
            "Clutch Gene",
        ],
        "stat_labels": ["PPG", "RPG", "APG"],
        "athletes": [
            # GOATs & Superstars
            {
                "name": "Michael Jordan",
                "safe": "His Airness #23",
                "team": "CHI",
                "tier": "GOAT",
                "hint": "6x Finals MVP, Scoring & Lockdown God",
                "vals": [99, 88, 91, 99, 84, 99],
            },
            {
                "name": "LeBron James",
                "safe": "The Akron King #23",
                "team": "LAL",
                "tier": "GOAT",
                "hint": "All-Time Scoring Leader & Complete Freight Train",
                "vals": [99, 88, 99, 93, 92, 97],
            },
            {
                "name": "Stephen Curry",
                "safe": "The Golden Chef #30",
                "team": "GSW",
                "tier": "GOAT",
                "hint": "Greatest Shooter Ever, Smaller Frame Inside",
                "vals": [91, 99, 94, 82, 72, 98],
            },
            {
                "name": "Nikola Jokić",
                "safe": "The Sombor Joker #15",
                "team": "DEN",
                "tier": "GOAT",
                "hint": "Point-Center Triple-Double Machine",
                "vals": [97, 92, 99, 80, 97, 96],
            },
            {
                "name": "Kobe Bryant",
                "safe": "Black Mamba #24",
                "team": "LAL",
                "tier": "GOAT",
                "hint": "81-Point Assassin & Relentless Closer",
                "vals": [98, 91, 89, 96, 80, 99],
            },
            {
                "name": "Kevin Durant",
                "safe": "Slim Reaper #35",
                "team": "PHX",
                "tier": "GOAT",
                "hint": "7-Foot 50/40/90 Walking Bucket",
                "vals": [97, 98, 88, 89, 86, 97],
            },
            {
                "name": "Larry Bird",
                "safe": "The Hick from French Lick #33",
                "team": "BOS",
                "tier": "GOAT",
                "hint": "Trash-Talking Shooting & Passing Legend",
                "vals": [94, 98, 97, 88, 92, 99],
            },
            {
                "name": "Magic Johnson",
                "safe": "Showtime General #32",
                "team": "LAL",
                "tier": "GOAT",
                "hint": "6'9\" Point Guard Maestro",
                "vals": [92, 84, 99, 85, 90, 96],
            },
            {
                "name": "Tim Duncan",
                "safe": "Big Fundamental #21",
                "team": "SAS",
                "tier": "GOAT",
                "hint": "5-Ring Bank-Shot & Defensive Anchor",
                "vals": [96, 76, 88, 94, 98, 96],
            },
            {
                "name": "Luka Dončić",
                "safe": "Luka Magic #77",
                "team": "DAL",
                "tier": "STAR",
                "hint": "Offensive Heliocentric Genius, Slow Footwork on D",
                "vals": [96, 94, 99, 74, 90, 97],
            },
            {
                "name": "Shai Gilgeous-Alexander",
                "safe": "Mid-Range Maestro #2",
                "team": "OKC",
                "tier": "STAR",
                "hint": "Slithery Two-Way Scoring Guard",
                "vals": [97, 89, 91, 93, 78, 95],
            },
            {
                "name": "Anthony Edwards",
                "safe": "Ant-Man Posterizer #5",
                "team": "MIN",
                "tier": "STAR",
                "hint": "Explosive Rim Attacker & Two-Way Wing",
                "vals": [96, 90, 86, 93, 82, 94],
            },
            {
                "name": "Jayson Tatum",
                "safe": "Boston Franchise Wing #0",
                "team": "BOS",
                "tier": "STAR",
                "hint": "Well-Rounded Championship Two-Way Forward",
                "vals": [93, 91, 89, 92, 89, 91],
            },
            {
                "name": "Damian Lillard",
                "safe": "Logo Dame Time #0",
                "team": "MIL",
                "tier": "STAR",
                "hint": "40-Foot Buzzer-Beater Specialist, Weak Defense",
                "vals": [91, 98, 92, 72, 70, 99],
            },
            {
                "name": "Kyrie Irving",
                "safe": "Uncle Drew Handles #11",
                "team": "DAL",
                "tier": "STAR",
                "hint": "Unmatched Finishing & Game 7 Dagger",
                "vals": [97, 95, 92, 78, 72, 98],
            },
            {
                "name": "Kawhi Leonard",
                "safe": "The Klaw #2",
                "team": "LAC",
                "tier": "STAR",
                "hint": "Robotic Mid-Range & Lockdown Perimeter Thief",
                "vals": [95, 92, 85, 99, 88, 96],
            },
            # High-Variance Specialists (Dangerous Traps in wrong slot!)
            {
                "name": "Shaquille O'Neal",
                "safe": "The Big Diesel #34",
                "team": "LAL",
                "tier": "SPEC",
                "hint": "99 Paint Dominance & Rebounding, 45 Shooting!",
                "vals": [99, 45, 76, 80, 99, 90],
            },
            {
                "name": "Giannis Antetokounmpo",
                "safe": "The Greek Freak #34",
                "team": "MIL",
                "tier": "SPEC",
                "hint": "Unstoppable Paint & Defense, Shaky Jumper",
                "vals": [99, 68, 89, 96, 98, 93],
            },
            {
                "name": "Victor Wembanyama",
                "safe": "The 7-4 Alien #1",
                "team": "SAS",
                "tier": "SPEC",
                "hint": "8-Foot Wingspan Defensive & Rebounding Phenom",
                "vals": [92, 86, 84, 99, 98, 89],
            },
            {
                "name": "Dennis Rodman",
                "safe": "The Worm #91",
                "team": "CHI",
                "tier": "SPEC",
                "hint": "99 Rebounding & Defense, Refuses to Shoot!",
                "vals": [58, 42, 68, 99, 99, 82],
            },
            {
                "name": "Rudy Gobert",
                "safe": "The Stifle Tower #27",
                "team": "MIN",
                "tier": "SPEC",
                "hint": "4x DPOY Rebounder, Zero Jumper",
                "vals": [84, 35, 62, 88, 98, 65],
            },
            {
                "name": "Kyle Korver",
                "safe": "Catch & Shoot Sniper #26",
                "team": "ATL",
                "tier": "SPEC",
                "hint": "98 Three-Point Laser, Limited Everywhere Else",
                "vals": [72, 98, 74, 70, 65, 82],
            },
            {
                "name": "Ben Simmons",
                "safe": "Pass-First Point Forward #10",
                "team": "PHI",
                "tier": "SPEC",
                "hint": "Elite Playmaking & Perimeter D, Allergic to Shooting!",
                "vals": [80, 32, 92, 95, 88, 42],
            },
            # Full Bust Traps
            {
                "name": "Kwame Brown",
                "safe": "Draft Bust #1",
                "team": "WAS",
                "tier": "TRAP",
                "hint": "Small Hands & Butterfingers Under Pressure",
                "vals": [62, 40, 50, 68, 72, 45],
            },
            {
                "name": "Brian Scalabrine",
                "safe": "The White Mamba #44",
                "team": "BOS",
                "tier": "TRAP",
                "hint": "Human Victory Cigar & Bench Meme Legend",
                "vals": [66, 78, 68, 62, 64, 75],
            },
            {
                "name": "Smush Parker",
                "safe": "Backcourt Bystander #1",
                "team": "LAL",
                "tier": "TRAP",
                "hint": "Famous for Combining with Kobe for 94 Points",
                "vals": [68, 70, 69, 60, 55, 52],
            },
        ],
    },
    "🏈 Pro Football": {
        "icon": "🏈",
        "attributes": [
            "Passing Accuracy",
            "Arm Strength & Deep Ball",
            "Rushing & Elusiveness",
            "Receiving & Hands",
            "Football IQ & Defense",
            "2-Minute Clutch Drive",
        ],
        "stat_labels": ["Total Yds/Yr", "Total TDs/Yr", "All-Pro Honors"],
        "athletes": [
            # GOATs & Superstars
            {
                "name": "Tom Brady",
                "safe": "The 7-Ring GOAT #12",
                "team": "NE",
                "tier": "GOAT",
                "hint": "99 IQ, Accuracy & Clutch, Statue in the Pocket",
                "vals": [99, 92, 54, 65, 99, 99],
            },
            {
                "name": "Patrick Mahomes",
                "safe": "Showtime Grim Reaper #15",
                "team": "KC",
                "tier": "GOAT",
                "hint": "No-Look Rocket Arm, Scrambling & OT Magic",
                "vals": [97, 99, 91, 78, 96, 99],
            },
            {
                "name": "Jerry Rice",
                "safe": "The 80 Route God",
                "team": "SF",
                "tier": "GOAT",
                "hint": "Untouchable Receiving Records & Stamina",
                "vals": [75, 72, 92, 99, 98, 99],
            },
            {
                "name": "Peyton Manning",
                "safe": "The Omaha Sheriff #18",
                "team": "IND",
                "tier": "GOAT",
                "hint": "5x MVP Field General, Zero Mobility",
                "vals": [99, 93, 52, 60, 99, 95],
            },
            {
                "name": "Lamar Jackson",
                "safe": "Action Jackson #8",
                "team": "BAL",
                "tier": "STAR",
                "hint": "99 Human Joystick Rushing & Deep Flick",
                "vals": [91, 94, 99, 82, 91, 92],
            },
            {
                "name": "Josh Allen",
                "safe": "Buffalo Hurdle Tank #17",
                "team": "BUF",
                "tier": "STAR",
                "hint": "99 Howitzer Arm & Bulldozer Dual-Threat",
                "vals": [91, 99, 95, 78, 89, 95],
            },
            {
                "name": "Joe Burrow",
                "safe": "Joe Shiesty #9",
                "team": "CIN",
                "tier": "STAR",
                "hint": "Ice-Vein Pocket Surgeon & 4th Down Closer",
                "vals": [97, 90, 82, 74, 96, 98],
            },
            {
                "name": "Randy Moss",
                "safe": "The Freak #84",
                "team": "MIN",
                "tier": "GOAT",
                "hint": "'You Got Mossed!' 99 Deep Ball Hands & Speed",
                "vals": [70, 82, 95, 99, 88, 94],
            },
            {
                "name": "Calvin Johnson",
                "safe": "Megatron #81",
                "team": "DET",
                "tier": "GOAT",
                "hint": "Triple-Covered Jump Ball Monster",
                "vals": [70, 78, 92, 99, 90, 95],
            },
            {
                "name": "Justin Jefferson",
                "safe": "Jettas Griddy King #18",
                "team": "MIN",
                "tier": "STAR",
                "hint": "Acrobatic Route Technician & Elite Hands",
                "vals": [75, 74, 93, 99, 92, 95],
            },
            {
                "name": "Ja'Marr Chase",
                "safe": "Always Open #1",
                "team": "CIN",
                "tier": "STAR",
                "hint": "Explosive YAC & Deep Threat Receiver",
                "vals": [72, 74, 95, 98, 90, 95],
            },
            {
                "name": "Tyreek Hill",
                "safe": "The Cheetah #10",
                "team": "MIA",
                "tier": "STAR",
                "hint": "99 Track Speed & Deep Separation",
                "vals": [70, 72, 99, 96, 86, 92],
            },
            {
                "name": "Christian McCaffrey",
                "safe": "Run CMC #23",
                "team": "SF",
                "tier": "STAR",
                "hint": "1,000/1,000 Rushing & Receiving Swiss Army Knife",
                "vals": [80, 76, 98, 96, 94, 94],
            },
            {
                "name": "Barry Sanders",
                "safe": "The Lion Ankle-Breaker #20",
                "team": "DET",
                "tier": "GOAT",
                "hint": "Greatest Elusive Runner in Gridiron History",
                "vals": [68, 65, 99, 88, 92, 93],
            },
            {
                "name": "Derrick Henry",
                "safe": "King Henry Tractorcito #22",
                "team": "BAL",
                "tier": "SPEC",
                "hint": "98 Stiff-Arm Freight Train & Jump-Pass Threat",
                "vals": [74, 76, 98, 78, 88, 92],
            },
            {
                "name": "Saquon Barkley",
                "safe": "Reverse Hurdle Phenom #26",
                "team": "PHI",
                "tier": "STAR",
                "hint": "Home-Run Hitter with Elite Lower-Body Power",
                "vals": [72, 72, 98, 90, 89, 93],
            },
            {
                "name": "Travis Kelce",
                "safe": "Big Yeti Tight End #87",
                "team": "KC",
                "tier": "STAR",
                "hint": "Playoff Zone-Finder & Unstoppable Improviser",
                "vals": [78, 76, 86, 98, 96, 98],
            },
            {
                "name": "Rob Gronkowski",
                "safe": "Gronk Spike #87",
                "team": "NE",
                "tier": "GOAT",
                "hint": "Dominant Red-Zone & Blocking Tight End",
                "vals": [70, 78, 89, 98, 94, 97],
            },
            {
                "name": "Lawrence Taylor",
                "safe": "L.T. #56",
                "team": "NYG",
                "tier": "GOAT",
                "hint": "99 Defensive Terror Who Changed Pass Protection",
                "vals": [55, 65, 90, 75, 99, 97],
            },
            {
                "name": "Ed Reed",
                "safe": "Ballhawk Safety #20",
                "team": "BAL",
                "tier": "GOAT",
                "hint": "99 Defensive IQ, Interceptions & Return Threat",
                "vals": [68, 72, 93, 94, 99, 96],
            },
            {
                "name": "Deion Sanders",
                "safe": "Prime Time #21",
                "team": "DAL",
                "tier": "GOAT",
                "hint": "99 Lockdown Island, Speed & Two-Way Hands",
                "vals": [70, 70, 99, 95, 99, 96],
            },
            {
                "name": "Aaron Donald",
                "safe": "Interior Wrecking Ball #99",
                "team": "LAR",
                "tier": "GOAT",
                "hint": "3x DPOY Who Closes Super Bowls on 4th Down",
                "vals": [55, 65, 86, 70, 99, 98],
            },
            # Traps & Oddballs
            {
                "name": "JaMarcus Russell",
                "safe": "70-Yard Kneeling Cannon #2",
                "team": "OAK",
                "tier": "SPEC",
                "hint": "99 Arm Strength, 45 Everything Else!",
                "vals": [52, 99, 50, 50, 42, 45],
            },
            {
                "name": "Tim Tebow",
                "safe": "Mile High Miracle #15",
                "team": "DEN",
                "tier": "SPEC",
                "hint": "96 4th-Quarter Magic & Power Run, 55 Passing Accuracy!",
                "vals": [55, 78, 91, 70, 82, 96],
            },
            {
                "name": "Nathan Peterman",
                "safe": "5-Interception Half #2",
                "team": "BUF",
                "tier": "TRAP",
                "hint": "Preseason Hall of Famer, Regular Season Pick-Six Machine",
                "vals": [54, 62, 60, 55, 48, 40],
            },
        ],
    },
    "⚽ World Soccer": {
        "icon": "⚽",
        "attributes": [
            "Clinical Finishing",
            "Dribbling & Flair",
            "Vision & Passing",
            "Defensive Workrate",
            "Pace & Stamina",
            "Big Match Clutch",
        ],
        "stat_labels": ["Goals/Yr", "Assists/Yr", "Major Trophies"],
        "athletes": [
            # GOATs & Superstars
            {
                "name": "Lionel Messi",
                "safe": "La Pulga #10",
                "team": "ARG",
                "tier": "GOAT",
                "hint": "8x Ballon d'Or Alien Playmaker & Finisher",
                "vals": [99, 99, 99, 62, 89, 99],
            },
            {
                "name": "Cristiano Ronaldo",
                "safe": "CR7 Apex Predator #7",
                "team": "POR",
                "tier": "GOAT",
                "hint": "900+ Goals, Champions League Clutch God",
                "vals": [99, 94, 87, 72, 97, 99],
            },
            {
                "name": "Pelé",
                "safe": "O Rei #10",
                "team": "BRA",
                "tier": "GOAT",
                "hint": "3x World Cup Winner & Complete Attacker",
                "vals": [99, 97, 95, 78, 95, 99],
            },
            {
                "name": "Diego Maradona",
                "safe": "El Pibe de Oro #10",
                "team": "ARG",
                "tier": "GOAT",
                "hint": "1986 World Cup Solo-Goal Magician",
                "vals": [95, 99, 98, 68, 91, 99],
            },
            {
                "name": "Zinedine Zidane",
                "safe": "Zizou Maestro #5",
                "team": "FRA",
                "tier": "GOAT",
                "hint": "Velvet First Touch, Vision & Final Volleys",
                "vals": [91, 97, 99, 82, 85, 98],
            },
            {
                "name": "Ronaldo Nazário",
                "safe": "O Fenômeno R9",
                "team": "BRA",
                "tier": "GOAT",
                "hint": "Unstoppable Explosive Dribbling & Rounding Keepers",
                "vals": [99, 99, 86, 55, 97, 97],
            },
            {
                "name": "Ronaldinho",
                "safe": "Joga Bonito Magician #10",
                "team": "BRA",
                "tier": "GOAT",
                "hint": "99 Elastico Flair & Bernabéu Standing Ovation",
                "vals": [92, 99, 96, 58, 91, 95],
            },
            {
                "name": "Johan Cruyff",
                "safe": "Total Football Prophet #14",
                "team": "NED",
                "tier": "GOAT",
                "hint": "The Cruyff Turn & Tactical Mastermind",
                "vals": [94, 98, 99, 78, 93, 96],
            },
            {
                "name": "Kylian Mbappé",
                "safe": "Bondy Rocket #7",
                "team": "FRA",
                "tier": "STAR",
                "hint": "World Cup Final Hat-Trick & 99 Blistering Pace",
                "vals": [97, 96, 86, 60, 99, 98],
            },
            {
                "name": "Erling Haaland",
                "safe": "The Nordic Cyborg #9",
                "team": "NOR",
                "tier": "SPEC",
                "hint": "99 Goal Poacher & Sprint Power, Low Link-Up Play",
                "vals": [99, 78, 74, 68, 96, 94],
            },
            {
                "name": "Jude Bellingham",
                "safe": "Hey Jude #5",
                "team": "ENG",
                "tier": "STAR",
                "hint": "95th-Minute Box-to-Box Clutch Midfielder",
                "vals": [91, 91, 92, 90, 93, 97],
            },
            {
                "name": "Vinícius Júnior",
                "safe": "Baila Vini #7",
                "team": "BRA",
                "tier": "STAR",
                "hint": "UCL Knockout Dribbler, Pace & Big-Game Closer",
                "vals": [92, 98, 89, 68, 98, 97],
            },
            {
                "name": "Lamine Yamal",
                "safe": "La Masia Wonderkid #19",
                "team": "ESP",
                "tier": "STAR",
                "hint": "Teenage Euro Champion Wing Wizard",
                "vals": [89, 97, 95, 72, 94, 94],
            },
            {
                "name": "Kevin De Bruyne",
                "safe": "King Kev Assist Machine #17",
                "team": "BEL",
                "tier": "STAR",
                "hint": "99 Laser Through-Balls & Crossing",
                "vals": [90, 89, 99, 78, 85, 94],
            },
            {
                "name": "Luka Modrić",
                "safe": "Trivela Maestro #10",
                "team": "CRO",
                "tier": "GOAT",
                "hint": "6x UCL Midfield Engine & Endless Stamina",
                "vals": [84, 94, 99, 91, 93, 97],
            },
            {
                "name": "Andrés Iniesta",
                "safe": "El Ilusionista #8",
                "team": "ESP",
                "tier": "GOAT",
                "hint": "World Cup Final Winner & Tight-Space Genius",
                "vals": [85, 98, 99, 82, 88, 98],
            },
            {
                "name": "Rodri",
                "safe": "Untucked Shirt Anchor #16",
                "team": "ESP",
                "tier": "STAR",
                "hint": "Ballon d'Or Defensive Midfielder & Late Bangers",
                "vals": [86, 88, 95, 98, 90, 97],
            },
            {
                "name": "N'Golo Kanté",
                "safe": "Covers 30% of Earth #7",
                "team": "FRA",
                "tier": "SPEC",
                "hint": "99 Defensive Workrate & Endless Lungs",
                "vals": [72, 84, 85, 99, 99, 93],
            },
            {
                "name": "Paolo Maldini",
                "safe": "Il Capitano #3",
                "team": "ITA",
                "tier": "GOAT",
                "hint": "Greatest Defender of All Time",
                "vals": [70, 82, 88, 99, 93, 97],
            },
            {
                "name": "Virgil van Dijk",
                "safe": "The Anfield Colossus #4",
                "team": "NED",
                "tier": "STAR",
                "hint": "99 Defensive Aura & Long Diagonal Passing",
                "vals": [76, 78, 88, 99, 91, 94],
            },
            {
                "name": "Sergio Ramos",
                "safe": "92:48 Header King #4",
                "team": "ESP",
                "tier": "STAR",
                "hint": "Elite Defender with 99 Clutch Final Headers",
                "vals": [86, 78, 84, 96, 90, 99],
            },
            {
                "name": "Gareth Bale",
                "safe": "Wales. Golf. Bicycle Kick #11",
                "team": "WAL",
                "tier": "STAR",
                "hint": "99 Sprint Speed & Champions League Final Bangers",
                "vals": [94, 92, 86, 76, 99, 98],
            },
            # Specialists & Traps
            {
                "name": "Adama Traoré",
                "safe": "Baby-Oil Speed Demon #11",
                "team": "ESP",
                "tier": "SPEC",
                "hint": "99 Pace & 94 Dribbling, 58 Finishing into Row Z!",
                "vals": [58, 94, 65, 72, 99, 62],
            },
            {
                "name": "Nicklas Bendtner",
                "safe": "Lord Bendtner #52",
                "team": "DEN",
                "tier": "TRAP",
                "hint": "100 Confidence in Interviews, 70 on the Pitch",
                "vals": [72, 64, 62, 52, 68, 75],
            },
            {
                "name": "Antony",
                "safe": "360 Fidget Spinner #21",
                "team": "BRA",
                "tier": "TRAP",
                "hint": "88 Flashy Spins, Low End Product",
                "vals": [68, 88, 70, 68, 84, 62],
            },
        ],
    },
    "🎾 Pro Tennis": {
        "icon": "🎾",
        "attributes": [
            "Forehand Power",
            "Backhand Precision",
            "Serve & Aces",
            "Net Volley & Touch",
            "Court Speed & Stamina",
            "Tiebreak Mental Clutch",
        ],
        "stat_labels": [
            "Grand Slams",
            "Career Win %",
            "Weeks at World #1",
        ],
        "athletes": [
            # GOATs & Legends
            {
                "name": "Novak Djokovic",
                "safe": "The Belgrade Elastic Wall",
                "team": "SRB",
                "tier": "GOAT",
                "hint": "24 Slams, 99 Backhand, Speed & Tiebreak God",
                "vals": [96, 99, 94, 90, 99, 99],
            },
            {
                "name": "Roger Federer",
                "safe": "The Swiss Maestro",
                "team": "SUI",
                "tier": "GOAT",
                "hint": "Liquid Forehand, Precision Serve & 99 Net Grace",
                "vals": [99, 92, 97, 99, 94, 95],
            },
            {
                "name": "Rafael Nadal",
                "safe": "The King of Clay",
                "team": "ESP",
                "tier": "GOAT",
                "hint": "14 Roland Garros Titles, Heavy Topspin & 99 Fight",
                "vals": [99, 95, 89, 92, 99, 99],
            },
            {
                "name": "Serena Williams",
                "safe": "The 23-Slam Queen",
                "team": "USA",
                "tier": "GOAT",
                "hint": "Greatest Serve & Power Baseline Game Ever",
                "vals": [99, 96, 99, 90, 93, 99],
            },
            {
                "name": "Carlos Alcaraz",
                "safe": "Carlitos Drop-Shot Phenom",
                "team": "ESP",
                "tier": "STAR",
                "hint": "100mph Forehand, Feather Touch & 5-Set Stamina",
                "vals": [98, 93, 91, 97, 99, 97],
            },
            {
                "name": "Jannik Sinner",
                "safe": "The San Candido Laser",
                "team": "ITA",
                "tier": "STAR",
                "hint": "Cleanest Ball-Striker on Both Wings Under Pressure",
                "vals": [97, 98, 94, 88, 95, 96],
            },
            {
                "name": "Pete Sampras",
                "safe": "Pistol Pete",
                "team": "USA",
                "tier": "GOAT",
                "hint": "99 Clutch Second Serve & Slam Dunk Smash",
                "vals": [95, 84, 99, 98, 91, 98],
            },
            {
                "name": "Andre Agassi",
                "safe": "The Vegas Punisher",
                "team": "USA",
                "tier": "GOAT",
                "hint": "Career Golden Slam & Pure Baseline Ball-Striking",
                "vals": [96, 98, 86, 84, 90, 95],
            },
            {
                "name": "Steffi Graf",
                "safe": "Fräulein Forehand (Golden Slam)",
                "team": "GER",
                "tier": "GOAT",
                "hint": "99 Inside-Out Forehand, Footwork & Slice",
                "vals": [99, 93, 91, 92, 99, 98],
            },
            {
                "name": "Iga Świątek",
                "safe": "The Warsaw Bakery (6-0)",
                "team": "POL",
                "tier": "STAR",
                "hint": "Heavy Topspin, Sliding Movement & Clay Mastery",
                "vals": [96, 95, 86, 86, 98, 94],
            },
            {
                "name": "Aryna Sabalenka",
                "safe": "The Tiger Baseline Crusher",
                "team": "BLR",
                "tier": "STAR",
                "hint": "Raw Groundstroke Power & Hardcourt Dominance",
                "vals": [98, 94, 93, 84, 90, 93],
            },
            {
                "name": "Andy Murray",
                "safe": "Sir Andy Lob Master",
                "team": "GBR",
                "tier": "STAR",
                "hint": "Elite Two-Handed Backhand, Defense & Grit",
                "vals": [89, 97, 86, 92, 97, 95],
            },
            {
                "name": "Stan Wawrinka",
                "safe": "Stan The Man (1HBH Rocket)",
                "team": "SUI",
                "tier": "SPEC",
                "hint": "99 One-Handed Backhand Howitzer in Grand Slam Finals",
                "vals": [94, 99, 92, 85, 88, 96],
            },
            {
                "name": "Björn Borg",
                "safe": "The Ice Borg",
                "team": "SWE",
                "tier": "GOAT",
                "hint": "11 Slams, Ice-Cold Pulse & Endless Stamina",
                "vals": [94, 95, 88, 86, 99, 99],
            },
            {
                "name": "John McEnroe",
                "safe": "'You Cannot Be Serious!'",
                "team": "USA",
                "tier": "GOAT",
                "hint": "99 Serve-and-Volley Touch & Left-Handed Angles",
                "vals": [88, 89, 94, 99, 92, 92],
            },
            {
                "name": "Martina Navratilova",
                "safe": "167-Title Serve & Volley GOAT",
                "team": "USA",
                "tier": "GOAT",
                "hint": "Unmatched Net Coverage & 99 Volley Mastery",
                "vals": [93, 94, 95, 99, 97, 97],
            },
            {
                "name": "Venus Williams",
                "safe": "Wimbledon Grass Thunderbolt",
                "team": "USA",
                "tier": "STAR",
                "hint": "129mph Serve, Wingspan & Flat Groundstrokes",
                "vals": [95, 92, 97, 94, 94, 93],
            },
            {
                "name": "Daniil Medvedev",
                "safe": "The Hardcourt Octopus",
                "team": "RUS",
                "tier": "STAR",
                "hint": "Stands 15 Feet Behind Baseline & Returns Everything",
                "vals": [88, 96, 93, 80, 97, 93],
            },
            {
                "name": "Alexander Zverev",
                "safe": "135mph Serve & Backhand Beam",
                "team": "GER",
                "tier": "STAR",
                "hint": "World-Class Backhand & First Serve, Tight in 5th Sets",
                "vals": [90, 97, 96, 82, 92, 78],
            },
            # High-Variance Specialists & Traps
            {
                "name": "John Isner",
                "safe": "70-68 Marathon Servebot",
                "team": "USA",
                "tier": "SPEC",
                "hint": "All-Time Aces Leader (99 Serve), 68 Movement!",
                "vals": [91, 74, 99, 84, 68, 92],
            },
            {
                "name": "Ivo Karlović",
                "safe": "6'11\" Ace Doctor",
                "team": "CRO",
                "tier": "SPEC",
                "hint": "99 Unreturnable Serve, 62 Baseline Rallies!",
                "vals": [82, 62, 99, 88, 64, 88],
            },
            {
                "name": "Juan Martín del Potro",
                "safe": "The Tower of Tandil (Thor's Hammer)",
                "team": "ARG",
                "tier": "SPEC",
                "hint": "99 Fearhand Nuclear Missile, Wrist-Limited Backhand",
                "vals": [99, 78, 93, 85, 84, 94],
            },
            {
                "name": "Gaël Monfils",
                "safe": "La Monf 360 Showman",
                "team": "FRA",
                "tier": "SPEC",
                "hint": "99 Diving Speed & Trick Shots, Plays for the Crowd",
                "vals": [92, 89, 91, 88, 99, 78],
            },
            {
                "name": "Nick Kyrgios",
                "safe": "Underarm Serve Maverick",
                "team": "AUS",
                "tier": "SPEC",
                "hint": "98 Serve & Touch Talent, Volatile Meltdown Risk",
                "vals": [93, 91, 98, 95, 82, 62],
            },
            {
                "name": "Bernard Tomic",
                "safe": "8-Second Match Point Tank",
                "team": "AUS",
                "tier": "TRAP",
                "hint": "Returned Serve with the Handle of His Racket",
                "vals": [72, 70, 78, 74, 52, 38],
            },
        ],
    },
}


# ==========================================
# HELPER FUNCTIONS (RADAR SVG, SYNERGY, SIM)
# ==========================================
def generate_radar_svg(labels: list[str], values: list[int]) -> str:
    """Renders a sleek, zero-dependency SVG hexagonal radar chart."""
    size = 320
    cx, cy = size / 2, size / 2
    max_r = 105

    grid_polygons = ""
    for level in [25, 50, 75, 100]:
        pts = []
        r = max_r * (level / 100.0)
        for i in range(6):
            angle = math.radians(i * 60 - 90)
            pts.append(f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}")
        grid_polygons += (
            f'<polygon points="{" ".join(pts)}" fill="none" '
            f'stroke="#334155" stroke-width="1" stroke-dasharray="3,3" />'
        )

    axis_lines = ""
    label_nodes = ""
    for i in range(6):
        angle = math.radians(i * 60 - 90)
        x_end = cx + max_r * math.cos(angle)
        y_end = cy + max_r * math.sin(angle)
        axis_lines += (
            f'<line x1="{cx}" y1="{cy}" x2="{x_end:.1f}" y2="{y_end:.1f}" '
            f'stroke="#475569" stroke-width="1" />'
        )
        lx = cx + (max_r + 28) * math.cos(angle)
        ly = cy + (max_r + 22) * math.sin(angle)
        short_lbl = labels[i].split(" ")[0].upper()
        val_str = str(values[i]) if values[i] > 0 else "--"
        label_nodes += (
            f'<text x="{lx:.1f}" y="{ly:.1f}" fill="#cbd5e1" font-size="11" '
            f'font-weight="bold" text-anchor="middle" dominant-baseline="middle">'
            f"{short_lbl} ({val_str})</text>"
        )

    data_pts = []
    dots = ""
    for i in range(6):
        v = max(15, values[i]) if values[i] > 0 else 10
        r = max_r * (v / 100.0)
        angle = math.radians(i * 60 - 90)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        data_pts.append(f"{px:.1f},{py:.1f}")
        if values[i] > 0:
            dots += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="#38bdf8" stroke="#0f172a" stroke-width="1.5" />'

    poly = (
        f'<polygon points="{" ".join(data_pts)}" '
        f'fill="rgba(56, 189, 248, 0.28)" stroke="#38bdf8" stroke-width="2.5" />'
    )

    return (
        f'<div style="display:flex;justify-content:center;align-items:center;">'
        f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        f"{grid_polygons}{axis_lines}{poly}{dots}{label_nodes}</svg></div>"
    )


def evaluate_synergies(assigned_slots: dict) -> tuple[int, list[str]]:
    """Calculates bonus OVR points and unlocked badge descriptions."""
    bonus = 0
    badges = []
    filled = [v for v in assigned_slots.values() if v is not None]
    if len(filled) < 6:
        return 0, []

    teams = [a["team"] for a in filled]
    unique_teams = set(teams)
    if len(unique_teams) == 6:
        bonus += 2
        badges.append("🌈 Rainbow Draft (+2 OVR: 6 Different Teams)")
    elif any(teams.count(t) >= 3 for t in unique_teams):
        bonus += 2
        badges.append("🤝 Franchise Dynasty (+2 OVR: 3+ Same Team/Nation)")

    raw_vals = [assigned_slots[i]["vals"][i] for i in range(6)]
    if min(raw_vals) >= 88:
        bonus += 1
        badges.append("💎 Flawless Blueprint (+1 OVR: All Skills 88+)")

    if sum(1 for v in raw_vals if v >= 98) >= 3:
        bonus += 1
        badges.append("⚡ Apex Triple-Crown (+1 OVR: 3+ 98/99 Attributes)")

    return bonus, badges


def get_deterministic_athlete(
    pool: list[dict], mode: str, custom_code: str, step_idx: int, league_name: str
) -> dict:
    """Returns a deterministic athlete for Daily/Seeded modes or random for Free Play."""
    if mode == "🔥 Daily Challenge (Global Seed)":
        today_str = datetime.date.today().isoformat()
        seed_str = f"DAILY_{today_str}_{league_name}_{step_idx}"
        seed_int = int(hashlib.sha256(seed_str.encode()).hexdigest()[:12], 16)
        rng = random.Random(seed_int)
        return rng.choice(pool)
    elif mode == "⚔️ Friend Room Code":
        clean_code = (custom_code or "FORGE1").strip().upper()
        seed_str = f"ROOM_{clean_code}_{league_name}_{step_idx}"
        seed_int = int(hashlib.sha256(seed_str.encode()).hexdigest()[:12], 16)
        rng = random.Random(seed_int)
        return rng.choice(pool)
    else:
        return random.choice(pool)


def simulate_career(league: str, assigned_slots: dict, final_ovr: int) -> dict:
    """Deterministically simulates career rings, MVPs, prime stats & storyline log."""
    raw_vals = [assigned_slots[i]["vals"][i] for i in range(6)]
    sig = sum(v * (i + 17) for i, v in enumerate(raw_vals)) + final_ovr * 31
    rng = random.Random(sig)

    clutch = raw_vals[5]
    if final_ovr >= 96:
        tier = "👑 IMMORTAL GOAT"
        hof = "100% (First-Ballot Unanimous)"
        titles = rng.randint(4, 7) + (1 if clutch >= 97 else 0)
        mvps = rng.randint(3, 6)
    elif final_ovr >= 92:
        tier = "🏆 FIRST-BALLOT LEGEND"
        hof = f"{min(99.8, 88.0 + (final_ovr - 90) * 2.2):.1f}%"
        titles = rng.randint(2, 4)
        mvps = rng.randint(1, 3)
    elif final_ovr >= 87:
        tier = "🌟 PERENNIAL ALL-STAR"
        hof = f"{min(84.0, 48.0 + (final_ovr - 85) * 7.5):.1f}%"
        titles = rng.randint(0, 2)
        mvps = rng.randint(0, 1)
    elif final_ovr >= 80:
        tier = "🛡️ SOLID STARTER / CULT HERO"
        hof = "14.5%"
        titles = rng.randint(0, 1)
        mvps = 0
    else:
        tier = "🧢 ROTATION / MEME LEGEND"
        hof = "1.2%"
        titles = 0
        mvps = 0

    # Sport-specific Prime Stats
    if "Basketball" in league:
        ppg = round(11.0 + ((raw_vals[0] * 0.55 + raw_vals[1] * 0.45) - 60) * 0.58, 1)
        rpg = round(3.2 + (raw_vals[4] - 55) * 0.24, 1)
        apg = round(2.0 + (raw_vals[2] - 55) * 0.23, 1)
        stats = [f"{max(6.5, ppg)} PPG", f"{max(2.5, rpg)} RPG", f"{max(1.5, apg)} APG"]
    elif "Football" in league:
        yds = int(1800 + ((raw_vals[0] + raw_vals[1] + raw_vals[2] + raw_vals[3]) / 4 - 55) * 90)
        tds = int(12 + ((raw_vals[0] + raw_vals[3] + raw_vals[5]) / 3 - 55) * 0.95)
        all_pros = max(0, int((final_ovr - 82) * 0.65))
        stats = [f"{max(950, yds):,} Yds/Yr", f"{max(6, tds)} TDs/Yr", f"{all_pros}x All-Pro"]
    elif "Soccer" in league:
        goals = int(5 + ((raw_vals[0] * 0.7 + raw_vals[1] * 0.3) - 55) * 1.05)
        assists = int(4 + (raw_vals[2] - 55) * 0.58)
        trophies = titles * 3 + rng.randint(1, 4)
        stats = [f"{max(2, goals)} Goals/Yr", f"{max(2, assists)} Assists/Yr", f"{trophies} Trophies"]
    else:
        # Tennis
        slams = max(0, int((final_ovr - 85) * 1.55) + (2 if clutch >= 96 else 0))
        win_pct = round(min(91.5, max(51.0, 50.0 + (final_ovr - 70) * 1.45)), 1)
        weeks = max(0, int((final_ovr - 87) * 28))
        titles = slams
        stats = [f"{slams} Grand Slams", f"{win_pct}% Win Rate", f"{weeks} Wks at #1"]

    # Storyline Log
    best_idx = raw_vals.index(max(raw_vals))
    worst_idx = raw_vals.index(min(raw_vals))
    attrs = LEAGUES_DATA[league]["attributes"]
    timeline = [
        f"**Year 1 (Rookie Phenom):** Entered the league with an immediate {raw_vals[best_idx]}-rated **{attrs[best_idx]}** weapon, stunning scouts on opening night.",
        f"**Year 4 (Breakout Prime):** Peaked at **{final_ovr} OVR**, posting prime numbers of **{stats[0]}** and **{stats[1]}**.",
        (
            f"**Year 8 (Championship Legacy):** Delivered a legendary {clutch}-Clutch postseason run to cement **{titles} Major Titles/Rings**."
            if titles > 0
            else f"**Year 8 (Playoff Heartbreak):** Despite elite numbers, opponents ruthlessly targeted their {raw_vals[worst_idx]}-rated **{attrs[worst_idx]}** in tight playoff series."
        ),
        f"**Year 15 (Retirement & Hall of Fame Verdict):** Hung up the jersey with a **{hof}** Hall of Fame probability as a **{tier}**.",
    ]

    return {
        "tier": tier,
        "hof": hof,
        "titles": titles,
        "mvps": mvps,
        "stats": stats,
        "timeline": timeline,
    }


# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
def reset_forge_state():
    st.session_state.assigned_slots = {i: None for i in range(6)}
    st.session_state.current_spun_athlete = None
    st.session_state.spin_step = 0
    st.session_state.skip_tokens = 1
    st.session_state.swap_tokens = 1
    st.session_state.auto_tokens = 1
    st.session_state.drawn_names = set()


if "league" not in st.session_state:
    st.session_state.league = "🏀 Pro Basketball"
if "game_mode" not in st.session_state:
    st.session_state.game_mode = "🎲 Free Play (Random)"
if "room_code" not in st.session_state:
    st.session_state.room_code = "GOAT2026"
if "blind_mode" not in st.session_state:
    st.session_state.blind_mode = True
if "safe_mode" not in st.session_state:
    st.session_state.safe_mode = False
if "player_name" not in st.session_state:
    st.session_state.player_name = "Apex Prospect"
if "hall_of_fame_log" not in st.session_state:
    st.session_state.hall_of_fame_log = []
if "assigned_slots" not in st.session_state:
    reset_forge_state()


# ==========================================
# SIDEBAR CONTROLS
# ==========================================
st.sidebar.title("⚡ Forge Control Room")

selected_league = st.sidebar.selectbox(
    "1. Select Sport League", list(LEAGUES_DATA.keys())
)
if selected_league != st.session_state.league:
    st.session_state.league = selected_league
    reset_forge_state()
    st.rerun()

selected_mode = st.sidebar.radio(
    "2. Challenge Mode",
    [
        "🎲 Free Play (Random)",
        "🔥 Daily Challenge (Global Seed)",
        "⚔️ Friend Room Code",
    ],
)
if selected_mode != st.session_state.game_mode:
    st.session_state.game_mode = selected_mode
    reset_forge_state()
    st.rerun()

if st.session_state.game_mode == "⚔️ Friend Room Code":
    new_code = st.sidebar.text_input(
        "Enter Shared Room Code", value=st.session_state.room_code
    )
    if new_code != st.session_state.room_code:
        st.session_state.room_code = new_code
        reset_forge_state()
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🕵️ Scouting & Legal Settings")
st.session_state.blind_mode = st.sidebar.toggle(
    "🕶️ Authentic Blind Mode (Hide Ratings Until Picked)",
    value=st.session_state.blind_mode,
)
st.session_state.safe_mode = st.sidebar.toggle(
    "🛡️ Legal-Safe Parody Names",
    value=st.session_state.safe_mode,
)
st.session_state.player_name = st.sidebar.text_input(
    "Custom Prospect Name", value=st.session_state.player_name
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Current Build", use_container_width=True):
    reset_forge_state()
    st.rerun()


# ==========================================
# MAIN HEADER & LIVE TELEMETRY
# ==========================================
league_cfg = LEAGUES_DATA[st.session_state.league]
attributes = league_cfg["attributes"]
pool = league_cfg["athletes"]

filled_slots_count = sum(
    1 for v in st.session_state.assigned_slots.values() if v is not None
)

col_hdr1, col_hdr2 = st.columns([3, 2])
with col_hdr1:
    st.title(f"{league_cfg['icon']} PLAYER FORGE")
    st.caption(
        f"**Mode:** {st.session_state.game_mode} | "
        f"**Scouting:** {'🕶️ Blind Mode (True Knowledge Test)' if st.session_state.blind_mode else '👁️ Scouted Mode (Ratings Visible)'} | "
        f"**Pool Size:** {len(pool)} Athletes"
    )
with col_hdr2:
    current_vals = [
        st.session_state.assigned_slots[i]["vals"][i]
        for i in range(6)
        if st.session_state.assigned_slots[i] is not None
    ]
    running_avg = int(sum(current_vals) / len(current_vals)) if current_vals else 0
    m1, m2, m3 = st.columns(3)
    m1.metric("Slots Forged", f"{filled_slots_count} / 6")
    m2.metric("Running OVR", f"{running_avg}" if filled_slots_count > 0 else "--")
    m3.metric("Skips Left", f"{st.session_state.skip_tokens}")


# ==========================================
# TABS: FORGE ARENA | ROSTER DEX | HOF LEADERBOARD
# ==========================================
tab_arena, tab_dex, tab_hof = st.tabs(
    [
        "🏟️ Forge Arena",
        f"📖 League Scouting Dex ({len(pool)} Players)",
        f"🏛️ Session Leaderboard ({len(st.session_state.hall_of_fame_log)})",
    ]
)

with tab_arena:
    # ------------------------------------------
    # CENTRAL SPIN STAGE
    # ------------------------------------------
    if filled_slots_count < 6:
        btn_c1, btn_c2, btn_c3 = st.columns([2, 1.5, 1.5])

        with btn_c1:
            spin_disabled = st.session_state.current_spun_athlete is not None
            if st.button(
                f"🎰 SPIN ATHLETE #{filled_slots_count + 1}",
                type="primary",
                disabled=spin_disabled,
                use_container_width=True,
            ):
                # Draw avoiding duplicates when possible
                available = [
                    a
                    for a in pool
                    if a["name"] not in st.session_state.drawn_names
                ] or pool
                drawn = get_deterministic_athlete(
                    available,
                    st.session_state.game_mode,
                    st.session_state.room_code,
                    st.session_state.spin_step,
                    st.session_state.league,
                )
                st.session_state.current_spun_athlete = drawn
                st.session_state.drawn_names.add(drawn["name"])
                st.session_state.spin_step += 1
                st.rerun()

        with btn_c2:
            can_skip = (
                st.session_state.current_spun_athlete is not None
                and st.session_state.skip_tokens > 0
            )
            if st.button(
                f"⏭️ Burn Skip Token ({st.session_state.skip_tokens})",
                disabled=not can_skip,
                use_container_width=True,
            ):
                available = [
                    a
                    for a in pool
                    if a["name"] not in st.session_state.drawn_names
                ] or pool
                drawn = get_deterministic_athlete(
                    available,
                    st.session_state.game_mode,
                    st.session_state.room_code,
                    st.session_state.spin_step,
                    st.session_state.league,
                )
                st.session_state.current_spun_athlete = drawn
                st.session_state.drawn_names.add(drawn["name"])
                st.session_state.spin_step += 1
                st.session_state.skip_tokens -= 1
                st.rerun()

        with btn_c3:
            can_auto = (
                st.session_state.current_spun_athlete is not None
                and st.session_state.auto_tokens > 0
            )
            if st.button(
                f"🤖 Auto-Best Slot ({st.session_state.auto_tokens})",
                disabled=not can_auto,
                use_container_width=True,
            ):
                ath = st.session_state.current_spun_athlete
                best_idx = max(
                    (
                        i
                        for i in range(6)
                        if st.session_state.assigned_slots[i] is None
                    ),
                    key=lambda idx: ath["vals"][idx],
                )
                st.session_state.assigned_slots[best_idx] = ath
                st.session_state.current_spun_athlete = None
                st.session_state.auto_tokens -= 1
                st.rerun()

    # Active Spun Player Card
    curr_ath = st.session_state.current_spun_athlete
    if curr_ath is not None:
        disp_name = (
            curr_ath["safe"] if st.session_state.safe_mode else curr_ath["name"]
        )
        tier_map = {
            "GOAT": ("pill-goat", "👑 GOAT LEGEND"),
            "STAR": ("pill-star", "🌟 SUPERSTAR"),
            "SPEC": ("pill-spec", "🎯 HIGH-VARIANCE SPECIALIST"),
            "TRAP": ("pill-trap", "⚠️ DANGER TRAP"),
        }
        pill_cls, pill_txt = tier_map.get(curr_ath["tier"], ("pill-star", "STAR"))

        st.markdown(
            f"""
            <div class="spin-banner">
                <span class="tier-pill {pill_cls}">{pill_txt}</span>
                <h2 style="margin: 4px 0; color: #f8fafc;">{disp_name} <span style="color:#94a3b8;font-size:18px;">({curr_ath['team']})</span></h2>
                <p style="margin: 4px 0 12px 0; color: #a5b4fc; font-size: 14px;">
                    <strong>Scouting Report:</strong> {curr_ath['hint']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Show preview row (hidden in Blind Mode, visible in Scouted Mode)
        preview_cols = st.columns(6)
        for i, attr in enumerate(attributes):
            with preview_cols[i]:
                is_open = st.session_state.assigned_slots[i] is None
                if st.session_state.blind_mode:
                    shown_val = "??" if is_open else "🔒"
                else:
                    shown_val = f"{curr_ath['vals'][i]}"
                st.metric(label=attr, value=shown_val)
    elif filled_slots_count < 6:
        st.info(
            f"👆 Click **SPIN ATHLETE #{filled_slots_count + 1}** above to draw your next player, then pick which skill slot to lock in!"
        )

    st.markdown("---")

    # ------------------------------------------
    # 6-SLOT ATTRIBUTE BOARD & RADAR CHART
    # ------------------------------------------
    board_left, radar_right = st.columns([2.2, 1])

    with board_left:
        st.subheader(f"🛠️ {st.session_state.player_name}'s 6-Tool Blueprint")
        grid_cols = st.columns(3)

        for idx, attr in enumerate(attributes):
            with grid_cols[idx % 3]:
                assigned = st.session_state.assigned_slots[idx]
                if assigned is not None:
                    a_name = (
                        assigned["safe"]
                        if st.session_state.safe_mode
                        else assigned["name"]
                    )
                    val = assigned["vals"][idx]
                    card_cls = (
                        "filled-elite"
                        if val >= 94
                        else ("filled-good" if val >= 80 else "filled-trap")
                    )
                    val_color = (
                        "#facc15"
                        if val >= 94
                        else ("#60a5fa" if val >= 80 else "#f87171")
                    )
                    st.markdown(
                        f"""
                        <div class="slot-card {card_cls}">
                            <div style="font-size:11px; color:#cbd5e1; font-weight:700; text-transform:uppercase;">
                                {idx + 1}. {attr}
                            </div>
                            <div style="font-size:34px; font-weight:900; color:{val_color}; margin: 6px 0;">
                                {val}
                            </div>
                            <div style="font-size:13px; color:#f8fafc; font-weight:600;">
                                {a_name}
                            </div>
                            <div style="font-size:11px; color:#94a3b8;">
                                Team: {assigned['team']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    # Optional Swap Token allows replacing an already filled slot with current spun player
                    if (
                        curr_ath is not None
                        and st.session_state.swap_tokens > 0
                    ):
                        if st.button(
                            f"🔄 Overwrite ({st.session_state.swap_tokens} Swap)",
                            key=f"swap_{idx}",
                            use_container_width=True,
                        ):
                            st.session_state.assigned_slots[idx] = curr_ath
                            st.session_state.current_spun_athlete = None
                            st.session_state.swap_tokens -= 1
                            st.rerun()
                else:
                    preview_txt = (
                        f"Lock In ({curr_ath['vals'][idx]} Rating)"
                        if (curr_ath and not st.session_state.blind_mode)
                        else "Lock In Slot"
                    )
                    st.markdown(
                        f"""
                        <div class="slot-card">
                            <div style="font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase;">
                                {idx + 1}. {attr}
                            </div>
                            <div style="font-size:26px; font-weight:800; color:#475569; margin: 14px 0;">
                                OPEN SLOT
                            </div>
                            <div style="font-size:12px; color:#64748b;">
                                Waiting for assignment
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if curr_ath is not None:
                        if st.button(
                            f"⚡ {preview_txt}",
                            key=f"pick_{idx}",
                            type="primary",
                            use_container_width=True,
                        ):
                            st.session_state.assigned_slots[idx] = curr_ath
                            st.session_state.current_spun_athlete = None
                            st.rerun()

    with radar_right:
        st.subheader("🕸️ 6-Tool Radar DNA")
        radar_vals = [
            st.session_state.assigned_slots[i]["vals"][i]
            if st.session_state.assigned_slots[i] is not None
            else 0
            for i in range(6)
        ]
        st.markdown(
            generate_radar_svg(attributes, radar_vals),
            unsafe_allow_html=True,
        )

    # ------------------------------------------
    # FULL CAREER SIMULATION & SHARE SCORECARD
    # ------------------------------------------
    if filled_slots_count == 6:
        st.markdown("---")
        base_ovr = sum(radar_vals) // 6
        syn_bonus, syn_badges = evaluate_synergies(
            st.session_state.assigned_slots
        )
        final_ovr = min(99, base_ovr + syn_bonus)

        sim = simulate_career(
            st.session_state.league,
            st.session_state.assigned_slots,
            final_ovr,
        )

        st.subheader(
            f"🏆 Career Simulation Report: {st.session_state.player_name}"
        )

        if syn_badges:
            badge_html = "".join(
                f'<span class="synergy-chip">{b}</span>' for b in syn_badges
            )
            st.markdown(badge_html, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(
            "Final Composite OVR",
            f"{final_ovr} OVR",
            f"+{syn_bonus} Synergy" if syn_bonus > 0 else "Base Rating",
        )
        c2.metric("Legacy Tier", sim["tier"])
        c3.metric("Major Titles / Rings", f"{sim['titles']}")
        c4.metric("Hall of Fame Odds", sim["hof"])

        sc1, sc2, sc3 = st.columns(3)
        for i in range(3):
            sc1.metric(league_cfg["stat_labels"][0], sim["stats"][0]) if i == 0 else None
            sc2.metric(league_cfg["stat_labels"][1], sim["stats"][1]) if i == 1 else None
            sc3.metric(league_cfg["stat_labels"][2], sim["stats"][2]) if i == 2 else None

        col_story, col_share = st.columns([1.6, 1])
        with col_story:
            st.markdown("#### 📜 Career Storyline Chronicle")
            for event in sim["timeline"]:
                st.markdown(f"- {event}")

            if st.button("🏛️ Save Build to Session Leaderboard"):
                st.session_state.hall_of_fame_log.append(
                    {
                        "Prospect": st.session_state.player_name,
                        "League": st.session_state.league,
                        "Mode": st.session_state.game_mode,
                        "Final OVR": final_ovr,
                        "Tier": sim["tier"],
                        "Titles": sim["titles"],
                        "HOF Odds": sim["hof"],
                    }
                )
                st.success("Saved to Session Leaderboard tab!")

        with col_share:
            st.markdown("#### 📲 Shareable Group-Chat Scorecard")
            emoji_bars = "".join(
                "🟨" if v >= 95 else ("🟦" if v >= 85 else ("🟩" if v >= 75 else "🟥"))
                for v in radar_vals
            )
            lines = [
                f"⚡ PLAYER FORGE | {st.session_state.league}",
                f"👤 {st.session_state.player_name} — {final_ovr} OVR ({sim['tier']})",
                f"📊 DNA: {emoji_bars}",
            ]
            for i, attr in enumerate(attributes):
                ath = st.session_state.assigned_slots[i]
                nm = ath["safe"] if st.session_state.safe_mode else ath["name"]
                lines.append(f"• {attr}: {radar_vals[i]} ({nm})")
            lines.append(
                f"🏆 Titles: {sim['titles']} | HOF: {sim['hof']}"
            )
            st.code("\n".join(lines), language="text")


# ==========================================
# TAB 2: LEAGUE SCOUTING DEX (ALL PLAYERS)
# ==========================================
with tab_dex:
    st.subheader(f"📖 {st.session_state.league} Athlete Database ({len(pool)} Players)")
    st.caption(
        "Use this database in Free Play or study up before tackling Authentic Blind Mode!"
    )
    dex_rows = []
    for a in pool:
        row = {
            "Athlete": a["safe"] if st.session_state.safe_mode else a["name"],
            "Team": a["team"],
            "Tier": a["tier"],
            "Avg OVR": int(sum(a["vals"]) / 6),
        }
        for i, attr in enumerate(attributes):
            row[attr] = a["vals"][i]
        dex_rows.append(row)
    df_dex = pd.DataFrame(dex_rows).sort_values(by="Avg OVR", ascending=False)
    st.dataframe(df_dex, use_container_width=True, hide_index=True)


# ==========================================
# TAB 3: SESSION HALL OF FAME LEADERBOARD
# ==========================================
with tab_hof:
    st.subheader("🏛️ Session Hall of Fame Leaderboard")
    if st.session_state.hall_of_fame_log:
        df_hof = pd.DataFrame(st.session_state.hall_of_fame_log).sort_values(
            by="Final OVR", ascending=False
        )
        st.dataframe(df_hof, use_container_width=True, hide_index=True)
    else:
        st.info(
            "Complete a 6-slot player build in the **Forge Arena** and click **Save Build to Session Leaderboard** to rank your creations here!"
        )

# ==========================================
# FOOTER DISCLAIMER
# ==========================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 12px;">
        <strong>Player Forge</strong> is an independent, fan-made sports trivia and attribute drafting simulation.
        Not affiliated with, endorsed by, or licensed by the NBA, NFL, FIFA, ATP, WTA, or any players association.
    </div>
    """,
    unsafe_allow_html=True,
)
