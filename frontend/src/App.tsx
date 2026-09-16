import "./App.css";

function App() {
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

        <div className="section-label">RECENT</div>

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
            Workspace / <strong>Multimodal RAG</strong>
          </div>

          <div className="topbar-actions">
            <button className="icon-button">☼</button>
            <button className="icon-button">⚙</button>
          </div>
        </header>

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
                Upload PDFs, DOCX files, images and reports. Ask questions
                naturally and get grounded answers with document sources.
              </p>
            </div>

            <div className="tech-badge">
              Gemini Vision · ChromaDB · RAG
            </div>
          </div>

          {/* Upload */}
          <div className="upload-card">
            <div className="upload-icon">↥</div>

            <div className="upload-content">
              <h3>Drop documents here</h3>

              <p>
                PDF, DOCX, PNG or JPG · Multimodal extraction enabled
              </p>
            </div>

            <button className="primary-button">
              Choose files
            </button>
          </div>

          {/* Main Grid */}
          <div className="content-grid">

            {/* Chat */}
            <section className="panel chat-panel">
              <div className="panel-header">
                <div>
                  <div className="panel-title">
                    Ask your documents
                  </div>

                  <div className="panel-subtitle">
                    Grounded answers from your indexed knowledge
                  </div>
                </div>

                <div className="source-count">
                  5 sources
                </div>
              </div>

              <div className="chat-content">
                <div className="message user-message">
                  <div className="message-bubble">
                    What are the main components of the IoT architecture?
                  </div>
                </div>

                <div className="message ai-message">
                  <div className="answer-label">
                    AI ANSWER
                  </div>

                  <div className="message-bubble">
                    The document describes IoT architecture through four
                    core layers: <strong>sensing/devices</strong>,
                    <strong> network & communication</strong>,
                    <strong> data processing</strong>, and
                    <strong> application/services</strong>.
                  </div>

                  <div className="sources">
                    <button>📄 IoT Notes · p.2</button>
                    <button>📊 IoT Notes · p.4</button>
                    <button>🖼 Diagram · p.5</button>
                  </div>
                </div>
              </div>

              <div className="chat-input-area">
                <input
                  placeholder="Ask a question about your documents..."
                />

                <button className="send-button">
                  ➤
                </button>
              </div>
            </section>

            {/* Documents */}
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

              {/* Retrieval */}
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
                    Gemini generates grounded answer
                  </div>

                </div>
              </div>
            </section>

          </div>

          <div className="footer-note">
            Multimodal RAG · AI-powered document intelligence
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;