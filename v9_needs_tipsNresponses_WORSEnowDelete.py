import random
import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the historical energy usage data
try:
    usage_data = pd.read_csv("home\energy_usage_daynames.csv")
except FileNotFoundError:
    print("Error: Could not find the energy usage data file.")
    exit()
except pd.errors.EmptyDataError:
    print("Error: The energy usage data file is empty.")
    exit()
except pd.errors.ParserError:
    print("Error: There is an issue with the format of the energy usage data file.")
    exit()

# Fit a linear regression model to the data
X = usage_data["day"].values.reshape(-1, 1)
y = usage_data["usage"].values
try:
    model = LinearRegression().fit(X, y)
except ValueError:
    print("Error: There is an issue with the format of the energy usage data.")
    exit()

# Define the chatbot's main loop
def main():
    while True:
        user_input = input("You: ").lower()
        
        if user_input == "usage":
            usage = model.predict([[datetime.datetime.now().weekday()]])[0]
            print("Chatbot: Let me check your energy usage for today... According to our records, you've used {:.2f} kWh so far today.".format(usage))
        
        elif user_input == "history":
            print("Chatbot: Here's a summary of your energy usage for the past week:\n\n" + usage_data[["day_name", "usage"]].to_string(index=False))
        
        elif user_input == "bye":
            print("Chatbot: Goodbye! Remember to always monitor your energy usage!")
            break
        
        elif user_input == "time":
            print("Chatbot: The current time is " + datetime.datetime.now().strftime("%H:%M:%S") + ".")
        
        else:
            print("Chatbot: I'm sorry, I didn't understand. Could you please try again?")

# Run the chatbot
if __name__ == "__main__":
    main()


# I've removed the tips and responses sections and restructured the main loop to handle user input directly with if-elif-else statements. The chatbot will now provide energy usage, history, time, and goodbye messages without providing energy-saving tips.