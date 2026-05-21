"use client";

/**
 * Lightweight markdown renderer for legal AI responses.
 * Handles: bold, links, lists, headings, code, citations.
 * No external deps — pure regex transforms.
 *
 * Security: All input is HTML-escaped FIRST, then only safe markdown
 * constructs are converted to HTML tags. No raw user HTML passes through.
 */
export function MarkdownContent({ content }: { content: string }) {
  const html = markdownToHtml(content);
  // Safe: content is escaped first, then only safe tags are produced by our transforms
  return (
    <div
      className="prose-legal text-caption text-ink-muted-80 [&_strong]:text-ink [&_a]:text-primary [&_a]:underline [&_h3]:text-body-strong [&_h3]:text-ink [&_h3]:mt-3 [&_h3]:mb-1 [&_ul]:list-disc [&_ul]:pl-5 [&_ul]:space-y-1 [&_ol]:list-decimal [&_ol]:pl-5 [&_ol]:space-y-1 [&_code]:bg-ink/5 [&_code]:px-1 [&_code]:rounded [&_code]:text-micro-legal [&_code]:font-mono [&_p]:mb-2 [&_blockquote]:border-l-2 [&_blockquote]:border-primary/30 [&_blockquote]:pl-3 [&_blockquote]:italic [&_blockquote]:text-ink-muted-48"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function markdownToHtml(md: string): string {
  const lines = md.split("\n");
  const out: string[] = [];
  let inList = false;
  let listType = "";

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Headings
    const h3 = line.match(/^###\s+(.+)/);
    if (h3) {
      closeList();
      out.push(`<h3>${inline(h3[1])}</h3>`);
      continue;
    }
    const h2 = line.match(/^##\s+(.+)/);
    if (h2) {
      closeList();
      out.push(`<h3>${inline(h2[1])}</h3>`);
      continue;
    }

    // Unordered list
    const ul = line.match(/^[\-\*]\s+(.+)/);
    if (ul) {
      if (!inList || listType !== "ul") {
        closeList();
        out.push("<ul>");
        inList = true;
        listType = "ul";
      }
      out.push(`<li>${inline(ul[1])}</li>`);
      continue;
    }

    // Ordered list
    const ol = line.match(/^\d+[\.\)]\s+(.+)/);
    if (ol) {
      if (!inList || listType !== "ol") {
        closeList();
        out.push("<ol>");
        inList = true;
        listType = "ol";
      }
      out.push(`<li>${inline(ol[1])}</li>`);
      continue;
    }

    // Blockquote
    const bq = line.match(/^>\s?(.*)/);
    if (bq) {
      closeList();
      out.push(`<blockquote>${inline(bq[1])}</blockquote>`);
      continue;
    }

    // Empty line
    if (line.trim() === "") {
      closeList();
      continue;
    }

    // Paragraph
    closeList();
    out.push(`<p>${inline(line)}</p>`);
  }
  closeList();
  return out.join("");

  function closeList() {
    if (inList) {
      out.push(listType === "ol" ? "</ol>" : "</ul>");
      inList = false;
      listType = "";
    }
  }
}

function inline(text: string): string {
  // Escape HTML first — prevents any XSS from user/AI content
  let s = escapeHtml(text);
  // Bold
  s = s.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  // Inline code
  s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
  // Links [text](url)
  s = s.replace(
    /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,
    '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>'
  );
  // Bare URLs
  s = s.replace(
    /(?<![">])(https?:\/\/[^\s<]+)/g,
    '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
  );
  return s;
}
