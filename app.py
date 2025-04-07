import gradio as gr
import requests

API_URL = "https://apiend-08av.onrender.com/recommend/"

def fetch_recommendations(query, top_k):
    try:
        payload = {"query": query, "top_n": int(top_k)}
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()

        data = response.json()

        # Extract list from dictionary key
        recommendations = data.get("recommendations", [])
        if not isinstance(recommendations, list):
            return "❌ Unexpected response format from API."

        formatted_results = ""
        for i, rec in enumerate(recommendations, start=1):
            job_solution = rec.get("Job Solution", "N/A")
            link = rec.get("Link", "#")
            remote = rec.get("Remote Testing", "N/A")
            adaptive = rec.get("Adaptive/IRT", "N/A")
            test_types = rec.get("Test Types", "N/A")
            duration = rec.get("Duration", "N/A")

            formatted_results += (
                f"### {i}. [{job_solution}]({link})\n"
                f"- **Remote Testing**: {remote}\n"
                f"- **Adaptive/IRT**: {adaptive}\n"
                f"- **Test Types**: {test_types}\n"
                f"- **Duration**: {duration} minutes\n\n"
            )

        return formatted_results.strip()

    except Exception as e:
        return f"❌ Error: {str(e)}"

# Build Gradio UI
gr.Interface(
    fn=fetch_recommendations,
    inputs=[
        gr.Textbox(label="Enter your query"),
        gr.Number(label="How many recommendations?", value=5),
    ],
    outputs=gr.Markdown(label="Recommendations"),
    title="Assessment Recommender",
    description="Enter a job role or query and the number of recommendations you want.",
).launch(server_name="0.0.0.0", server_port=8081)

