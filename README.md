# Python Projects 

This repository contains several Python projects that showcase the utilization of various APIs for data analysis and visualization. These projects provide insights into a variety of fields such as music preference analysis, sleep trend evaluation, and nutrition analysis. Each project is developed with Python and employs various libraries for data fetching, processing, and visualization. 

## Project Descriptions

### **Spotify Music Analysis**
In this project, Python was used to interface with the Spotify API and fetch data from the 'Liked Songs' playlist. The analysis was performed to determine top artists based on danceability and top songs based on acousticness. Additionally, the genre distribution across the tracks was analyzed. The script successfully fetches song and artist details, collects and processes audio features, and finally visualizes these metrics in a series of plots. This analysis provides a comprehensive view of music preferences based on track properties like danceability, energy, tempo, and duration.

### **Oura Ring's Sleep Trend Analysis**
This project involved analyzing Oura Ring's sleep trend data using Python to investigate the relationship between daily activity levels, sleep efficiency, and readiness scores. Various data visualization techniques were employed to present key findings and insights. The project aimed to test hypotheses regarding correlations between daily movement and sleep efficiency, as well as sleep efficiency and readiness scores. An interactive Streamlit app was created to simplify data presentation and enhance accessibility, providing insights into how sleep quality can impact overall well-being and daily preparedness.

### **Food Protein Content Analysis**
In this project, the FoodData Central API provided by the U.S. Department of Agriculture (USDA) was leveraged to fetch and analyze the average protein content in various types of foods across different categories such as meats, dairy, legumes, nuts & seeds, whole grains, and others. The script fetches data for each type of food within these categories and calculates the average protein content per 100g serving size. The results are then displayed in the console as well as through a comprehensive table and a visual bar chart using Streamlit and Plotly. This project can serve as a valuable tool for nutritionists, dietitians, or anyone interested in comparing the protein content of different foods. To use the script, a Python environment should be set up, required libraries installed (requests, pandas, streamlit, plotly), and the script should be run using Streamlit.

All scripts include comprehensive comments to guide the user through the code, ensuring understanding of the underlying logic. **Note: users need to replace "xxx" with their own APIs keys.**

## Future Scope
These projects are examples of how public APIs can be used to gather and analyze data in various contexts, such as meal planning, health and fitness apps, academic research, and more. The data visualized in these projects aids in better decision-making in respective fields, indicating the potential application of such scripts in practical scenarios.
