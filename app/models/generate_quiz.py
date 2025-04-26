from app.config.gemini_ai_config import configure_genai
import google.generativeai as genai
from dotenv import load_dotenv
from app.logger.logger import logger
import json
logger = logger(__name__)

def generate_quiz(summary_text, num_questions=10, difficulty="mixed"):
    logger.info("Generating quiz...")
    """
    Generate a quiz with multiple-choice questions based on the provided summary text using Google Gemini AI.
    Args: Summary text (str): The summary text to base the quiz on.
          num_questions (int): The number of questions to generate. Default is 10.
          difficulty (str): The difficulty level of the questions. Options are "undergraduate", "graduate", or "mixed". Default is "mixed".
          Returns: list: A list of dictionaries containing the generated quiz questions and answers.
    """

    try:
        if not configure_genai():
            logger.error("API configuration failed. Unable to generate quiz.")
            return []
    
        model = genai.GenerativeModel(model_name='gemini-2.0-flash')
        logger.info("Quiz generation started.")
        logger.info("Model choosen: gemini-2.0-flash")
        
        difficulty_instruction = ""
        if difficulty == "undergraduate":
            difficulty_instruction = "Create questions suitable for undergraduate students, focusing on fundamental understanding and application of concepts."
        elif difficulty == "graduate":
            difficulty_instruction = "Create questions suitable for PhD students, focusing on advanced analysis, synthesis of complex ideas, and evaluation of theoretical implications."
        else:  
            difficulty_instruction = "Create a mix of questions with varying difficulty levels: 60% at undergraduate level (fundamental understanding and application) and 40% at graduate/PhD level (advanced analysis and synthesis of complex concepts)."
        
        prompt = f"""Based on a given summary, create {num_questions} multiple-choice questions to test understanding of the content.

{difficulty_instruction}

Here are examples at two different academic levels:

UNDERGRADUATE LEVEL EXAMPLE (Medium Difficulty):
Summary: Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, but since the 1800s, human activities have been the main driver of climate change, primarily due to the burning of fossil fuels like coal, oil, and gas, which produces heat-trapping gases. The primary greenhouse gases include carbon dioxide, methane, nitrous oxide, and fluorinated gases. Global warming is causing polar ice sheets and glaciers to melt, raising sea levels and threatening coastal communities. Climate models project that without significant mitigation efforts, global temperatures could rise by 2.7°F to 8.6°F by 2100, with catastrophic consequences including extreme weather events, biodiversity loss, food insecurity, and economic damage. The Paris Agreement, adopted in 2015, aims to limit global warming to well below 2°C, preferably 1.5°C, compared to pre-industrial levels through nationally determined contributions to greenhouse gas reductions.

Questions:
[
  {{
    "question": "Which human activity has been identified as the main driver of climate change since the 1800s?",
    "options": [
      "Deforestation",
      "Agriculture",
      "Burning fossil fuels",
      "Urbanization"
    ],
    "answer": "C",
    "explanation": "While all options contribute to climate change, the burning of fossil fuels (coal, oil, and gas) has been the primary human activity driving climate change since the Industrial Revolution, as it releases significant amounts of carbon dioxide into the atmosphere."
  }},
  {{
    "question": "What is the main goal of the 2015 Paris Agreement?",
    "options": [
      "To eliminate the use of all fossil fuels by 2050",
      "To limit global warming to well below 2°C compared to pre-industrial levels",
      "To provide funding for developing countries affected by climate change",
      "To establish a global carbon tax"
    ],
    "answer": "B",
    "explanation": "The Paris Agreement's central aim is to strengthen the global response to climate change by keeping global temperature rise this century well below 2°C above pre-industrial levels and to pursue efforts to limit the temperature increase even further to 1.5°C."
  }},
  {{
    "question": "Which of the following is a direct consequence of global warming on Earth's cryosphere?",
    "options": [
      "Increase in tropical storms",
      "Ocean acidification",
      "Melting of polar ice sheets",
      "Rise in infectious diseases"
    ],
    "answer": "C",
    "explanation": "Global warming directly causes the melting of the cryosphere (frozen parts of the Earth), including polar ice sheets and glaciers, which contributes to sea level rise."
  }}
]

GRADUATE/PhD LEVEL EXAMPLE (Advanced Difficulty):
Summary: Epigenetics studies heritable changes in gene expression that don't involve alterations to the underlying DNA sequence. Key epigenetic mechanisms include DNA methylation, histone modifications, and non-coding RNAs. DNA methylation typically involves the addition of a methyl group to the 5' position of cytosine in CpG dinucleotides, often resulting in gene silencing. Histone modifications include acetylation, methylation, phosphorylation, and ubiquitination of histone tails, creating the "histone code" that influences chromatin structure and gene accessibility. The field has revealed remarkable plasticity in gene expression, with environmental factors like diet, stress, and toxin exposure capable of inducing epigenetic changes that may persist across generations through mechanisms like incomplete erasure during gametogenesis. This challenges traditional Mendelian inheritance models and has profound implications for understanding disease etiology, particularly in cancer, neurodevelopmental disorders, and metabolic diseases. Epigenetic dysregulation is now recognized as a hallmark of cancer, with global hypomethylation and gene-specific hypermethylation common across tumor types. Emerging epigenetic therapeutics include DNMT inhibitors, HDAC inhibitors, and approaches targeting reader proteins of epigenetic marks. The field's evolution has benefited from technological advances including bisulfite sequencing, ChIP-seq, and ATAC-seq, enabling genome-wide epigenetic profiling at unprecedented resolution.

Questions:
[
  {{
    "question": "How does the transgenerational inheritance of environmentally-induced epigenetic modifications challenge classical genetic theory?",
    "options": [
      "It suggests that genetic mutations can be spontaneously reversed",
      "It contradicts the central dogma of molecular biology",
      "It challenges the Mendelian concept that inheritance occurs exclusively through DNA sequence transmission",
      "It implies that mitochondrial DNA is more important than nuclear DNA"
    ],
    "answer": "C",
    "explanation": "The inheritance of environmentally-induced epigenetic changes across generations challenges Mendelian genetics, which posits that inheritance occurs exclusively through transmission of DNA sequences. Epigenetic inheritance suggests that acquired characteristics can be passed to offspring without changes to DNA sequence, a concept that was previously rejected in classical genetics."
  }},
  {{
    "question": "Which theoretical model best explains the observation that identical twins often show increasing epigenetic divergence as they age?",
    "options": [
      "Stochastic epigenetic drift in response to subtle environmental differences",
      "Programmed epigenetic diversification driven by evolutionary advantage",
      "Lamarckian inheritance of acquired characteristics",
      "Random deamination of methylated cytosines"
    ],
    "answer": "A",
    "explanation": "The increasing epigenetic divergence between identical twins over time is best explained by stochastic epigenetic drift in response to different environmental exposures. This model accounts for how genetically identical individuals develop different epigenetic profiles and potentially different phenotypes despite sharing identical DNA sequences."
  }},
  {{
    "question": "In the context of cancer epigenetics, what mechanistic explanation best accounts for the paradoxical observation of global hypomethylation concurrent with gene-specific hypermethylation?",
    "options": [
      "Mutations in DNA methyltransferases that randomly alter their targeting",
      "Differential activity of TET enzymes across genomic regions",
      "Redistribution of DNMTs from repetitive elements to tumor suppressor promoters due to altered chromatin organization",
      "Selective pressure that independently favors both hypomethylation and hypermethylation events"
    ],
    "answer": "C",
    "explanation": "The paradox is best explained by the redistribution of DNA methyltransferases (DNMTs) from repetitive elements to specific gene promoters, particularly tumor suppressors. This is associated with altered nuclear architecture and chromatin reorganization in cancer cells, leading to simultaneous global hypomethylation (activating oncogenes and transposable elements) and targeted hypermethylation of tumor suppressor genes."
  }},
  {{
    "question": "Which conceptual framework most accurately captures the relationship between genetic variants and epigenetic modifications in complex disease etiology?",
    "options": [
      "Genetic variants determine epigenetic patterns which then cause disease",
      "Epigenetic modifications occur independently of genetic background",
      "A bidirectional relationship where genetic variants can affect epigenetic modifications, while environmental factors can induce epigenetic changes that modulate genetic effects",
      "Epigenetic modifications cause genetic mutations that lead to disease"
    ],
    "answer": "C",
    "explanation": "Complex disease etiology is best understood through a bidirectional framework where genetic variants can influence epigenetic patterns (for example, mutations in epigenetic enzymes), while environmentally-induced epigenetic modifications can alter how genetic variants are expressed. This gene-environment interaction model explains why genetic risk factors show variable penetrance and why environmental exposures affect individuals differently based on their genetic background."
  }},
  {{
    "question": "Which methodological approach would be most appropriate for investigating whether prenatal nutrition influences metabolic phenotypes through epigenetic reprogramming?",
    "options": [
      "A cross-sectional study comparing DNA methylation patterns in adults with different BMIs",
      "A genome-wide association study correlating SNPs with metabolic traits",
      "A longitudinal cohort study with maternal nutritional assessments, offspring cord blood epigenetic profiling, and follow-up metabolic phenotyping",
      "An in vitro study of adipocyte differentiation under different nutrient conditions"
    ],
    "answer": "C",
    "explanation": "A longitudinal cohort approach with maternal nutritional assessments, epigenetic profiling at birth (cord blood), and long-term follow-up is methodologically superior for establishing causal relationships between prenatal nutrition, epigenetic changes, and metabolic outcomes. This design accounts for temporal relationships and allows researchers to control for confounding variables while establishing the persistence of epigenetic changes and their association with metabolic phenotypes."
  }}
]

Now, based on the following summary, create {num_questions} multiple-choice questions:

HERE IS THE SUMMARY:
{summary_text}

Respond ONLY with the properly formatted JSON array of questions. Do not include any introductory or explanatory text.
"""
        
        response = model.generate_content(prompt)
        logger.info("Quiz generation completed.")
        logger.info("Response received from model.")

        try:
            json_text = response.text
            if "```json" in json_text:
                json_text = json_text.split("```json")[1].split("```")[0].strip()
            elif "```" in json_text:
                json_text = json_text.split("```")[1].split("```")[0].strip()
                
            quiz_data = json.loads(json_text)
            quiz_data = list(quiz_data)  # Ensure the data is a list of dictionaries
            logger.info("Quiz data parsed successfully.")
            return quiz_data
        except json.JSONDecodeError as e:
            logger.error("Failed to parse quiz data from response.")
            logger.error(f"Error: {e}")
            return []
    
    except Exception as e:
        logger.info("Error generating quiz:")
        logger.error(f"Error: {e}")
        return []