import pandas as pd
import random

# Generate random energy usage data for a week
usage_data = pd.DataFrame({
    "day": range(7),
    "usage": [random.uniform(10, 25) for _ in range(7)],
    "temperature": [random.uniform(15, 35) for _ in range(7)],  # Add random temperature data
})

# Add a "day_name" column to the data based on the day of the week
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
usage_data["day_name"] = usage_data["day"].apply(lambda x: day_names[x % 7])

# Add an "is_weekend" column to the data (1 for weekends and 0 for weekdays)
usage_data["is_weekend"] = usage_data["day"].apply(lambda x: 1 if x % 7 >= 5 else 0)

# Save the data to a CSV file
# usage_data.to_csv("home\\energy_usage_extended.csv", index=False)
usage_data.to_csv("C:\\Users\\dimil\\Documents\\workspace-home\\home\\energy_usage_extended.csv", index=False)

# This modified code adds a "temperature" column with random temperature values between 15 and 35 degrees Celsius, as well as an "is_weekend" column, which takes the value 1 for weekends and 0 for weekdays. The new CSV file is called "energy_usage_extended.csv".