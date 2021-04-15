import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

### Parameters
list_of_excluded_elements = ["is", "for", "with", "at", "the", "or", "of", "be", "a.", "b.",\
							"c.", "d.", "e.", "to", "up", "and", "was", "from", "if", "other",\
							 "an", "in", "on", "no", "na", "not", "yn", "11", "a.age", "please",\
							 "15", "can", "yes", "r"]
threshold_plot = 49 # number of occurence considered for the plot

### Read the excel file containing the common data elements
colName = ["Name of the ERN", "Name of the grouping item", "Name of the Data Element", "Explanatory description",\
			"Data type or list of permitted values", "Example value", "Comments"]
data = pd.read_excel("DCDE_Candidates_Template V2.xlsx", sheet_name = "Data Dictionary (stewards)",\
					 usecols = colName, skiprows = 5).dropna(how = "all").reset_index()

### Special case of the ERRBone & EuRReca registries
listRows = ["ADRENAL", "CALCIUM & PHOSPHATE", "GLUCOSE & INSULIN", "GENETIC ENDOCRINE TUMOURS",\
			"GROWTH & OBESITY", "PITUITARY", "SEX DEVELOPMENT", "THYROID", "BONE DYSPLASIA"]
indices = data[data["Name of the grouping item"].isin(listRows)].index
data.loc[indices, "Name of the Data Element"] = data.loc[indices, "Explanatory description"]

# Transform data elements to be able to match them
data["Name of the Data Element copy"] = data["Name of the Data Element"].str.\
									lower().str.replace("_", " ").str.\
									replace("\t", "").str.replace("?","").\
									str.replace(":"," ").str.replace("(","").\
									str.replace(")","")

### Count all individual words disregarding of the context, registry
individual_words = data["Name of the Data Element copy"].str.split().apply(pd.Series).\
		merge(data, right_index = True, left_index = True).drop(["Explanatory description",\
		"Data type or list of permitted values", "Example value", "Comments", "index"], axis = 1).\
		melt(id_vars = ['Name of the ERN', 'Name of the grouping item', 'Name of the Data Element'],\
			value_vars = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], value_name = "data_element").\
		drop("variable", axis = 1).dropna()
# individual_words.to_csv("test.csv")
frequency_ind = individual_words["data_element"].value_counts()

### Create a dataframe that contains all the match between the different ERN
# Create empty dataframe to contain the data
colList = ["element", "nb occurence", "name of data element",\
		 	"name of the grouping item", "name of registry", "explanatory description",\
		 	"list of permitted values"]
commonElements = pd.DataFrame(columns = colList)

list_individual_elements = list(set(individual_words["data_element"].values))

# extract frequency distribution 
freq_distribution = []

for j in range(0, len(list_individual_elements)):

	if (list_individual_elements[j] not in list_of_excluded_elements) &\
		(len(list_individual_elements[j]) > 1): # to exclude words that we know are wrong

		numberElements = data.index[data['Name of the Data Element copy'].str.contains(list_individual_elements[j]) == True]
		freq_distribution.append(len(numberElements))
		# Create the new rows to append to the final dataframe
		new_rows = pd.DataFrame(data = {"element": np.repeat(list_individual_elements[j], len(numberElements)),\
					"nb occurence": np.repeat(len(numberElements), len(numberElements)),\
					"name of data element": data.loc[numberElements, "Name of the Data Element"].values,\
					"name of the grouping item": data.loc[numberElements, "Name of the grouping item"].values,\
					"name of registry": data.loc[numberElements, "Name of the ERN"].values,\
					"explanatory description": data.loc[numberElements, "Explanatory description"].values,\
					"list of permitted values": data.loc[numberElements, "Data type or list of permitted values"].values})
		# Add the new rows tot the final dataframe
		commonElements = commonElements.append(new_rows, ignore_index = True)

# Export as a CSV document		
commonElements.to_csv("List_Common_Data_Elements_CLC.csv", sep = ";", index = False)

# Count the frequency distribution of each individual element
freq_distribution = pd.DataFrame(freq_distribution).value_counts(sort = True)
freq_distribution.to_csv("Frequency_distribution_ind_elements_CLC.csv", sep = ";")

### Make a frequency plot
element_frequency = commonElements[["element" , "nb occurence"]].drop_duplicates()

fig = plt.figure(figsize = (10,6))
gs = GridSpec(2, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])

ax1.hist(element_frequency["nb occurence"].values, bins = 500)
ax1.set_xlim([0, 70])
ax1.set_xlabel("Nb of occurrence [-]")
ax1.set_ylabel("Count [-]")

ax2.bar(np.arange(len(element_frequency["nb occurence"].values)), np.sort(element_frequency["nb occurence"].values), width = 0.5)
ax2.set_xticks([])
ax2.set_xticklabels([], rotation = 90)
ax2.set_ylim([0, 200])
ax2.set_xlabel("Ind. data element [-]")
ax2.set_ylabel("Count [-]")

ax3.bar(np.arange(len(element_frequency.loc[element_frequency["nb occurence"] > threshold_plot, "nb occurence"])), element_frequency.loc[element_frequency["nb occurence"] > threshold_plot, "nb occurence"].values, width = 0.5)
ax3.set_xticks(np.arange(len(element_frequency.loc[element_frequency["nb occurence"] > threshold_plot, "nb occurence"])))
ax3.set_xticklabels(element_frequency.loc[element_frequency["nb occurence"] > threshold_plot, "element"].values, rotation = 90)
ax3.set_ylabel("Count [-]")

plt.subplots_adjust(bottom=0.2, hspace = 0.25)
plt.savefig("Distribution_Data_Elements_CLC.pdf", format = "pdf", dpi = 300)
plt.show()
