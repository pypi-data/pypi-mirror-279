from PA_WorkFlow import PA_KG
from LLM_Summ import LLM_Summ



subjectType = 'breast cancer'
openAIKey = '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'

kg_Work = PA_KG(pathGene='../../tests/geneExpression_data.txt',
                 pathGroup='../../tests/group_data.txt',
                 subject=subjectType)

#retrieves the exp_id used inside database to save subgraph
exp_id = kg_Work.expID_retrieve()
print(exp_id)

# conducts pathwayAnalysis workflow using netGSA in R
kg_Work.pathwayAnalysis()

# writes netGSA results into graph database, conducts WCC analysis
kg_Work.kgSubgraph()

# retrieves knowledge graph data from graph database
retrievedDocuments = kg_Work.retrieval()

# feeds retrieved documents to LLM by creating a LLM object instance
allSumm = LLM_Summ(retrievedDocuments, subjectType)

# connects ChatGPT OpenAI using key
allSumm.llm_connect(key=openAIKey)

# generates summaries, if component is too large uses ontology and interactions to group data into clusters.
# if to_write option is enabled then the data output is written to files in current working directory
rankedSummaries = allSumm.generateSumm(to_write=True)

print(rankedSummaries)