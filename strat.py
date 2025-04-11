import fastf1
from matplotlib import pyplot as plt
import fastf1.plotting
import os
from pathlib import Path

session = fastf1.get_session(2024, 'Monaco','R')
session.load()

laps = session.laps
drivers = session.drivers
print(drivers)

drivers = [session.get_driver(driver)['Abbreviation'] for driver in drivers]
print(drivers)

stints = laps[['Driver', 'Stint', 'Compound', 'LapNumber']]
stints = stints.groupby(['Driver', 'Stint', 'Compound']).count().reset_index()
stints = stints.rename(columns={'LapNumber': 'StintLength'})

fig, ax = plt.subplots(figsize=(5, 10))
for driver in drivers:
  driver_stints = stints[stints['Driver']==driver]

  previous_stint_end = 0
  for idx, row in driver_stints.iterrows():
        compound_color = fastf1.plotting.get_compound_color(row["Compound"],
                                                            session=session)
        plt.barh(
            y=driver,
            width=row["StintLength"],
            left=previous_stint_end,
            color=compound_color,
            edgecolor="black",
            fill=True
        )

        previous_stint_end += row["StintLength"]

plt.title("2024 Monaco Grand Prix Strategies")
plt.xlabel("Lap Number")
plt.grid(False)
ax.invert_yaxis()

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()

output_dir = os.path.join(str(Path.home()),'tyre_strat','stratgies')
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, 'monaco.png'))