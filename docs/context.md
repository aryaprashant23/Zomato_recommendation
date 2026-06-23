**Project Context: AI-Powered Restaurant Recommendation System**

**Overview**

Build an AI-powered restaurant recommendation service inspired by **Zomato**. The system intelligently suggests restaurants based on user preferences by combining structured data with a **Large Language Model (LLM)**.

**Objective**

Design and implement an application that:

1. Takes user preferences (location, budget, cuisine, ratings, and more)
2. Uses a real-world dataset of restaurants
3. Leverages an LLM to generate personalized, human-like recommendations
4. Displays clear and useful results to the user

---

**System Workflow**

**1. Data Ingestion**

- Load and preprocess the Zomato dataset from Hugging Face:
  - **Dataset URL:** https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation
- Extract relevant fields, including:
  - Restaurant name
  - Location
  - Cuisine
  - Cost
  - Rating
  - Other applicable metadata from the dataset

**2. User Input**

Collect user preferences:

| Preference | Examples |
|------------|----------|
| **Location** | Delhi, Bangalore |
| **Budget** | Low, medium, high |
| **Cuisine** | Italian, Chinese |
| **Minimum rating** | Numeric threshold |
| **Additional preferences** | Family-friendly, quick service, etc. |

**3. Integration Layer**

- Filter and prepare relevant restaurant data based on user input
- Pass structured results into an LLM prompt
- Design a prompt that helps the LLM reason and rank options

**4. Recommendation Engine**

Use the LLM to:

- **Rank** restaurants
- **Provide explanations** — why each recommendation fits the user's preferences
- **Optionally summarize** choices

**5. Output Display**

Present top recommendations in a user-friendly format. Each recommendation should include:

- Restaurant name
- Cuisine
- Rating
- Estimated cost
- AI-generated explanation

---

**Key Technical Requirements**

| Area | Requirement |
|------|-------------|
| **Data source** | Hugging Face — `ManikaSaini/zomato-restaurant-recommendation` |
| **AI component** | LLM for ranking, reasoning, and natural-language explanations |
| **Input** | Structured user preferences (location, budget, cuisine, rating, extras) |
| **Processing** | Filter dataset → structure results → LLM prompt → ranked recommendations |
| **Output** | Top recommendations with metadata and AI-generated rationale |

---

**Success Criteria**

- User preferences are collected and applied to filter the restaurant dataset
- Filtered data is passed to an LLM with a well-designed prompt
- The LLM returns ranked recommendations with clear, personalized explanations
- Results are displayed in a readable, user-friendly format

---

**Source**

This context is derived from `docs/ProblemStatement.txt`.
