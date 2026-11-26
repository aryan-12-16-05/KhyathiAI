
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import "./MarkdownRenderer.css";

interface MarkdownRendererProps {
    content: string;
}

function MarkdownRenderer({ content }: MarkdownRendererProps) {
    return (
        <div className="markdown-renderer">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {content}
            </ReactMarkdown>
        </div>
    );
}

export default MarkdownRenderer;
