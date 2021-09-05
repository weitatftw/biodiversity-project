from matplotlib import pyplot as plt
import pandas as pd


species = pd.read_csv('species_info.csv')
print(species.head())


species_type = species.category.unique()
conservation_statuses = species.conservation_status.unique()
conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()
species.fillna('No Intervention', inplace=True)
conservation_counts_fixed = species.groupby('conservation_status').scientific_name.nunique().reset_index()
protection_counts = species.groupby('conservation_status')    .scientific_name.nunique().reset_index()    .sort_values(by='scientific_name')


plt.figure(figsize=(10,4))
ax = plt.subplot()
plt.bar(range(0,5), height=protection_counts.scientific_name)
ax.set_xticks(range(0, 5))
ax.set_xticklabels(protection_counts.conservation_status)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.show()
plt.savefig('Conservation Status by Species.png')


protected = lambda x: True if x != 'No Intervention' else False
species['is_protected'] = species.conservation_status.apply(protected)


category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()
print(category_counts.head())
category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()
print(category_pivot)
category_pivot.columns = ['category', 'not_protected', 'protected']
category_pivot['percent_protected'] = (category_pivot.protected) / (category_pivot.protected + category_pivot.not_protected)
print(category_pivot)


contingency = [[30, 146], [75, 413]]
from scipy.stats import chi2_contingency


chi2, pval, freq, dof = chi2_contingency(contingency)
contingency2 = [[30, 146], [5, 73]]
chi22, pval_reptile_mammal, freq2, dof2 = chi2_contingency(contingency2)


observations = pd.read_csv('observations.csv')
print(observations.head())


sheepornot = lambda x: True if 'Sheep' in x else False
species['is_sheep'] = species.common_names.apply(sheepornot)
species_is_sheep = species[species['is_sheep'] == True]
print(species_is_sheep)
sheep_species = species[(species['is_sheep'] == True) & (species['category'] == 'Mammal')]
sheep_observations = sheep_species.merge(observations)
obs_by_park = sheep_observations.groupby(sheep_observations.park_name).observations.sum().reset_index()


plt.figure(figsize=(16,4))
ax = plt.subplot()
plt.bar(range(0,4), height=obs_by_park.observations)
ax.set_xticks(range(0,4))
ax.set_xticklabels(['Bryce National Park', 'Great Smoky Mountains National Park', 'Yellowstone National Park', 'Yosemite National Park'])
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.show()
plt.savefig('observations of sheep per week.png')


minimum_detectable_effect = 100*5/15
sample_size_per_variant = 870
yellowstone_weeks_observing = sample_size_per_variant/507
bryce_weeks_observing = sample_size_per_variant/250
