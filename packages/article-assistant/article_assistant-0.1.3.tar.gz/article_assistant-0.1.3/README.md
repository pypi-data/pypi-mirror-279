# Article-Assistant

#### Article Assistant is a comprehensive Python package designed to assist with authoring and reviewing scientific articles. Utilizing advanced AI models from OpenAI, the package offers tools for generating complete articles based on provided topics and descriptions and reviewing existing articles for clarity, accuracy, and overall quality.


### Features
* Authoring: Automatically generate well-structured review articles with sections including Title, Abstract, Introduction, Body, Conclusion, and Sources.
* Reviewing: Use a multi-agent AI system to review articles. The system includes:
  * SME Reviewer: Reviews the article for technical accuracy and provides detailed feedback. 
  * SME Search: Searches the internet for similar articles and provides recommendations based on findings. 
  * Lead Reviewer: Summarizes the findings from both SME agents into a single cohesive summary.


### Quick Start:

Install the Application:

    pip install article-assistant

Author a New Article:

    # Set API Key:
    api_key = os.getenv('OPENAI_API_KEY')
    author = Author(api_key)

    # Describe the article:
    topic = "quaternary ammonium compounds"
    description = "An article of quaternary ammonium compounds and their efficacy"

    # Generate the Article:
    outline = author.generate_outline(topic, description)
    paper_content = author.draft_paper(outline)
    author.save_to_word(paper_content, "Drafted_Paper.docx")

Review Existing Article:

    # Select files to review:
    review = Review()
    pdf_path = "path/to/file.pdf"

    # Run Review:
    results = review.review_article(pdf_path)

    # Print the results
    print("\nSummary by Lead Reviewer:")
    print(results["summary"])

    print("\nSME_Reviewer Outputs:")
    for output in results["sme_reviewer"]:
        print(output)

    print("\nSME_Search Outputs:")
    for output in results["sme_search"]:
        print(output)