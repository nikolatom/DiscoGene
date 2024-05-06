import time

import reactome2py.content as content
import requests
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="<your openAI API key")


def fetch_clinvar_data(gene_symbol):
    clinvar_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term={gene_symbol}[gene]+AND+single_gene[prop]&retmax=500&retmode=json"
    response = requests.get(clinvar_url)
    if response.status_code == 200:
        return response.json()
    else:
        return "Error fetching data from ClinVar."


def get_pathways(gene_symbol):
    """Retrieve pathways associated with a gene symbol."""
    pathways = content.entities_complexes(id=gene_symbol, resource="UniProt")
    st.json(pathways, expanded=False)  # Debug output
    return pathways


def get_diseases(gene_symbol):
    """Retrieve diseases associated with a gene symbol."""
    diseases = content.disease(doid=True)  # Assuming DOIDs are required
    return diseases


def get_publications(gene_symbol):
    """Retrieve publications associated with a gene symbol."""
    publications = content.query_id(id=gene_symbol, enhanced=True)
    return publications


def gene_symbol_to_uniprot(gene_symbol):
    """Convert gene symbol to UniProt ID using UniProt API."""
    # Correctly encoding the query string
    query = f'gene_exact:"{gene_symbol}" AND reviewed:true AND organism_id:9606'
    url = f"https://rest.uniprot.org/uniprotkb/search?query={query}&format=tsv&fields=accession"
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.splitlines()
        if len(lines) > 1:  # First line is headers, subsequent lines are data
            # Return the first UniProt ID from the response
            return lines[1].split("\t")[0]
    else:
        print("Failed to fetch or parse the response:", response.text)
    return None


def test_reactome_queries(uniprot_id):
    """Test Reactome data retrieval."""
    pathways = get_pathways(uniprot_id)
    diseases = get_diseases(uniprot_id)
    publications = get_publications(uniprot_id)

    return {"pathways": pathways, "diseases": diseases, "publications": publications}


def analyze_gene(gene_symbol):
    """Fetches data related to the gene symbol and returns structured information."""
    protein_id = gene_symbol_to_uniprot(gene_symbol)
    st.write(f"Converted UniProt ID: {protein_id}")  # Debug output

    if protein_id:
        pathways = get_pathways(protein_id)
        diseases = get_diseases(protein_id)
        publications = get_publications(protein_id)
        result = {
            "pathways": pathways,
            "diseases": diseases,
            "publications": publications,
        }
        return result
    else:
        st.write(
            "Conversion to UniProt ID failed or returned no results."
        )  # Debug output
        return None


def fetch_publications(gene_symbol):
    """Fetch publications from PubMed."""
    pubmed_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={gene_symbol}[gene]&retmode=json"
    response = requests.get(pubmed_url)
    if response.status_code == 200:
        return response.json()
    else:
        return "Error fetching publication data."


def generate_narrative_analysis(gene_symbol, gene_data):
    """Generate narrative analysis using OpenAI GPT-4."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Provide an analysis for the gene symbol '{gene_symbol}' that includes its associated pathways, diseases, and any relevant publications. Highlight the significance of these pathways in human biology and disease, and mention any notable findings from the publications.",
        },
    ]
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        stream=True,
    )
    narrative_summary = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            narrative_summary += chunk.choices[0].delta.content
    return narrative_summary.strip()


def generate_pathways_table(gene_symbol, gene_data):
    """Generate table of pathways using OpenAI GPT-4."""
    pathways_content = "\n".join(
        [
            f"- {pathway['displayName']} (ID: {pathway['stId']})"
            for pathway in gene_data["pathways"]
        ]
    )
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Based on the pathways information provided for '{gene_symbol}', create a table summarizing the pathways. Include the pathway name, ID, and its role in human biology and disease:\n{pathways_content}",
        },
    ]
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        stream=True,
    )
    table_summary = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            table_summary += chunk.choices[0].delta.content
    return table_summary.strip()

    # # Add diseases information
    # diseases_content = "Diseases:\n" + "\n".join(
    #     [
    #         f"- {disease['name']} (ID: {disease['id']})"
    #         for disease in gene_data["diseases"]
    #     ]
    # )
    # messages.append({"role": "user", "content": diseases_content})

    # # Add publications information
    # publications_content = "Publications:\n" + "\n".join(
    #     [
    #         f"- {publication['title']} (ID: {publication['id']})"
    #         for publication in gene_data["publications"]
    #     ]
    # )
    # messages.append({"role": "user", "content": publications_content})

    # Collect the response


def main():
    # Streamlit user interface setup
    st.title("DiscoGENE - Genetic Variant and Pathway Analyzer")
    with st.expander("Get information about a gene symbol"):
        gene_symbol = st.text_input("Enter Genetic Symbol", "BRCA1")

        if st.button("Analyze"):
            st.write("Fetching data...")
            gene_data = analyze_gene(
                gene_symbol
            )  # Ensure this function returns the expected data structure

            if gene_data:
                narrative_summary = generate_narrative_analysis(gene_symbol, gene_data)
                table_summary = generate_pathways_table(gene_symbol, gene_data)
                combined_summary = narrative_summary + "\n\n" + table_summary

                def stream_combined_summary():
                    for part in combined_summary.split(" "):
                        yield part + " "
                        time.sleep(0.02)  # Simulate delay

                st.write_stream(stream_combined_summary)

            else:
                st.error("Error fetching data or no data available.")


if __name__ == "__main__":
    main()