import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


# st.markdown("""
#
# # Title
# ## Subtitle
#
# - bullet 1
# - bullet 2
# - bullet 3
#
# > Amazing Quote
#
# """)
#
# st.radio("Which dessert is best?", ["Cake", "Ice Cream", "Pie"])

df = sns.load_dataset("penguins") #load dataset

fig, ax = plt.subplots() # Create a new figure, get the axes object
sns.scatterplot(data=df, x="flipper_length_mm", y="bill_length_mm", hue="species",
                ax=ax) #Use the axes object to plot on the same figure

st.pyplot(fig) #show the figure in Streamlit




