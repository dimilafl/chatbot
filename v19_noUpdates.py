import random
import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# new additions

def handle_complex_question(question, appliance_data):
    # Identify if the question is about appliances and energy usage
    question_about_appliances = False
    question_about_energy_usage = False
    appliance_name = None

    for key in appliance_data.keys():
        if key in question.lower():
            question_about_appliances = True
            appliance_name = key

    if any(keyword in question.lower() for keyword in ["energy", "power", "usage", "consumption"]):
        question_about_energy_usage = True

    if question_about_appliances and question_about_energy_usage:
        if appliance_name:
            # Respond with the energy usage of the specific appliance
            response = f"The {appliance_name.capitalize()} is using {appliance_data[appliance_name]} kWh of energy."
        else:
            # Respond with a breakdown of energy usage by appliance
            response = "Here's a breakdown of energy usage by appliance:\n\n"
            for appliance, usage in appliance_data.items():
                response += f"{appliance.capitalize()}: {usage} kWh\n"
        return response

    # If no matches or only partial matches, return a default response
    return "I'm sorry, I didn't understand your question. Could you please try again?"



#In order to provide a breakdown of energy usage by appliance, I need to have data on the energy usage of various appliances.
#For this example, I created a sample dictionary containing energy usage data for different appliances:


appliance_data = {
    "refrigerator": 2.0,
    "washing machine": 0.5,
    "air conditioner": 4.0,
    "tv": 0.8,
    "oven": 1.5,
}

appliance_categories = {
    "Kitchen Appliances": ["refrigerator", "oven"],
    "Laundry Appliances": ["washing machine"],
    "Entertainment": ["tv"],
    "Cooling & Heating": ["air conditioner"],
}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Load the historical energy usage data
# usage_data = pd.read_csv("ML\energy_usage.csv")

#Randomized data
# usage_data = pd.read_csv("home\energy_usage_daynames.csv")


# Load the extended historical energy usage data
try:
    usage_data = pd.read_csv("home\energy_usage_extended.csv")
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
X = usage_data[["day", "temperature", "is_weekend"]]
y = usage_data["usage"].values
try:
    model = LinearRegression().fit(X, y)
except ValueError:
    print("Error: There is an issue with the format of the energy usage data.")
    exit()


# Create a DataFrame with the same feature names for prediction
new_data = pd.DataFrame(data=[[datetime.datetime.now().weekday(), 22, 0]], columns=["day", "temperature", "is_weekend"])

# Use the model to predict energy usage for the new_data
predicted_usage = model.predict(new_data)



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
    
    # "help": "Sure, here are some things you can do to monitor your energy usage:\n\n- Use a smart thermostat to control your heating and cooling\n- Install a whole-house energy monitor\n- Use a power meter to measure individual appliance usage",
    "help": "Sure, here are some things you can do to monitor your energy usage:\n\n- Use a smart thermostat to control your heating and cooling\n- Install a whole-house energy monitor\n- Use a power meter to measure individual appliance usage\n- Type 'chart' to see a chart of your energy usage over time\n- Type 'heatmap' to see a heatmap of energy usage by time of day",

    "tip": None, # We'll set the tip based on energy usage later
    
    "usage":  "Let me check your energy usage for today... According to our records, you've used " + "{:.2f}".format(model.predict([[datetime.datetime.now().weekday(), 22, 0]])[0]) + " kWh so far today.",
    
    
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
                new_data = pd.DataFrame(data=[[datetime.datetime.now().weekday(), 22, 0]], columns=["day", "temperature", "is_weekend"])
                usage = model.predict(new_data)[0]

                # Choose a tip based on the user's energy usage
                if usage < 16:
                    tip = random.choice(low_usage_tips)
                elif usage < 20:
                    tip = random.choice(medium_usage_tips)
                else:
                    tip = random.choice(high_usage_tips)
                
                # Set the tip in the responses dictionary
                responses["tip"] = tip

            elif user_input == "usage":
                # Get the user's energy usage for today
                new_data = pd.DataFrame(data=[[datetime.datetime.now().weekday(), 22, 0]], columns=["day", "temperature", "is_weekend"])
                usage = model.predict(new_data)[0]

                # Set the usage in the responses dictionary
                responses["usage"] = f"Let me check your energy usage for today... According to our records, you've used {usage:.2f} kWh so far today."

            # Respond to the user's input
            print("Chatbot: " + responses[user_input])
            
            if user_input == "bye":
                break
        elif user_input == "time":
            print("Chatbot: The current time is " +
                  datetime.datetime.now().strftime("%H:%M:%S") + ".")
            
        elif user_input == "chart":
            plot_energy_usage_over_time(usage_data)
        elif user_input == "heatmap":
            plot_energy_usage_heatmap()
        elif user_input == "bar chart":
            plot_energy_usage_bar_chart(appliance_data)
        elif user_input == "pie chart":
            plot_energy_usage_pie_chart(appliance_data)




        else:
            response = handle_complex_question(user_input, appliance_data)
            print("Chatbot: " + response)



