from biobox_analytics.data.adapters._base import Adapter
import _structs as structs
import rdflib
import json
import requests
import math


class GenomeAdapter(Adapter):
    def __init__(self, species, target: structs.Genome ):
        super().__init__()
        self.species = species
        self.assembly = None
        self.__get_taxonid()
        self.__get_ensembl_assembly_info()

    def __get_taxonid(self):
        species = self.species
        # curl request the species name here: curl "https://www.ebi.ac.uk/ena/taxonomy/rest/scientific-name/Leptonycteris%20nivalis"
        url = "https://www.ebi.ac.uk/ena/taxonomy/rest/scientific-name/" + species.replace(" ","%20")
        r = requests.get(url)
        r.json()
        if len(r.json()) == 1:
            self.taxon = int(r.json()[0]['taxId'])

    def __get_ensembl_assembly_info(self):
        species = self.species
        server = "https://rest.ensembl.org"
        ext = "/info/assembly/" + species.replace(" ","_")  + "?"
         
        r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
         
        if not r.ok:
          r.raise_for_status()
          sys.exit()
         
        decoded = r.json()
        self.assembly = decoded['assembly_name']
        self.karyotypes = decoded['karyotype']
        chromosomes = []
        for chrom in decoded['top_level_region']:
            if (chrom['coord_system'] == "chromosome"):
                chromosomes.append(chrom)
        self.chromosome_regions = chromosomes
                
    def pull_data(self):
        pass

    def iterate_nodes(self):
        # Generate genomic coordinate nodes
        chromosomeRegions = []
        for chrom in self.chromosome_regions:
            maxCoord = math.ceil(chrom['length']/1000)
            for i in range(maxCoord):
                start = (i*1000) + 1
                if (i+1)==(maxCoord):
                    end = chrom['length']
                else:
                    end = (i+1)*1000
                chromosomeRegions.append({
                    "uuid": f"{self.taxon}:{chrom['name']}:{start}-{end}",
                    "displayName": f"{self.species} {chrom}:{start}-{end}"
                    "taxon": self.taxon,
                    "species": self.species,
                    # "assembly": decoded['assembly_name'],
                    "chr": chrom['name'],
                    "start": start,
                    "end": end,
                })
            # write chromosome regions to jsonl file
            
        pass

    def iterate_edges(self):
        # Generate edges between adjacent genomic coordinates
        coordinateEdges = []
        for chrom in self.chromosome_regions:
            maxCoord = math.ceil(chrom['length']/1000)
            # One fewer edge than num nodes
            for i in range(maxCoord-1):
                # current node
                start1 = (i*1000) + 1
                end1 = (i+1)*1000
                start2 = end1 + 1
                if (i+2)==(maxCoord):
                    end2 = chrom['length']
                else:
                    end2 = (i+2)*1000
                # next node
                
                coordinateEdges.append({
                    "uuid": f"9606:{chrom['name']}:{start}-{end}",
                    "taxon": 9606,
                    # "species": "homo sapiens",
                    # "assembly": decoded['assembly_name'],
                    "chrom": chrom['name'],
                    "start": start,
                    "end": end
                })
        pass

    def process_item(self, item):
        """Processes a single item (node or edge)."""
        # Customize how you want to process each item, e.g., add extra information, filter, etc.
        return item  # In this example, we just return the item as-is.

    def describe_node_properties(self):
        pass

    def describe_edge_properties(self):
        pass
