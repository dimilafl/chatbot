import random
import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import spacy
from spacy.matcher import Matcher
import re
import Levenshtein


nlp = spacy.load("en_core_web_sm")

def validate_user_input(user_input):
    if len(user_input) > 100:
        print("Chatbot: Your input is too long. Please keep it under 100 characters.")
        return False

    if not re.match(r'^[\w\s]+$', user_input):
        print("Chatbot: Invalid characters detected. Please use only alphanumeric characters and spaces.")
        return False

    return True

def find_closest_keyword(user_input):
    min_distance = float('inf')
    closest_keyword = None

    for keyword in responses.keys():
        distance = Levenshtein.distance(user_input, keyword)
        if distance < min_distance:
            min_distance = distance
            closest_keyword = keyword

    return closest_keyword if min_distance <= 2 else None

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
    pass

def handle_temperature_question():
    return "The current temperature is 22°C."

def handle_day_question():
    return f"Today is {datetime.datetime.now().strftime('%A')}."

patterns = [
    (re.compile(r'how hot.*|.*temperature.*'), handle_temperature_question),
    (re.compile(r'what day.*|.*day today.*'), handle_day_question),
]

def process_user_input(user_input):
    doc = nlp(user_input)

    for token in doc:
        if token.dep_ == "ROOT":
            if token.lemma_ == "temperature":
                return handle_temperature_question()
            elif token.lemma_ == "day":
                return handle_day_question()

    return None

#In order to provide a breakdown of energy usage by appliance, I need to have data on the energy usage of various appliances.
#For this example, I created a sample dictionary containing energy usage data for different appliances:
appliance_data = {
    "refrigerator": 2.0,
    "washing machine": 0.5,
    "air conditioner": 4.0,
    "tv": 0.8,
    "oven": 1.5,
    "dishwasher": 1.3,
    "dryer": 3.0,
    "microwave": 0.6,
    "computer": 0.4,
    "water heater": 4.5,
}
appliance_categories = {
    "Kitchen Appliances": ["refrigerator", "oven", "dishwasher", "microwave"],
    "Laundry Appliances": ["washing machine", "dryer"],
    "Entertainment": ["tv", "computer"],
    "Cooling & Heating": ["air conditioner", "water heater"],
}

def calculate_total_energy_usage(appliance_data):
    return sum(appliance_data.values())

def calculate_energy_percentage_per_category(appliance_data, appliance_categories):
    total_energy = calculate_total_energy_usage(appliance_data)
    percentages = {}
    for category, appliances in appliance_categories.items():
        category_usage = sum([appliance_data[appliance] for appliance in appliances])
        percentages[category] = (category_usage / total_energy) * 100
    return percentages

def calculate_energy_difference(appliance1, appliance2, appliance_data):
    if appliance1 in appliance_data and appliance2 in appliance_data:
        difference = abs(appliance_data[appliance1] - appliance_data[appliance2])
        return difference
    else:
        return None

def save_energy_usage_bar_chart(appliance_data, file_name):
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
    plt.savefig(file_name)
    print(f"Chatbot: Energy usage bar chart saved as '{file_name}'")

# Add new functions
def find_highest_energy_appliance(appliance_data):
    return max(appliance_data, key=appliance_data.get)

def find_lowest_energy_appliance(appliance_data):
    return min(appliance_data, key=appliance_data.get)

def calculate_average_energy_usage(appliance_data):
    total_energy = calculate_total_energy_usage(appliance_data)
    num_appliances = len(appliance_data)
    return total_energy / num_appliances

# Load the extended historical energy usage data
try:
    usage_data = pd.read_csv("/Users/dimitrilafleur/Documents/GitHub/chatbot/energy_usage_extended.csv")

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
    "help": "Sure, here are some things you can do to monitor your energy usage:\n\n- Use a smart thermostat to control your heating and cooling\n- Install a whole-house energy monitor\n- Use a power meter to measure individual appliance usage\n- Type 'chart' to see a chart of your energy usage over time\n- Type 'heatmap' to see a heatmap of energy usage by time of day",
    "tip": None, # We'll set the tip based on energy usage later
    "usage":  "Let me check your energy usage for today... According to our records, you've used " + "{:.2f}".format(model.predict([[datetime.datetime.now().weekday(), 22, 0]])[0]) + " kWh so far today.",
    "history": "Here's a summary of your energy usage for the past week:\n\n" + usage_data[["day_name", "usage"]].to_string(index=False),
    "bye": "Goodbye! Remember to always monitor your energy usage!",
}

