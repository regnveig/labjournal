from lib.blister import *

Blister.Logo("Andre's Beasts")

tracking = pd.read_csv("/dev/datasets/FairWind/_results/Andre/cuffdiff_4gr/genes.read_group_tracking", sep='\t')
samples = pd.read_csv("/dev/datasets/FairWind/_results/Andre/cuffdiff_4gr/read_groups.info", sep='\t')
samples.rename(columns={'replicate_num' : 'replicate'}, inplace=True)
samples.drop(columns=['total_mass', 'norm_mass', 'internal_scale', 'external_scale'], inplace=True, axis=1)
tracking = pd.merge(samples, tracking, on=['replicate', 'condition'], how='right')

#lst = ['XLOC_013547', 'XLOC_020821', 'XLOC_005197']

#tracking = tracking[tracking['tracking_id'].isin(lst)]
tracking.drop(columns=['raw_frags', 'internal_scaled_frags', 'external_scaled_frags', 'effective_length', 'status'], inplace=True, axis=1)
tracking.sort_values(by=['tracking_id', 'condition', 'replicate'], ascending=True, inplace=True)
cols = tracking.columns
tracking = tracking.groupby('tracking_id').apply(pd.Series.to_list).apply(pd.DataFrame, columns=cols).apply(pd.DataFrame.drop, columns=['condition', 'replicate', 'tracking_id'], axis=1).to_dict()

table = 1

for it in tracking.keys():
	tracking[it] = tracking[it].rename(columns={'FPKM' : it})
	if type(table) == type(pd.DataFrame()): table = pd.merge(tracking[it], table, on=['file'], how='right')
	else: 
		table = tracking[it]

table['file'] = table['file'].apply(lambda x: x[7:9])

table = table.transpose()
table.columns = ['01[SD-DAY]', '02[SD-DAY]', '03[SD-DAY]', '04[SD-NIGHT]', '05[SD-NIGHT]', '06[SD-NIGHT]', '07[L27-DAY]', '09[L27-DAY]', '08[L27-NIGHT]', '10[L27-NIGHT]', '11[L27-NIGHT]', '12[L27-NIGHT]']
table.drop(labels='file', axis=0, inplace=True)
#print(Blister.GitHubTable(table, index=True))
print(table)
table.to_csv("/dev/datasets/FairWind/_results/Andre/every_beast.csv", sep=',', index=True)
