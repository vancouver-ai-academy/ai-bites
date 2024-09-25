from agentpoirot.tools import func_tools
import pandas as pd

# Load the dataset into a DataFrame
df = pd.read_csv('/mnt/home/projects/research-agent-poirot/web/static/datasets/csm/insights_from_questions_list/poirot/dataset.csv')

# Stage Name: Data Manipulation
# Create a new column to count the number of reassignments for each assignment group
df['reassignment_count'] = df['reassignment_count'].astype(float)  # Ensure the column is numeric for aggregation
# Group by assignment group and sum the reassignments
df = df.groupby('assignment_group', as_index=False).agg({'reassignment_count': 'sum'})
# Filter to find assignment groups with more than 3 reassignments
df = df[df['reassignment_count'] > 3]

# Stage Name: Plotting
<<<<<<< HEAD
# Create a bar plot to visualize the assignment groups with more than 3 reassignments
func_tools.plot_bar(df=df, plot_column='assignment_group', count_column='reassignment_count', plot_title='Assignment Groups with More than 3 Reassignments')
=======
# Use the plot function to visualize the assignment groups with more than 3 reassignments
func_tools.plot_boxplot(df=df, x_column='assignment_group', y_column='reassignment_count', plot_title='Reassignments by Assignment Group')
>>>>>>> 2289d805431ec572755276c7c9765016c0e4b07d