# Define the chatbot's main loop
def main():
    while True:
        try:
            user_input = input("You: ").lower()
            
            if not validate_user_input(user_input):
                continue

            matched_pattern = False

            for pattern, handler in patterns:
                if pattern.match(user_input):
                    print("Chatbot:", handler())
                    matched_pattern = True
                    break

            if matched_pattern:
                continue

            processed_input = process_user_input(user_input)

            if processed_input is not None:
                print("Chatbot:", processed_input)
                continue


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



            # New inputs for the chatbot
            elif user_input == "weekday_usage":
                print("Chatbot: The average energy usage on weekdays is {:.2f} kWh.".format(usage_data.loc[usage_data['is_weekend'] == 0, 'usage'].mean()))
                
            elif user_input == "weekend_usage":
                print("Chatbot: The average energy usage on weekends is {:.2f} kWh.".format(usage_data.loc[usage_data['is_weekend'] == 1, 'usage'].mean()))
            
            elif user_input == "highest_usage_day":
                day, usage = usage_data.loc[usage_data['usage'].idxmax(), ['day_name', 'usage']]
                print(f"Chatbot: The highest energy usage was on {day} with {usage:.2f} kWh.")
            
            elif user_input == "lowest_usage_day":
                day, usage = usage_data.loc[usage_data['usage'].idxmin(), ['day_name', 'usage']]
                print(f"Chatbot: The lowest energy usage was on {day} with {usage:.2f} kWh.")
            
            elif user_input == "compare_weekday_weekend":
                weekday_mean = usage_data.loc[usage_data['is_weekend'] == 0, 'usage'].mean()
                weekend_mean = usage_data.loc[usage_data['is_weekend'] == 1, 'usage'].mean()
                if weekday_mean > weekend_mean:
                    difference = weekday_mean - weekend_mean
                    print(f"Chatbot: Your energy usage on weekdays is higher than weekends by {difference:.2f} kWh on average.")
                elif weekend_mean > weekday_mean:
                    difference = weekend_mean - weekday_mean
                    print(f"Chatbot: Your energy usage on weekends is higher than weekdays by {difference:.2f} kWh on average.")
                else:
                    print("Chatbot: Your energy usage on weekdays and weekends is the same on average.")

            # New inputs for the chatbot
            elif user_input == "average_usage":
                print("Chatbot: The average energy usage across all days is {:.2f} kWh.".format(usage_data['usage'].mean()))

            elif user_input == "highest_category_usage":
                max_category, max_usage = max([(category, sum([appliance_data[appliance] for appliance in appliances])) for category, appliances in appliance_categories.items()], key=lambda x: x[1])
                print(f"Chatbot: The appliance category with the highest energy usage is '{max_category}' with {max_usage} kWh.")

            elif user_input == "lowest_category_usage":
                min_category, min_usage = min([(category, sum([appliance_data[appliance] for appliance in appliances])) for category, appliances in appliance_categories.items()], key=lambda x: x[1])
                print(f"Chatbot: The appliance category with the lowest energy usage is '{min_category}' with {min_usage} kWh.")

            elif user_input.startswith("compare_categories"):
                category_names = [name for name in appliance_categories.keys()]
                category1, category2 = None, None

                # Select the first two mentioned categories in user_input
                for name in category_names:
                    if name.lower() in user_input:
                        if category1 is None:
                            category1 = name
                        else:
                            category2 = name
                            break

                if category1 and category2:
                    usage1 = sum([appliance_data[appliance] for appliance in appliance_categories[category1]])
                    usage2 = sum([appliance_data[appliance] for appliance in appliance_categories[category2]])
                    print(f"Chatbot: The energy usage for '{category1}' is {usage1} kWh and for '{category2}' is {usage2} kWh.")
                else:
                    print("Chatbot: Please mention two appliance categories to compare their energy usage.")



            # Add new commands for the chatbot
            elif user_input == "total_energy_usage":
                total_energy = calculate_total_energy_usage(appliance_data)
                print(f"Chatbot: The total energy usage for all appliances is {total_energy} kWh.")

            elif user_input == "category_percentage":
                percentages = calculate_energy_percentage_per_category(appliance_data, appliance_categories)
                response = "Energy usage percentage per category:\n\n"
                for category, percentage in percentages.items():
                    response += f"{category}: {percentage:.2f}%\n"
                print("Chatbot: " + response)

            elif user_input.startswith("compare_appliances"):
                appliances = [appliance for appliance in appliance_data.keys()]
                appliance1, appliance2 = None, None
                for appliance in appliances:
                    if appliance in user_input:
                        if appliance1 is None:
                            appliance1 = appliance
                        else:
                            appliance2 = appliance
                            break
                if appliance1 and appliance2:
                    difference = calculate_energy_difference(appliance1, appliance2, appliance_data)
                    print(f"Chatbot: The energy usage difference between '{appliance1}' and '{appliance2}' is {difference} kWh.")
                else:
                    print("Chatbot: Please mention two appliances to compare their energy usage.")

            elif user_input.startswith("save_bar_chart"):
                file_name = "energy_usage_bar_chart.png"
                save_energy_usage_bar_chart(appliance_data, file_name)

            
            # Add new commands for the chatbot
            elif user_input == "highest_energy_appliance":
                highest_energy_appliance = find_highest_energy_appliance(appliance_data)
                print(f"Chatbot: The appliance with the highest energy usage is '{highest_energy_appliance}' with {appliance_data[highest_energy_appliance]} kWh.")

            elif user_input == "lowest_energy_appliance":
                lowest_energy_appliance = find_lowest_energy_appliance(appliance_data)
                print(f"Chatbot: The appliance with the lowest energy usage is '{lowest_energy_appliance}' with {appliance_data[lowest_energy_appliance]} kWh.")

            elif user_input == "average_energy_usage":
                average_energy = calculate_average_energy_usage(appliance_data)
                print(f"Chatbot: The average energy usage per appliance is {average_energy:.2f} kWh.")

            
            else:
                closest_keyword = find_closest_keyword(user_input)
                if closest_keyword:
                    print(f"Chatbot: It seems like you meant '{closest_keyword}'. Here's the response for that:")
                    print("Chatbot: " + responses[closest_keyword])
                else:
                    response = handle_complex_question(user_input, appliance_data)
                    print("Chatbot: " + response)
        
        except KeyboardInterrupt:
            print("\nChatbot: Goodbye! Have a nice day!")
            break
        except Exception as e:
            print(f"Chatbot: An error occurred: {e}")



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

    # what temperature is it?
    # what day is it?
    # how hot is it?
    
    # day
    # temperature

