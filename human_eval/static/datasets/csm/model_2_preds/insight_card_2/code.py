from agentpoirot.tools import func_tools
import pandas as pd

# Load the dataset into a DataFrame
df = pd.read_csv('/mnt/home/projects/research-agent-poirot/web/static/datasets/csm/insights_from_questions_list/poirot/dataset.csv')

<<<<<<< HEAD
# Stage 1: Data Manipulation
# Create a new column to identify SLA breaches for high-priority cases
df['sla_breach'] = (df['made_sla'] == 0) & (df['priority'] == 'High')

# Create a new column to count total high-priority cases
df['total_high_priority'] = df['priority'].apply(lambda x: 1 if x == 'High' else 0)

# Stage 2: Plotting
# Use the pie chart function to visualize the percentage of high-priority cases that breached their SLA
func_tools.plot_pie_chart(df=df, plot_column='sla_breach', count_column='total_high_priority', plot_title='Percentage of High-Priority Cases Breaching SLA')
=======
# Data Manipulation
# Create a new column to identify SLA breaches for high-priority cases
df['sla_breach'] = (df['made_sla'] == 0) & (df['priority'] == 'High')

# Calculate the percentage of high-priority cases that breached their SLA
df['high_priority_count'] = df['priority'].apply(lambda x: 1 if x == 'High' else 0)
df['sla_breach_percentage'] = df['sla_breach'].sum() / df['high_priority_count'].sum() * 100

# Plotting
# Use a pie chart to visualize the percentage of SLA breaches among high-priority cases
func_tools.plot_pie_chart(df=df, plot_column='sla_breach', count_column='high_priority_count', plot_title='Percentage of High-Priority Cases Breaching SLA')
>>>>>>> 2289d805431ec572755276c7c9765016c0e4b07d
