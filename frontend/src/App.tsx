import "./App.css";
import { useRef, useState } from "react";

function App() {
  // Hidden file input ko control karne ke liye
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // Selected files
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  // Upload status
  const [uploadStatus, setUploadStatus] = useState<
    Record<string, "uploading" | "ready" | "failed">
  >({});

  // Chunk count returned by backend
  const [chunkCounts, setChunkCounts] = useState<
    Record<string, number>
  >({});

  // Chat state
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  // Sources returned by backend
  const [sources, setSources] = useState<
    {
      source_file: string;
      page_number: number;
      content_type: string;
    }[]
  >([]);

  // Loading state
  const [isAsking, setIsAsking] = useState(false);

  // -----------------------------------
  // OPEN FILE PICKER
  // -----------------------------------

  const handleChooseFiles = () => {
    fileInputRef.current?.click();
  };

  // -----------------------------------
  // FILE UPLOAD
  // -----------------------------------

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const files = Array.from(event.target.files ?? []);

    setSelectedFiles(files);

    for (const file of files) {
      // Uploading state
      setUploadStatus((previous) => ({
        ...previous,
        [file.name]: "uploading",
      }));

      const formData = new FormData();

      formData.append("file", file);

      try {
        const response = await fetch(
          "http://127.0.0.1:8000/upload",
          {
            method: "POST",
            body: formData,
          }
        );

        const data = await response.json();

        // Backend error
        if (!response.ok) {
          throw new Error(
            data.detail || "Upload failed"
          );
        }

        console.log("Backend response:", data);

        // Save actual chunk count
        setChunkCounts((previous) => ({
          ...previous,
          [file.name]: data.chunks_created,
        }));

        // Ready state
        setUploadStatus((previous) => ({
          ...previous,
          [file.name]: "ready",
        }));
      } catch (error) {
        console.error("Upload failed:", error);

        // Failed state
        setUploadStatus((previous) => ({
          ...previous,
          [file.name]: "failed",
        }));
      }
    }
  };

  // -----------------------------------
  // ASK QUESTION
  // -----------------------------------

  const handleAsk = async () => {
    const trimmedQuestion = question.trim();

    // Empty question ko send nahi karna
    if (!trimmedQuestion) {
      return;
    }

    // Loading start
    setIsAsking(true);

    // Purana answer clear
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: trimmedQuestion,
          }),
        }
      );

      const data = await response.json();

      // Backend error
      if (!response.ok) {
        throw new Error(
          data.detail || "Question failed"
        );
      }

      console.log("Ask response:", data);

      // Actual AI answer
      setAnswer(data.answer || "");

      // Actual sources
      setSources(data.sources || []);
    } catch (error) {
      console.error("Ask failed:", error);

      setAnswer(
        "Sorry, I couldn't process that question right now."
      );
    } finally {
      // Loading stop
      setIsAsking(false);
    }
  };

  // -----------------------------------
  // UI
  // -----------------------------------

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">✦</div>

          <div className="brand-name">
            DocuMind <span>AI</span>
          </div>
        </div>

        <nav className="navigation">
          <button className="nav-item active">
            <span>⌂</span>
            Workspace
          </button>

          <button className="nav-item">
            <span>◫</span>
            Documents
          </button>

          <button className="nav-item">
            <span>◌</span>
            Chat History
          </button>
        </nav>

        <div className="section-label">
          RECENT
        </div>

        <div className="recent-list">
          <div>IoT Architecture Notes</div>
          <div>Machine Learning Basics</div>
          <div>Research Paper — RAG</div>
        </div>

        <div className="sidebar-bottom">
          <div className="system-status">
            <span className="status-dot"></span>
            RAG engine ready
          </div>
        </div>
      </aside>

      {/* Main */}
      <main className="main">

        {/* Top bar */}
        <header className="topbar">
          <div className="breadcrumb">
            Workspace /{" "}
            <strong>Multimodal RAG</strong>
          </div>

          <div className="topbar-actions">
            <button className="icon-button">
              ☼
            </button>

            <button className="icon-button">
              ⚙
            </button>
          </div>
        </header>

        {/* Workspace */}
        <section className="workspace">

          {/* Hero */}
          <div className="hero">

            <div>
              <div className="eyebrow">
                MULTIMODAL DOCUMENT INTELLIGENCE
              </div>

              <h1>
                Understand your documents.
                <br />
                <span>Ask anything.</span>
              </h1>

              <p>
                Upload PDFs, DOCX files, images and
                reports. Ask questions naturally and
                get grounded answers with document
                sources.
              </p>
            </div>

            <div className="tech-badge">
              Gemini Vision · ChromaDB · RAG
            </div>

          </div>

          {/* Upload */}
          <div className="upload-card">

            <div className="upload-icon">
              ↥
            </div>

            <div className="upload-content">
              <h3>
                Drop documents here
              </h3>

              <p>
                PDF, DOCX, PNG or JPG ·
                Multimodal extraction enabled
              </p>
            </div>

            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept=".pdf,.docx,.png,.jpg,.jpeg"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />

            {/* Choose files */}
            <button
              className="primary-button"
              onClick={handleChooseFiles}
            >
              Choose files
            </button>

          </div>

          {/* Selected files */}
          {selectedFiles.length > 0 && (
            <div className="selected-files">

              {selectedFiles.map((file) => (
                <div
                  className="selected-file"
                  key={`${file.name}-${file.size}`}
                >

                  <div>
                    <strong>
                      {file.name}
                    </strong>

                    <span>
                      {(
                        file.size /
                        1024 /
                        1024
                      ).toFixed(2)}{" "}
                      MB

                      {chunkCounts[file.name] !==
                        undefined &&
                        ` · ${chunkCounts[file.name]} chunks`}
                    </span>
                  </div>

                  <div>

                    {uploadStatus[file.name] ===
                      "uploading" && (
                      <span className="file-status uploading">
                        Processing...
                      </span>
                    )}

                    {uploadStatus[file.name] ===
                      "ready" && (
                      <span className="file-status ready-status">
                        ✓ Ready
                      </span>
                    )}

                    {uploadStatus[file.name] ===
                      "failed" && (
                      <span className="file-status failed">
                        ✕ Failed
                      </span>
                    )}

                  </div>

                </div>
              ))}

            </div>
          )}

          {/* Main Grid */}
          <div className="content-grid">

            {/* CHAT PANEL */}
            <section className="panel chat-panel">

              {/* Chat header */}
              <div className="panel-header">

                <div>
                  <div className="panel-title">
                    Ask your documents
                  </div>

                  <div className="panel-subtitle">
                    Grounded answers from your
                    indexed knowledge
                  </div>
                </div>

                <div className="source-count">
                  {sources.length > 0
                    ? `${sources.length} sources`
                    : "RAG"}
                </div>

              </div>

              {/* Chat content */}
              <div className="chat-content">

                {/* Empty state */}
                {!question &&
                  !answer &&
                  !isAsking && (
                    <div className="empty-chat">

                      <div className="empty-chat-icon">
                        ✦
                      </div>

                      <h3>
                        Ask your documents anything
                      </h3>

                      <p>
                        Ask a question and DocuMind
                        will search your indexed
                        documents for the answer.
                      </p>

                    </div>
                  )}

                {/* User question */}
                {question && (
                  <div className="message user-message">

                    <div className="message-bubble">
                      {question}
                    </div>

                  </div>
                )}

                {/* Loading */}
                {isAsking && (
                  <div className="message ai-message">

                    <div className="answer-label">
                      AI ANSWER
                    </div>

                    <div className="message-bubble thinking">
                      Thinking over your
                      documents...
                      <span>
                        {" "}
                        ● ● ●
                      </span>
                    </div>

                  </div>
                )}

                {/* Real AI answer */}
                {answer && !isAsking && (
                  <div className="message ai-message">

                    <div className="answer-label">
                      AI ANSWER
                    </div>

                    <div className="message-bubble">
                      {answer}
                    </div>

                    {/* Sources */}
                    {sources.length > 0 && (
                      <div className="sources">

                        {sources.map(
                          (source, index) => {

                            const fileName =
                              source.source_file
                                .split(/[\\/]/)
                                .pop() ||
                              "Document";

                            return (
                              <button
                                key={index}
                              >
                                📄{" "}
                                {fileName} · p.
                                {source.page_number}
                              </button>
                            );
                          }
                        )}

                      </div>
                    )}

                  </div>
                )}

              </div>

              {/* Chat input */}
              <div className="chat-input-area">

                <input
                  value={question}
                  onChange={(event) => {
                    setQuestion(
                      event.target.value
                    );
                  }}
                  onKeyDown={(event) => {
                    if (
                      event.key === "Enter"
                    ) {
                      handleAsk();
                    }
                  }}
                  placeholder="Ask a question about your documents..."
                  disabled={isAsking}
                />

                <button
                  className="send-button"
                  onClick={handleAsk}
                  disabled={
                    isAsking ||
                    !question.trim()
                  }
                >
                  {isAsking ? "..." : "➤"}
                </button>

              </div>

            </section>

            {/* DOCUMENTS PANEL */}
            <section className="panel documents-panel">

              <div className="panel-header">

                <div>
                  <div className="panel-title">
                    Your documents
                  </div>

                  <div className="panel-subtitle">
                    3 indexed
                  </div>
                </div>

                <span className="library-label">
                  Library
                </span>

              </div>

              {/* Documents */}
              <div className="documents-list">

                <div className="document">

                  <div className="document-icon pdf">
                    📕
                  </div>

                  <div className="document-info">

                    <div className="document-name">
                      IOT Notes_NM.pdf
                    </div>

                    <div className="document-meta">
                      PDF · 12 pages · 34 chunks
                    </div>

                  </div>

                  <div className="ready">
                    ✓ Ready
                  </div>

                </div>

                <div className="document">

                  <div className="document-icon docx">
                    📘
                  </div>

                  <div className="document-info">

                    <div className="document-name">
                      Machine Learning Basics.docx
                    </div>

                    <div className="document-meta">
                      DOCX · 8 pages · 21 chunks
                    </div>

                  </div>

                  <div className="ready">
                    ✓ Ready
                  </div>

                </div>

                <div className="document">

                  <div className="document-icon image">
                    🖼️
                  </div>

                  <div className="document-info">

                    <div className="document-name">
                      architecture.png
                    </div>

                    <div className="document-meta">
                      Image · Vision description
                    </div>

                  </div>

                  <div className="ready">
                    ✓ Ready
                  </div>

                </div>

              </div>

              {/* Retrieval pipeline */}
              <div className="retrieval">

                <div className="panel-title">
                  Retrieval pipeline
                </div>

                <div className="panel-subtitle">
                  What happens behind the answer
                </div>

                <div className="pipeline">

                  <div className="pipeline-step">
                    <div>✓</div>
                    Query embedding created
                  </div>

                  <div className="pipeline-step">
                    <div>✓</div>
                    Similar chunks retrieved
                  </div>

                  <div className="pipeline-step">
                    <div>✓</div>
                    Text + tables + image context
                  </div>

                  <div className="pipeline-step">
                    <div>✓</div>
                    Gemini generates grounded
                    answer
                  </div>

                </div>

              </div>

            </section>

          </div>

          <div className="footer-note">
            Multimodal RAG · AI-powered document
            intelligence
          </div>

        </section>
      </main>
    </div>
  );
}

export default App;