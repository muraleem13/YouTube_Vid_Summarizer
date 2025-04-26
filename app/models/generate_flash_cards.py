from app.config.gemini_ai_config import configure_genai
import google.generativeai as genai
from dotenv import load_dotenv
from app.logger.logger import logger
import json
logger = logger(__name__)

def generate_flashcards(summary_text, max_cards=10, complexity="mixed"):
    """
    Generate flashcards based on the provided summary text using Google Gemini AI.
    Args: Summary text (str): The summary text to generate flashcards from.
          max_cards (int): The maximum number of flashcards to generate. Default is 10.
          complexity (str): The complexity level for the flashcards. Options are "undergraduate", "graduate", or "mixed". Default is "mixed".
    Returns: list: A list of flashcards generated from the summary text.      
          """
    try:
        if not configure_genai():
            logger.error("Gemini AI API key is not set in the environment variables.")
            return None
        
        logger.info("Gemini AI API key is set in the environment variables.")
        logger.info("Gemini AI model initialized successfully.")
        
        model = genai.GenerativeModel(model_name='gemini-2.0-flash')
        
        complexity_instruction = ""
        if complexity == "undergraduate":
            complexity_instruction = "Create flashcards appropriate for undergraduate students, focusing on foundational terms and straightforward definitions that demonstrate core concepts in the field."
        elif complexity == "graduate":
            complexity_instruction = "Create flashcards appropriate for graduate students, focusing on advanced terminology, specialized concepts, nuanced definitions, and theoretical frameworks that would be relevant to advanced study or research."
        else: 
            complexity_instruction = "Create a mix of flashcards with varying academic levels: 60% at undergraduate level (core concepts) and 40% at graduate level (specialized terminology and advanced theoretical concepts)."
        
        prompt = f"""Based on the following summary, create flashcards ONLY for definitions/terms found in the content.
Do NOT create flashcards if no clear definitions exist in the text.
Create up to {max_cards} flashcards, but ONLY include actual definitions from the text.

{complexity_instruction}

Here are examples of flashcards at different academic levels:

UNDERGRADUATE LEVEL EXAMPLE:
Summary: Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, but since the 1800s, human activities have been the main driver of climate change, primarily due to the burning of fossil fuels like coal, oil, and gas, which produces heat-trapping gases. The primary greenhouse gases include carbon dioxide, methane, nitrous oxide, and fluorinated gases. Global warming is causing polar ice sheets and glaciers to melt, raising sea levels and threatening coastal communities. Climate models project that without significant mitigation efforts, global temperatures could rise by 2.7°F to 8.6°F by 2100, with catastrophic consequences including extreme weather events, biodiversity loss, food insecurity, and economic damage. The Paris Agreement, adopted in 2015, aims to limit global warming to well below 2°C, preferably 1.5°C, compared to pre-industrial levels through nationally determined contributions to greenhouse gas reductions.

Flashcards:
[
  {{
    "front": "Climate change",
    "back": "Long-term shifts in temperatures and weather patterns, primarily driven by human activities since the 1800s, especially the burning of fossil fuels.",
    "category": "Environmental Science"
  }},
  {{
    "front": "Greenhouse gases",
    "back": "Heat-trapping gases that contribute to climate change, including carbon dioxide, methane, nitrous oxide, and fluorinated gases.",
    "category": "Atmospheric Chemistry"
  }},
  {{
    "front": "Global warming",
    "back": "The increase in Earth's average temperature that causes polar ice sheets and glaciers to melt, raising sea levels and threatening coastal communities.",
    "category": "Climate Effects"
  }},
  {{
    "front": "Paris Agreement",
    "back": "An international climate accord adopted in 2015 that aims to limit global warming to well below 2°C, preferably 1.5°C, compared to pre-industrial levels through nationally determined contributions.",
    "category": "Climate Policy"
  }}
]

GRADUATE LEVEL EXAMPLE:
Summary: Epigenetics studies heritable changes in gene expression that don't involve alterations to the underlying DNA sequence. Key epigenetic mechanisms include DNA methylation, histone modifications, and non-coding RNAs. DNA methylation typically involves the addition of a methyl group to the 5' position of cytosine in CpG dinucleotides, often resulting in gene silencing. Histone modifications include acetylation, methylation, phosphorylation, and ubiquitination of histone tails, creating the "histone code" that influences chromatin structure and gene accessibility. The field has revealed remarkable plasticity in gene expression, with environmental factors like diet, stress, and toxin exposure capable of inducing epigenetic changes that may persist across generations through mechanisms like incomplete erasure during gametogenesis. This challenges traditional Mendelian inheritance models and has profound implications for understanding disease etiology, particularly in cancer, neurodevelopmental disorders, and metabolic diseases. Epigenetic dysregulation is now recognized as a hallmark of cancer, with global hypomethylation and gene-specific hypermethylation common across tumor types. Emerging epigenetic therapeutics include DNMT inhibitors, HDAC inhibitors, and approaches targeting reader proteins of epigenetic marks. The field's evolution has benefited from technological advances including bisulfite sequencing, ChIP-seq, and ATAC-seq, enabling genome-wide epigenetic profiling at unprecedented resolution.

Flashcards:
[
  {{
    "front": "Epigenetics",
    "back": "The study of heritable changes in gene expression that don't involve alterations to the underlying DNA sequence.",
    "category": "Molecular Biology"
  }},
  {{
    "front": "DNA methylation",
    "back": "An epigenetic mechanism involving the addition of a methyl group to the 5' position of cytosine in CpG dinucleotides, often resulting in gene silencing.",
    "category": "Epigenetic Mechanisms"
  }},
  {{
    "front": "Histone code",
    "back": "The combination of various histone modifications (including acetylation, methylation, phosphorylation, and ubiquitination) that influences chromatin structure and gene accessibility.",
    "category": "Chromatin Biology"
  }},
  {{
    "front": "Transgenerational epigenetic inheritance",
    "back": "The persistence of environmentally-induced epigenetic changes across generations through mechanisms like incomplete erasure during gametogenesis.",
    "category": "Inheritance Patterns"
  }},
  {{
    "front": "Epigenetic dysregulation in cancer",
    "back": "A hallmark of cancer characterized by global hypomethylation and gene-specific hypermethylation across tumor types.",
    "category": "Cancer Biology"
  }},
  {{
    "front": "Bisulfite sequencing",
    "back": "A technology used for genome-wide epigenetic profiling that enables detection of DNA methylation patterns at single-nucleotide resolution.",
    "category": "Epigenomic Technologies"
  }}
]

Now, based on the following summary, create up to {max_cards} flashcards:

HERE IS THE SUMMARY:
{summary_text}

Respond ONLY with the properly formatted JSON array of flashcards. Do not include any introductory or explanatory text.
"""
        
        response = model.generate_content(prompt)
        
        try:
            json_text = response.text
            if "```json" in json_text:
                json_text = json_text.split("```json")[1].split("```")[0].strip()
            elif "```" in json_text:
                json_text = json_text.split("```")[1].split("```")[0].strip()
                
            flashcards_data = json.loads(json_text)
            
            if not flashcards_data:
                logger.warning("No flashcards generated from the summary text.")
                print("No definitions found in the summary text.")
                
            return flashcards_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from flashcard generation: {e}")
            print("Response received:", response.text[:100] + "...")
            logger.error(f"Error decoding JSON from flashcard generation: {e}")
            logger.error("Response received: %s", response.text[:100] + "...")
            return None
    
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        logger.error(f"Error generating flashcards: {e}")
        return None