import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean data
df = pd.read_csv("data/premier_league_standard_stats.csv")

# Rename columns
df = df.rename(columns={
	'Unnamed: 1' : 'Player',
	'Unnamed: 4' : 'Squad',
	'Playing Time.2' : 'Minutes'
})

# Convert minutes to numeric
df['Minutes'] = pd.to_numeric(df['Minutes'], errors='coerce')

# Filter out any rows without player names or minutes
df = df.dropna(subset=['Player', 'Minutes'])

# Get top 10 players by minutes played
most_minutes = df.sort_values(by='Minutes', ascending=False)[['Player', 'Squad', 'Minutes']].head(10)

# Print result
print("Top 10 Players with Most Minutes Played:")
print(most_minutes)

# Plot result
plt.figure(figsize=(10, 6))
sns.barplot(data=most_minutes, x='Minutes', y='Player', palette='viridis')
plt.title('Top 10 Players with Most Minutes Played (Premier League)')
plt.xlabel('Minutes Played')
plt.ylabel('Player')
plt.tight_layout()
plt.savefig("outputs/minutes_played.png")
print("Chart saved to outputs/minutes_played.png")
plt.show()
