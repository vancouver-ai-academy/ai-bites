from agentpoirot.tools import func_tools
import pandas as pd

# Load the dataset into a DataFrame
<<<<<<< HEAD
df = pd.read_csv('/mnt/home/projects/research-agent-poirot/web/static/datasets/csm/insights_from_questions_list/poirot/dataset.csv')
=======
df = pd.read_csv('/mnt/home/research-agent-poirot/web/static/datasets/csm/insights_from_questions_list/poirot/dataset.csv')
>>>>>>> 2289d805431ec572755276c7c9765016c0e4b07d

# Data Manipulation
# Create a new column to identify high-impact cases with low or medium priority
df['high_impact_low_medium_priority'] = df.apply(lambda row: 1 if row['impact'] == 'High' and row['priority'] in ['Low', 'Medium'] else 0, axis=1)

# Group by the impact and priority to get counts
df['count'] = 1  # Create a count column for aggregation
df = df.groupby(['impact', 'priority'], as_index=False).agg({'count': 'sum'})  # Aggregate counts

# Plotting
<<<<<<< HEAD
# Create a bar plot to visualize the counts of high-impact cases with low or medium priority
func_tools.plot_bar(df=df, plot_column='priority', count_column='count', plot_title='Counts of High-Impact Cases with Low or Medium Priority')
=======
# Create a pie chart to visualize the proportions of high-impact cases with low or medium priority
func_tools.plot_pie_chart(df=df, plot_column='priority', count_column='count', plot_title='Proportion of High-Impact Cases with Low or Medium Priority')
>>>>>>> 2289d805431ec572755276c7c9765016c0e4b07d
