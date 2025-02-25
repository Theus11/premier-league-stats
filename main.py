# ----------------------------
# Import Libraries
# ----------------------------
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Data Loading & Preparation
# ----------------------------
# Load match data from CSV
df = pd.read_csv('data/PremierLeague.csv')

# Calculate points for each match outcome
df['home_points'] = df.apply(
    lambda row: 3 if row['home_team_goals'] > row['away_team_goals'] 
    else 1 if row['home_team_goals'] == row['away_team_goals'] 
    else 0, 
    axis=1
)

df['away_points'] = df.apply(
    lambda row: 3 if row['away_team_goals'] > row['home_team_goals'] 
    else 1 if row['away_team_goals'] == row['home_team_goals'] 
    else 0, 
    axis=1
)

# ----------------------------
# Data Transformation
# ----------------------------
# Create unified team performance dataset
home_teams = df[['round_number', 'home_team_name', 'home_points']].rename(
    columns={'home_team_name': 'team', 'home_points': 'points'}
).assign(is_home=True)

away_teams = df[['round_number', 'away_team_name', 'away_points']].rename(
    columns={'away_team_name': 'team', 'away_points': 'points'}
).assign(is_home=False)

team_points = pd.concat([home_teams, away_teams], ignore_index=True)

# ----------------------------
# Points Calculation
# ----------------------------
# Calculate total points and identify top 8 teams
total_points = team_points.groupby('team')['points'].sum().sort_values(ascending=False)
top_8_teams = total_points.head(8).index.tolist()  # Convert to list for consistent indexing

# Calculate cumulative points progression
points_per_round = (
    team_points.groupby(['team', 'round_number'])['points']
    .sum()
    .reset_index()
    .sort_values(['team', 'round_number'])
)
points_per_round['cumulative_points'] = points_per_round.groupby('team')['points'].cumsum()

# Pivot data for visualization
cumulative_pivot = points_per_round.pivot(
    index='round_number', 
    columns='team', 
    values='cumulative_points'
)[top_8_teams]  # Filter to top 8 teams

# ----------------------------
# Visualization Setup
# ----------------------------
# Define team colors (using official club colors where possible)
TEAM_COLORS = {
    'Manchester City': '#99c5ea',    # Sky blue
    'Arsenal': '#f40000',           # Arsenal red
    'Liverpool': '#e8d30e',         # Liverpool gold
    'Aston Villa': '#69091c',       # Claret
    'Tottenham Hotspur': '#001051', # Navy blue
    'Chelsea': '#0825db',           # Royal blue
    'Manchester United': '#be0000', # Manchester red
    'Newcastle United': '#000000'   # Black
}

# Configure plot style
plt.style.use('seaborn-v0_8-darkgrid')
plt.figure(figsize=(12, 6))

# ----------------------------
# Plot Construction
# ----------------------------
# Create line plots for each team
for team in cumulative_pivot.columns:
    plt.plot(
        cumulative_pivot.index, 
        cumulative_pivot[team], 
        linestyle='-', 
        marker='o',
        markevery=(18, 19),    # Add markers every 18 rounds starting at 19
        markersize=5,
        color=TEAM_COLORS[team],
        label=team,
        zorder=2  # Ensure lines appear above grid
    )

# ----------------------------
# Plot Customization
# ----------------------------
# Axis configuration
plt.xticks(range(0, 38, 3), rotation=15)  # Show every 3rd round
plt.yticks(range(0, 100, 10))             # Y-axis in 10-point increments
plt.xlim(0, 39)                           # Buffer for annotation space
plt.ylim(-1, 92)                          # Buffer for annotation space

# Grid & Background customization
plt.grid(
    True,
    linestyle='--',
    linewidth=1,
    alpha=0.7,
    color='gray',
    zorder=1  # Keep grid below data lines
)
plt.gca().set_facecolor('whitesmoke')

# Key annotation for Arsenal's performance
plt.annotate(
    'Arsenal loss vs Aston Villa cost them the title',
    xy=(33, cumulative_pivot.loc[33, 'Arsenal']),
    xytext=(33, 85),
    arrowprops=dict(
        facecolor='#f40000',
        arrowstyle='->',
        connectionstyle="arc3,rad=-0.2"
    ),
    horizontalalignment='right',
    fontsize=9,
    fontweight='semibold'
)

# Labels & Title
plt.xlabel('Round Number', fontsize=12, labelpad=10)
plt.ylabel('Points', fontsize=12, labelpad=10)
plt.title(
    "Premier League 2023: Cumulative Points by Team", 
    fontsize=16, 
    fontweight='bold', 
    pad=20
)

# Legend customization
legend = plt.legend(
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    frameon=True,
    framealpha=0.9,
    title='Teams',
    title_fontsize='12'
)

# ----------------------------
# Output & Saving
# ----------------------------
plt.tight_layout()
plt.savefig(
    'output/cumulative_points.png',
    dpi=300,
    bbox_inches='tight',
    transparent=False
)
plt.show()