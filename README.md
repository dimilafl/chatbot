# chatbot
enterprise ML chatbot for work


~~~~~~~~~~~
Description
~~~~~~~~~~~
-needs update

    The machine learning aspect of this code involves using historical energy usage data to train a linear regression model, which can then be used to predict the user's energy usage for the current day.

    The code loads the historical energy usage data from a CSV file and uses the scikit-learn library to fit a linear regression model to the data. The input to the model is the day of the week (represented as an integer between 0 and 6), and the output is the energy usage for that day.

    Once the model is trained, the chatbot can use it to provide personalized responses based on the user's energy usage. For example, the usage response uses the model to predict the user's energy usage for the current day, based on the day of the week. The history response provides a summary of the user's energy usage for the past week, based on the historical data that was used to train the model.

    Overall, the machine learning aspect of this code allows the chatbot to provide more personalized and accurate responses based on the user's energy usage patterns, which can help the user better understand their energy usage and identify areas where they can save energy and reduce costs.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Version History
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


~~ v10 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Used the matplotlib library to create visualizations

With these changes, users can now type 'chart' to visualize their energy usage over time and 'heatmap' to see 
which times of the day they tend to use the most energy.

~~ v16 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
natural language processing, added compound words

~~ v18 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
data viz, new additions pie and bar charts - would like to add more

~~ v21 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The find_closest_keyword() function calculates the Levenshtein distance between the user input and the predefined response keywords. If the minimum distance is less than or equal to 2 (indicating a small typo or a similar word), it returns the closest keyword. If the minimum distance is greater than 2, it returns None.

In the main() function, if the user input is not found in the responses dictionary, the code checks for the closest keyword using the find_closest_keyword() function. If there's a close match, the chatbot prints the response for the closest keyword. If there's no close match, it proceeds with the existing logic for handling complex questions.

    ~~~ for example ~~~
    You: hellp
    Chatbot: It seems like you meant 'help'. Here's the response for that:
    Chatbot: Sure, here are some things you can do to monitor your energy usage:

    - Use a smart thermostat to control your heating and cooling
    -....etc

    You: hiii
    Chatbot: It seems like you meant 'hi'. Here's the response for that:
    Chatbot: Hello! How can I help you monitor your energy usage today?


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Summary-
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This code is a chatbot that helps users monitor their energy usage. It has several features, including answering questions, providing tips, and visualizing energy usage data. The chatbot uses a linear regression model to predict daily energy usage, and provides energy-saving tips based on the predicted usage. It can also create a line chart of energy usage over time and a heatmap of energy usage by the time of day. Additionally, the chatbot uses the Spacy library for natural language processing to answer more complex questions about energy usage by appliances.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Summary of the code:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Import necessary libraries and load the Spacy model.
Define the handle_complex_question() function for handling appliance-related questions.
Provide sample data for energy usage by appliances.
Load the historical energy usage data and handle file-related exceptions.
Fit a linear regression model to the data.
Define energy-saving tips based on energy usage levels.
Define the chatbot's responses.
Define the chatbot's main loop, which includes handling complex questions and visualizations.
Define functions to plot energy usage over time and create a heatmap.
Run the chatbot.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Summary of the code: - 3.20 10.57am
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This code is a simple energy usage monitoring chatbot that helps users track their energy consumption and provides tips for saving energy. It utilizes machine learning to predict daily energy usage based on historical data. 


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Summary of the code (machine learning): - 3.20 10.57am
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~
Here's a summary of the machine learning aspect of this code:
~~~~~~~~~~~~~~~~~~~~~~~~

The code imports necessary libraries such as pandas, scikit-learn's LinearRegression, and matplotlib for data manipulation, model training, and visualization, respectively.

It reads the historical energy usage data from a CSV file and checks for errors.

The code uses a linear regression model from scikit-learn to fit the historical energy usage data.

It predicts the energy usage for the current day based on the day of the week, temperature, and whether it is a weekend.

Depending on the predicted energy usage, the chatbot provides appropriate energy-saving tips to the use