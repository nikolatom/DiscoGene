
# DiscoGENE

## Overview
DiscoGENE is a Streamlit-based web application designed to retrieve and analyze genetic information from multiple databases, utilizing the Reactome API and OpenAI's GPT-4 model. It allows users to input gene symbols, fetch related genetic information, and receive a comprehensive analysis that includes pathways, diseases, and publications.

## Features
- **Gene Information Retrieval**: Fetch gene-related data from ClinVar, UniProt, and PubMed.
- **Pathway and Disease Insights**: Obtain detailed pathway and disease associations for specific genes.
- **Narrative Analysis**: Generate narrative summaries and pathway tables using OpenAI GPT-4, enhancing understanding of the gene's impact in human biology.
- **Interactive Web Interface**: User-friendly interface powered by Streamlit for easy input and visualization of data.

## Prerequisites
- Python 3.x
- Streamlit
- OpenAI API key

## Installation Instructions

### Setting up the Environment
1. **Clone the Repository**:
   ```bash
   git clone https://https://github.com/nikolatom/DiscoGene.git
   cd DiscoGENE
   ```

2. **Create a Python Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. **Install Required Python Packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
Ensure that your OpenAI API key is correctly configured in the script or through environment variables.

### Running the Application
1. **Launch the Streamlit App**:
   ```bash
   streamlit run disco_gene.py
   ```

## Usage
Start the application, enter a gene symbol into the provided text box, and click the "Analyze" button. The results will include a narrative analysis, a pathways table, and potential diseases linked to the gene.

## Contributing
Contributions are welcome! Please refer to the `CONTRIBUTING.md` for guidelines on how to make contributions.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Support
For support, please open an issue in the GitHub repository.

## Acknowledgements
- Reactome API for gene-related data.
- OpenAI's GPT-4 for generating narrative summaries.
