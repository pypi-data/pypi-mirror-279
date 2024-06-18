from biobox_analytics.data.adapters._base import Adapter
import biobox_analytics.data.adapters.genome._structs as structs
import json
import requests
import os
import gzip
import math
from gtfparse import read_gtf
import urllib.request
from datetime import datetime
import itertools

class ScATAC(Adapter):
    def __init__(self, experimentID, experimentName, cellByPeakPath, celltypes=None, node_filename='node.jsonl.gz', edge_filename='edge.jsonl.gz' ):
        super().__init__()
        self.experiment = structs.SingleCellATACseqExperiment(
            uuid=experimentID,
            displayName=experimentName
        )
        self.node_filename = node_filename
        self.edge_filename = edge_filename

    def _generate_genomic_interval_nodes(self):
        genomicIntervals = []
        for chrom in self.chromosome_regions:
            maxCoord = math.ceil(chrom['length']/1000)
            for i in range(maxCoord):
                start = (i*1000) + 1
                if (i+1)==(maxCoord):
                    end = chrom['length']
                else:
                    end = (i+1)*1000
                genomicIntervals.append({
                    "_id": f"{self.taxon}:{chrom['name']}:{start}-{end}",
                    "labels": ["GenomicInterval"],
                    "properties": {
                        "uuid": f"{self.taxon}:{chrom['name']}:{start}-{end}",
                        "displayName": f"{self.species} {chrom['name']}:{start}-{end}",
                        "taxon": self.taxon,
                        "species": self.species,
                        # "assembly": decoded['assembly_name'],
                        "chr": chrom['name'],
                        "start": start,
                        "end": end,
                    }
                })
                # chromRegion = structs.GenomicInterval(
                #     taxon=self.taxon,
                #     species=self.species,
                #     uuid=f"{self.taxon}:{chrom['name']}:{start}-{end}",
                #     displayName=f"{self.species} {chrom}:{start}-{end}",
                #     chr=chrom['name'],
                #     start=start,
                #     end=end
                # )
                # genomicIntervals.append({
                #   "_id": f"{self.taxon}:{chrom['name']}:{start}-{end}",
                #   "labels": ["GenomicInterval"],
                #   "properties": chromRegion
                # })
        return genomicIntervals
    
    def _generate_gene_nodes(self):
        genes = self._gtf.filter(feature='gene')
        genes_fixed = []
        for g in genes.iter_rows(named=True):
            name = g['gene_name']
            if name == "":
                name = g['gene_id']
            genes_fixed.append({
                "_id": g['gene_id'],
                "labels": ["Gene"],
                "properties": {
                    "uuid": g['gene_id'],
                    "displayName": name,
                    "chr": g['seqname'],
                    "start": g['start'],
                    "end": g['end'],
                    "assembly": self.assembly,
                    "taxon": self.taxon,
                    "strand": g['strand']
                }
            })
        return genes_fixed
    
    def _generate_transcript_nodes(self):
        transcripts = self._gtf.filter(feature='transcript')
        transcripts_fixed = []
        for t in transcripts.iter_rows(named=True):
            name = t['transcript_name']
            if name == "":
                name = t['transcript_id']
            transcripts_fixed.append({
                "_id": t['transcript_id'],
                "labels": ["Transcript"],
                "properties": {
                    "uuid": t['transcript_id'],
                    "displayName": name,
                    "chr": t['seqname'],
                    "start": t['start'],
                    "end": t['end'],
                    "assembly": self.assembly,
                    "taxon": self.taxon,
                    "strand": t['strand']
                }
            })
        return transcripts_fixed
    
    def _generate_protein_nodes(self):
        protein = self._gtf.filter(self._gtf["protein_id"] != "")
        protein_subset = protein.select(['transcript_id', 'protein_id']).unique()
        protein_distinct = []
        for p in protein_subset.iter_rows(named=True):
            protein_distinct.append({
                "_id": p['protein_id'],
                "labels": ["Protein"],
                "properties": {
                    "uuid": p['protein_id'],
                    "displayName": p['protein_id'],
                    "assembly": self.assembly,
                    "taxon": self.taxon,
                }
            })
        return protein_distinct
    
    def iterate_nodes(self, gtf_file_path = "genome.gtf.gz"):
        genome = [
            {
                "_id": self.genome.uuid,
                "labels": ["Genome"],
                "properties": {
                    "_id": self.genome.uuid,
                    "displayName": self.genome.displayName,
                    "assembly": self.genome.assembly,
                    "taxon": self.genome.taxon,
                    "chromosomes": self.chromosome_regions
                }
            }
        ]
        genomic_intervals = self._generate_genomic_interval_nodes()
        # Load gtf file into dataframe before processing genes, transcripts, proteins
        self._gtf = read_gtf(gtf_file_path)
        self._gtfloaded = True
        genes = self._generate_gene_nodes()
        transcripts = self._generate_transcript_nodes()
        proteins = self._generate_protein_nodes()
        allNodes = [genome, genomic_intervals, genes, transcripts, proteins]
        self.nodes = list(itertools.chain(*allNodes))
        return self.nodes
    
    def _generate_genome_to_genomic_interval_edges(self):
        edges = []
        for chrom in self.chromosome_regions:
            maxCoord = math.ceil(chrom['length']/1000)
            for i in range(maxCoord):
                start = (i*1000) + 1
                if (i+1)==(maxCoord):
                    end = chrom['length']
                else:
                    end = (i+1)*1000
                edges.append({
                    "from": {
                        "uuid": self.genome.uuid,
                    },
                    "to": {
                        "uuid": f"{self.taxon}:{chrom['name']}:{start}-{end}",
                    },
                    "label": "genome contains interval"
                })
        return edges
    
    def _generate_genomic_interval_edges(self):
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
                # write the edges to a file
                coordinateEdges.append({
                    "from": {
                        "uuid": f"{self.taxon}:{chrom['name']}:{start1}-{end1}",
                    },
                    "to": {
                        "uuid": f"{self.taxon}:{chrom['name']}:{start2}-{end2}",
                    },
                    "label": "next"
                })
        return coordinateEdges
    
    def _generate_gene_transcript_edges(self):
        transcripts = self._gtf.filter(feature='transcript')
        edges = []
        for t in transcripts.iter_rows(named=True):
            edges.append({
                "from": {
                    "uuid": t["gene_id"],
                },
                "to": {
                    "uuid": t["transcript_id"],
                },
                "label": "transcribed to"
            })
        return edges
    
    def _generate_transcript_protein_edges(self):
        protein = self._gtf.filter(self._gtf["protein_id"] != "")
        protein_subset = protein.select(['transcript_id', 'protein_id']).unique()
        edges = []
        for t in protein_subset.iter_rows(named=True):
            edges.append({
                "from": {
                    "uuid": t["transcript_id"],
                },
                "to": {
                    "uuid": t["protein_id"],
                },
                "label": "has translation"
            })
        return edges

    def iterate_edges(self):
        if self._gtfloaded == False:
            print("Run iterate_nodes() to load in the gtf file, prior to this function being callable")
            return
        gene_genomic_edges = self._generate_genome_to_genomic_interval_edges()
        genomic_coordinate_edges = self._generate_genomic_interval_edges()
        gene_transcript_edges = self._generate_gene_transcript_edges()
        transcript_protein_edges = self._generate_transcript_protein_edges()
        allEdges = [gene_genomic_edges, genomic_coordinate_edges, gene_transcript_edges, transcript_protein_edges]
        self.edges = list(itertools.chain(*allEdges))
        return self.edges

    def process_item(self, item):
        """Processes a single item (node or edge)."""
        # Customize how you want to process each item, e.g., add extra information, filter, etc.
        return item  # In this example, we just return the item as-is.

    def describe_node_properties(self):
        pass

    def describe_edge_properties(self):
        pass
    
    def list_schema(self):
        return None

    def write_serialized_data_to_file(self, directory=""):
        node_filepath = os.path.join(directory, self.node_filename)
        edge_filepath = os.path.join(directory, self.edge_filename)

        with gzip.open(node_filepath, "at") as f:
            for x in self.nodes:
                json.dump(x, f)
                f.write("\n")

        with gzip.open(edge_filepath, "at") as f:
            for x in self.edges:
                json.dump(x, f)
                f.write("\n")
