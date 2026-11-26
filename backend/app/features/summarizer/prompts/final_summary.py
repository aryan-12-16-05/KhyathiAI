
from collections.abc import Sequence

from app.features.summarizer.pipeline.chunker import (
    TranscriptChunk,
)


# ==========================================
# FINAL SUMMARY SYSTEM PROMPT
# ==========================================

FINAL_SUMMARY_SYSTEM_PROMPT = """
You are an expert educational content summarization assistant.

You will receive summaries generated from different segments
of a single YouTube video.

Your task is to combine them into one coherent,
comprehensive, and well-structured final summary.

CORE INSTRUCTIONS:

1. Use only information contained in the supplied chunk summaries.

2. Preserve important explanations, concepts, examples,
   and analogies.

3. Remove repeated information across different chunks.

4. Maintain the logical and chronological flow of the video.

5. Connect related concepts across different segments
   only when the source material supports the connection.

6. Never invent missing facts, examples, or conclusions.

ACCURACY AND ATTRIBUTION RULES:

7. Preserve the distinction between the speaker's claims
   and established technical definitions.

8. Never convert a simplified speaker explanation
   into an established technical fact.

9. Do not present artificial intelligence and machine
   learning as identical concepts merely because the
   speaker informally connects their explanations.

10. When a chunk describes a simplified or debatable claim,
    retain its attribution to the speaker.

11. Preserve phrases such as "the speaker explains",
    "according to the speaker", and "the speaker's analogy"
    where needed for accuracy.

12. Do not silently remove qualifications or caveats
    from individual chunk summaries.

13. Do not add external knowledge or unsupported corrections.

TIMESTAMP RULES:

14. Use only timestamps supplied in the chunk summaries
    or their associated metadata.

15. Do not invent precise topic timestamps.

16. Do not assign the entire duration of a chunk to every
    individual topic discussed within it.

17. When only chunk-level timestamps are available,
    provide the chunk's time range as broad context
    rather than implying exact topic-level timing.

18. If precise topic timing is unavailable, omit
    topic-specific timestamps.

OUTPUT QUALITY:

19. Use simple, clear, educational English.

20. Preserve important technical terminology.

21. Avoid unnecessary repetition.

22. Ensure every statement is supported by the supplied
    chunk summaries.

23. Return the final summary directly in Markdown.

REQUIRED OUTPUT STRUCTURE:

# 1. Overall Summary

Provide a comprehensive overview of the entire video.

# 2. Topic-wise Explanation

Explain the major topics in a logical sequence.
Include timestamps only when supported by the source.

# 3. Important Concepts and Definitions

Explain important concepts introduced in the video.
Clearly attribute informal speaker explanations.

# 4. Examples and Analogies

Collect the examples and analogies mentioned by the speaker.

# 5. Key Takeaways

Present the most important lessons from the video.

# 6. Quick Revision Notes

Provide concise revision points useful for quick learning.
"""


# ==========================================
# FINAL SUMMARY PROMPT BUILDER
# ==========================================

def build_final_summary_messages(
    chunks: Sequence[TranscriptChunk],
    chunk_summaries: Sequence[str],
) -> list[dict[str, str]]:
    """
    Builds the final consolidation prompt from all chunk summaries.
    """

    if not chunks or not chunk_summaries:
        raise ValueError(
            "Chunks and chunk summaries cannot be empty."
        )

    if len(chunks) != len(chunk_summaries):
        raise ValueError(
            "The number of chunks and chunk summaries must match."
        )

    summary_sections = []

    for chunk, summary in zip(chunks, chunk_summaries):

        if not isinstance(chunk, TranscriptChunk):
            raise TypeError(
                "Every chunk must be a TranscriptChunk instance."
            )

        if not isinstance(summary, str) or not summary.strip():
            raise ValueError(
                "Every chunk summary must contain non-empty text."
            )

        summary_sections.append(
            f"""
CHUNK {chunk.chunk_id}

Time Range:
{chunk.start_time:.2f}s - {chunk.end_time:.2f}s

Word Count:
{chunk.word_count}

CHUNK SUMMARY:
{summary.strip()}
"""
        )

    combined_summaries = "\n".join(summary_sections)

    user_prompt = f"""
Create the final structured summary of the complete video.

The following summaries are provided in their original video order.

Use all relevant information while removing duplication.

Preserve the speaker attribution and accuracy qualifications
present in the individual chunk summaries.

Do not assign unsupported topic-level timestamps.

VIDEO CHUNK SUMMARIES:

{combined_summaries}

Follow the required six-section output structure.

Return a complete, coherent educational summary.
"""

    return [
        {
            "role": "system",
            "content": FINAL_SUMMARY_SYSTEM_PROMPT.strip(),
        },
        {
            "role": "user",
            "content": user_prompt.strip(),
        },
    ]
