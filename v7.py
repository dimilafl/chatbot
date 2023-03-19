import random
import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the historical energy usage data
# usage_data = pd.read_csv("ML\energy_usage.csv")

#Randomized data
usage_data = pd.read_csv("home\energy_usage_daynames.csv")

# Fit a linear regression model to the data
X = usage_data["day"].values.reshape(-1, 1)
y = usage_data["usage"].values
model = LinearRegression().fit(X, y)

# Define some energy-saving tips based on energy usage
low_usage_tips = [
    "Great job on reducing your energy usage! Here are some more tips to help you save even more:\n\n- Unplug electronics and appliances when not in use\n- Use LED light bulbs\n- Turn off lights when leaving a room",
    "You're doing a great job at saving energy! Here are some more tips to help you save:\n\n- Adjust your thermostat by a few degrees\n- Use a clothesline instead of a dryer\n- Cook with small appliances instead of a stove or oven",
    "Congratulations on your low energy usage! Here are some more tips to help you save even more:\n\n- Use natural light instead of artificial light\n- Turn off your computer and monitor when not in use\n- Use a power strip to reduce standby power",
]

medium_usage_tips = [
    "You're doing pretty well with your energy usage! Here are some tips to help you save more:\n\n- Seal air leaks around windows and doors\n- Use ceiling fans instead of air conditioning\n- Reduce water heater temperature",
    "You're on the right track with your energy usage! Here are some more tips to help you save:\n\n- Replace old appliances with energy-efficient models\n- Plant shade trees or install shading devices\n- Use a programmable thermostat",
    "You're doing a decent job with your energy usage! Here are some more tips to help you save:\n\n- Insulate your home to reduce heating and cooling costs\n- Use a microwave instead of a conventional oven\n- Turn off your water heater when you're away",
]

high_usage_tips = [
    "You're using a lot of energy! Here are some tips to help you reduce your usage:\n\n- Upgrade to energy-efficient windows\n- Install a solar water heater\n- Use a pool cover to reduce evaporation",
    "You have a lot of room for improvement with your energy usage! Here are some tips to help you save more:\n\n- Use a clothesline instead of a dryer\n- Install energy-efficient lighting\n- Use a low-flow showerhead",
    "You're using a lot of energy! Here are some more tips to help you save:\n\n- Install a programmable thermostat\n- Upgrade to an energy-efficient HVAC system\n- Install energy-efficient doors",
]

# Define the chatbot's responses
responses = {
    "hi": "Hello! How can I help you monitor your energy usage today?",
    "help": "Sure, here are some things you can do to monitor your energy usage:\n\n- Use a smart thermostat to control your heating and cooling\n- Install a whole-house energy monitor\n- Use a power meter to measure individual appliance usage",
    "tip": None, # We'll set the tip based on energy usage later
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
            if user_input == "tip":
                # Get the user's energy usage for today
                usage = model.predict([[datetime.datetime.now().weekday()]])[0]

                # Choose a tip based on the user's energy usage
                if usage < 16:
                    tip = random.choice(low_usage_tips)
                elif usage < 20:
                    tip = random.choice(medium_usage_tips)
                else:
                    tip = random.choice(high_usage_tips)
                
                # Set the tip in the responses dictionary
                responses["tip"] = tip

            # Respond to the user's input
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

#stuff worth using
    # history
    # usage
    # tip




#for tips i always get the same answer back - worry abt later

#history would be better if it corresponded to a day rather than a number
    # done

# randomizer for excel - new outputs created for demonstration
    # done

# figure out how to demo it giving workplace limitations

#limited w/ 25 every 3hr
    # 100 every 12

# description

    #The machine learning aspect of this code involves using historical energy usage data to train a linear regression model, which can then be used to predict the user's energy usage for the current day.
    # The code loads the historical energy usage data from a CSV file and uses the scikit-learn library to fit a linear regression model to the data. The input to the model is the day of the week (represented as an integer between 0 and 6), and the output is the energy usage for that day.
    # Once the model is trained, the chatbot can use it to provide personalized responses based on the user's energy usage. For example, the usage response uses the model to predict the user's energy usage for the current day, based on the day of the week. The history response provides a summary of the user's energy usage for the past week, based on the historical data that was used to train the model.
    # Overall, the machine learning aspect of this code allows the chatbot to provide more personalized and accurate responses based on the user's energy usage patterns, which can help the user better understand their energy usage and identify areas where they can save energy and reduce costs.










# In this updated code, I added three lists of energy-saving tips based on energy usage levels: `low_usage_tips`, `medium_usage_tips`, and `high_usage_tips`. These lists contain specific tips that are more relevant to users with different levels of energy usage.
# I also modified the `responses` dictionary to set the `tip` response to `None`, since we'll set it later based on the user's energy usage.
# Finally, I added some code to the `main` function that sets the `tip` response based on the user's energy usage. The code uses the linear regression model to predict the user's energy usage for the current day, and then selects a tip list based on the energy usage level. A random tip is then selected from the corresponding list and set as the `tip` response in the `responses` dictionary.
# With these changes, the chatbot should provide more personalized energy-saving tips based on the user's energy usage levels.