#NLP
    # What appliances are using the most energy in my home?
        # deprecated
    # What devices/appliances are using the most energy in my home?
        # deprecated


    # How much power is the oven using?
    # How much power is the TV using?
    # How much energy is the refrigerator using?
    # How much energy is the washing machine using?
    # How much energy is the air conditioner using?


    # TV usage?
        #these all can be used
    # energy power usage consumption


    #v22

    # weekday_usage
    # weekend_usage
    # highest_usage_day
    # lowest_usage_day
    # compare_weekday_weekend

    # v23
        # error handling

    #v24 optimization and more inputs

        # average_usage
        # highest_category_usage
        # lowest_category_usage
        # compare_categories

    # v25
        # refrigerator
        # washing machine
        # air conditioner
        # tv
        # oven
        # dishwasher
        # dryer
        # microwave
        # computer
        # water heater

# v27

# total_energy_usage
# category_percentage
# compare_appliances
# save_bar_chart

# ~~~~~~~~~~~~~~~~~~~~~~





# ~~~~~~~~~~~~~~~~~~~~~~
# documentation v28

# Find the appliance with the highest energy usage.
# Find the appliance with the lowest energy usage.
# Calculate the average energy usage per appliance.

# ~~~~~~~~~~~~~~~~~~~~~~
# documentation v27

# added the following functionality to code:

# Calculate the total energy usage.
# Calculate the percentage of energy usage per appliance category.
# Calculate the energy usage difference between two specified appliances.
# Save the energy usage bar chart to a file.


#documentation v22

#This code snippet added the following inputs to my chatbot:

    # "weekday_usage": Provides the average energy usage on weekdays.
    # "weekend_usage": Provides the average energy usage on weekends.
    # "highest_usage_day": Shows the day with the highest energy usage.
    # "lowest_usage_day": Shows the day with the lowest energy usage.
    # "compare_weekday_weekend": Compares energy usage on weekdays and weekends, and provides a summary.




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

    # The machine learning aspect of this code involves using historical energy usage data to train a linear regression model, which can then be used to predict the user's energy usage for the current day.
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
