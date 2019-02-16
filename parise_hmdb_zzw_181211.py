import xml.etree.cElementTree as ET #permits xml parsing trees
import sys
import pandas as pd

# tree = ET.parse('hmdb_metabolites_20180609.xml')
tree = ET.parse('sweat_metabolites.xml')
t_root = tree.getroot()

ns = {'hmdb': 'http://www.hmdb.ca'}
needed_items = ['accession', 'update_date', 'name', 'chemical_formula', 'monisotopic_molecular_weight', 'cas_registry_number', 'smiles', 'inchi',
               'inchikey', 'pubchem_compound_id', 'kegg_id']
taxonomys = ['kingdom', 'super_class', 'class', 'sub_class', 'molecular_framework']

for met in t_root.findall('hmdb:metabolite', namespaces=ns):
    # print(met)
    result = []
    taxonomy_res = []
    for item in needed_items:
        
        curr_node = met.find('hmdb:{}'.format(item), namespaces=ns)
        # print(curr_node)
        if curr_node!=None and curr_node.text:
            result.append(curr_node.text)
        else:
            result.append('NA')
    taxonomy_node = met.find('hmdb:taxonomy', ns)
    for tax in taxonomys:
        curr_node = taxonomy_node.find('hmdb:{}'.format(tax), ns)
        if curr_node!=None and curr_node.text:
            taxonomy_res.append(curr_node.text)
        else:
            taxonomy_res.append('NA')
    output_str = '\t'.join(result+taxonomy_res)
    # print(output_str)
    with open('parsed_hmdb_xml_20181211_ZZW.txt', 'a') as f:
        f.write(output_str + '\n')

all_hmdb = pd.read_csv('parsed_hmdb_xml_20181211_ZZW.txt', sep='\t', header=None, dtype={7:object})
all_hmdb.head()

cols = ['hmdb_acc', 'update_date', 'chemical_formula', 'name', 'monisotopic_molecular_weight', 'cas_registry_number', 'smiles', 'inchi',
               'inchikey', 'pubchem_compound_id', 'kegg_id', 'kingdom', 'super_class', 'class', 'sub_class', 'molecular_framework']

all_hmdb.columns = cols
all_hmdb.head()

all_hmdb.to_csv('parsed_hmdb_xml_20180609_ZZW_test.csv', index=False)
