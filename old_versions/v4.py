import random
import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the historical energy usage data
usage_data = pd.read_csv("ML\energy_usage.csv")

# Fit a linear regression model to the data
X = usage_data["day"].values.reshape(-1, 1)
y = usage_data["usage"].values
model = LinearRegression().fit(X, y)

# Define some energy-saving tips
tips = [
    "Reduce your energy usage during peak hours to save money on your energy bills.",
    "Monitor your energy usage regularly to identify areas where you can save energy.",
    "Invest in smart home devices that can automatically adjust your energy usage based on your needs and preferences.",
    "Consider using renewable energy sources like solar panels to generate your own electricity.",
]

# Define the chatbot's responses
responses = {
    "hi": "Hello! How can I help you monitor your energy usage today?",
    "help": "Sure, here are some things you can do to monitor your energy usage:\n\n" + "\n\n".join(tips),
    "tip": random.choice(tips),
    "usage": "Let me check your energy usage for today... According to our records, you've used " +
             "{:.2f}".format(model.predict([[datetime.datetime.now().weekday()]])[0]) +
             " kWh so far today.",
    "history": "Here's a summary of your energy usage for the past week:\n\n" + usage_data[["day_name", "usage"]].to_string(index=False),
    "bye": "Goodbye! Remember to always monitor your energy usage!",
}

# Define the chatbot's main loop
def main():
    while True:
        user_input = input("You: ").lower()
        if user_input in responses:
            print("Chatbot: " + responses[user_input])
            if user_input == "bye":
                break
        elif user_input == "time":
            print("Chatbot: The current time is " +
                  datetime.datetime.now().strftime("%H:%M:%S") + ".")
        else:
            print("Chatbot: I'm sorry, I didn't understand. Could you please try again?")

# Run the chatbot
if __name__ == "__main__":
    main()



# inputs
    # hi
    # help
    # tip
    # usage
    # history
    # bye



#for tips i always get the same answer back - worry abt later

#history would be better if it corresponded to a day rather than a number
    # done

# randomizer for excel - new outputs created for demonstration
# figure out how to demo it giving workplace limitations




#limited w/ 25 every 3hr
    # 100 every 12

# description

    #The machine learning aspect of this code involves using historical energy usage data to train a linear regression model, which can then be used to predict the user's energy usage for the current day.
    # The code loads the historical energy usage data from a CSV file and uses the scikit-learn library to fit a linear regression model to the data. The input to the model is the day of the week (represented as an integer between 0 and 6), and the output is the energy usage for that day.
    # Once the model is trained, the chatbot can use it to provide personalized responses based on the user's energy usage. For example, the usage response uses the model to predict the user's energy usage for the current day, based on the day of the week. The history response provides a summary of the user's energy usage for the past week, based on the historical data that was used to train the model.
    # Overall, the machine learning aspect of this code allows the chatbot to provide more personalized and accurate responses based on the user's energy usage patterns, which can help the user better understand their energy usage and identify areas where they can save energy and reduce costs.