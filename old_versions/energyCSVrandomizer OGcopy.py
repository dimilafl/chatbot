# code that generates random energy usage data and adds a "day_name" column to it based on 
# the day of the week:

import pandas as pd
import random

# Generate random energy usage data for a week
usage_data = pd.DataFrame({
    "day": range(7),
    "usage": [random.uniform(10, 25) for _ in range(7)]
})

# Add a "day_name" column to the data based on the day of the week
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
usage_data["day_name"] = usage_data["day"].apply(lambda x: day_names[x % 7])

# Save the data to a CSV file
usage_data.to_csv("home\energy_usage_daynames.csv", index=False)


# This code generates random energy usage data for a week using the random.uniform() function, 
# and then adds a new "day_name" column to it based on the day of the week using the modulo operator.
# Finally, the data is saved to a CSV file called "energy_usage_daynames.csv".