def plot_energy_usage_over_time(usage_data):
    days = usage_data["day_name"]
    usage = usage_data["usage"]

    plt.figure(figsize=(10, 5))
    plt.plot(days, usage, marker='o', linestyle='-', linewidth=2)
    plt.xlabel('Days of the Week')
    plt.ylabel('Energy Usage (kWh)')
    plt.title('Energy Usage Over Time')
    plt.grid(True)
    plt.show()


def plot_energy_usage_heatmap():
    # Generate random hourly energy usage data for a week
    hourly_usage = np.random.rand(7, 24)

    # Create a heatmap
    plt.figure(figsize=(12, 6))
    plt.imshow(hourly_usage, cmap='hot', aspect='auto', interpolation='nearest')
    plt.colorbar(label='Energy Usage (kWh)')

    # Label the x-axis with hours of the day and the y-axis with days of the week
    plt.xticks(range(0, 24), range(1, 25))
    plt.yticks(range(0, 7), ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    plt.xlabel('Hour of the Day')
    plt.ylabel('Day of the Week')
    plt.title('Energy Usage Heatmap')
    plt.show()


def plot_energy_usage_bar_chart(appliance_data):
    categories = []
    usage = []

    for category, appliances in appliance_categories.items():
        categories.append(category)
        category_usage = sum([appliance_data[appliance] for appliance in appliances])
        usage.append(category_usage)

    plt.figure(figsize=(10, 5))
    plt.bar(categories, usage)
    plt.xlabel("Appliance Categories")
    plt.ylabel("Energy Usage (kWh)")
    plt.title("Energy Usage by Appliance Category")
    plt.show()

def plot_energy_usage_pie_chart(appliance_data):
    categories = []
    usage = []

    for category, appliances in appliance_categories.items():
        categories.append(category)
        category_usage = sum([appliance_data[appliance] for appliance in appliances])
        usage.append(category_usage)

    plt.figure(figsize=(8, 8))
    plt.pie(usage, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title("Energy Usage by Appliance Category")
    plt.axis("equal")
    plt.show()




# Run the chatbot
if __name__ == "__main__":
    main()




#error

# C:\Users\dimil\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\sklearn\base.py:439: UserWarning: X does not have valid feature names, but LinearRegression was fitted with feature names
#   warnings.warn(






# In this updated code, I added error handling using try-except blocks to 
# catch potential issues with loading the energy usage data or fitting the linear regression model. 
# If there are any issues, the code will print an error message and exit the program.

# This error handling will help ensure that the chatbot runs 
# smoothly and provides helpful error messages to the user 
# if any issues occur.





# inputs
# ~~~~~~~~~~~~~~~~~~~~~~
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



# new ones... try this
    # time
    # chart
    # heatmap

    # bar chart
    # pie chart

#NLP
    # What appliances are using the most energy in my home?
    
    # What devices/appliances are using the most energy in my home?

    # How much energy is the refrigerator using?

    # How much energy is the washing machine using?
    # How much energy is the air conditioner using?

# ~~~~~~~~~~~~~~~~~~~~~~





#for tips i always get the same answer back - worry abt later
    # done

#history would be better if it corresponded to a day rather than a number
    # done

# randomizer for excel - new outputs created for demonstration
    # done

# figure out how to demo it given workplace limitations

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




# old documentation -

    # used the matplotlib library to create visualizations

    # With these changes, users can now type 'chart' to visualize their energy usage over time and 'heatmap' to see 
    # which times of the day they tend to use the most energy.

# new documentation -

    # With these changes, my chatbot will be able to handle more complex questions about energy usage and appliances. 
    # This is a basic example, and I can extend the natural language processing capabilities of my chatbot by creating more patterns and rules to handle other types of questions. 
    # I can also integrate more advanced NLP techniques, such as intent classification and entity extraction, using libraries like Rasa or Dialogflow.

# newest documentation -

# In this example, I added weather data (temperature) and day type (is_weekend) as additional features to improve the linear regression model's performance. I can further enhance the model by incorporating more features, such as user-specific behavior patterns, or by using more advanced machine learning algorithms such as decision trees, random forests, or gradient boosting machines.
# Remember to collect and preprocess the additional data needed for these new features before incorporating them into your model.
