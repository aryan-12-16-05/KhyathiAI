# KhyathiAI 🎥🤖

**Turn YouTube videos into clear, structured knowledge.**

KhyathiAI is an AI-powered YouTube video summarization project that transforms video transcripts into easy-to-understand summaries, helping users quickly grasp important concepts without watching an entire video.

The project is being developed in stages, starting with a Python-based summarization pipeline and expanding into a complete web application with a frontend and backend.

## ✨ Current Features

The initial Python notebook prototype includes:

- **YouTube URL Extraction:** Extracts the video ID from supported YouTube URL formats.
- **Transcript Extraction:** Retrieves available YouTube captions, including auto-generated captions.
- **Transcript Preprocessing:** Cleans and prepares transcript text for summarization.
- **Text Chunking:** Splits lengthy transcripts into manageable chunks.
- **AI-Powered Summarization:** Uses NVIDIA Nemotron 3 Ultra to generate summaries for individual chunks.
- **Final Summary Generation:** Combines chunk summaries into one structured, easy-to-understand result.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Google Colab | Notebook development and execution |
| YouTube Transcript API | Extracting video transcripts |
| OpenRouter API | Accessing AI models |
| NVIDIA Nemotron 3 Ultra | AI-powered summarization |
| Requests | API communication |

## ⚙️ How It Works

The current prototype follows this pipeline:

1. Provide a YouTube video URL.
2. Extract the video ID.
3. Retrieve the available transcript.
4. Clean and preprocess the transcript.
5. Divide the transcript into smaller chunks.
6. Generate summaries for each chunk using the AI model.
7. Consolidate the results into a structured final summary.

## 🚀 Getting Started

The current prototype runs in Google Colab.

**Prerequisites**
- A Google account.
- An OpenRouter account and API key.
- Access to Google Colab.

**Setup Instructions**

1. Clone or download this repository.
2. Open the Jupyter notebook in Google Colab.
3. Create an API key through [OpenRouter](https://openrouter.ai/).
4. In Google Colab, open **Secrets** and add a secret named `OPENROUTER_API_KEY`.
5. Enable notebook access to the secret.
6. Run the notebook cells sequentially.
7. Provide a YouTube video URL and follow the notebook workflow.

**Note:** The current implementation uses a free model variant through OpenRouter. Free model availability and rate limits are subject to provider policies. Never expose or commit your API key to GitHub.

## 🗺️ Project Roadmap

KhyathiAI is under active development.

- [x] Initial Python notebook setup.
- [x] YouTube transcript extraction.
- [x] Transcript cleaning and preprocessing.
- [x] Text chunking.
- [x] AI-powered chunk summarization.
- [x] Final structured summary generation.
- [ ] Develop the frontend interface.
- [ ] Build the backend API.
- [ ] Integrate the frontend and backend.
- [ ] Add more summarization and content-processing features.
- [ ] Deploy the complete application.

## 📌 Current Status

**Phase 1 – Python Prototype: Completed**

The initial notebook implementation is complete through the final summary generation stage. Development will continue with the frontend and backend implementation.

## 🎯 Vision

The goal of KhyathiAI is to make video-based learning and information consumption faster, simpler, and more accessible by turning lengthy videos into meaningful, structured knowledge.

---

**KhyathiAI** | From videos to understanding. 🚀
