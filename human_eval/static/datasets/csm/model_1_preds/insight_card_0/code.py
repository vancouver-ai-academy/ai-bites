from agentpoirot.tools import func_tools
import pandas as pd

<<<<<<< HEAD
# Load the dataset
df = pd.read_csv('/mnt/home/projects/research-agent-poirot/web/static/datasets/csm/insights_from_questions_list/poirot/dataset.csv')
=======
# Load the dataset into a DataFrame
df = pd.read_csv('/mnt/home/research-agent-poirot/web/static/datasets/csm/insights_from_questions_list/poirot/dataset.csv')
>>>>>>> 2289d805431ec572755276c7c9765016c0e4b07d

# Stage 1: Data Manipulation
# Calculate the average resolution duration
df['average_resolution_duration'] = df['u_rpt_case_resolve_duration'].mean()

# Create a new column to flag cases where resolution time exceeds 3x the average
df['exceeds_3x_average'] = df['u_rpt_case_resolve_duration'] > (3 * df['average_resolution_duration'])

# Stage 2: Plotting
# Plot the distribution of cases that exceed 3x the average resolution time
func_tools.plot_bar(df=df, plot_column='exceeds_3x_average', count_column='u_rpt_case_resolve_duration', plot_title='Cases Exceeding 3x Average Resolution Time')