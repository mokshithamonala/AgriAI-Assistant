# AI Chat Assistant

A modern, full-featured AI chat assistant built with **Next.js 15**, featuring multilingual support, voice input and output, Retrieval-Augmented Generation (RAG), and a comprehensive admin dashboard.

## ✨ Features

### Core Features

- **Intelligent Conversations** – Powered by OpenAI GPT models with context-aware responses.
- **RAG System** – Upload documents to enhance AI responses using your knowledge base.
- **Multilingual Support** – Supports 12 languages: English, Spanish, French, German, Italian, Portuguese, Chinese, Japanese, Korean, Arabic, Hindi, and Russian.
- **Voice Integration** – Speech recognition and text-to-speech capabilities.
- **Admin Dashboard** – Monitor usage, manage documents, and view statistics.

### Technical Features

- Responsive user interface built with Tailwind CSS and shadcn/ui.
- Dark and light mode support.
- Real-time chat interface with typing indicators.
- Document management for the RAG knowledge base.
- Conversation history and management.
- API-first architecture.

## 🛠️ Technology Stack

### Frontend
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui
- Lucide Icons
- Recharts

### Backend
- Next.js API Routes
- OpenAI API
- Supabase (PostgreSQL with pgvector)
- LangChain

### AI / ML
- OpenAI GPT-4o-mini
- OpenAI Embeddings
- pgvector for similarity search
- Retrieval-Augmented Generation (RAG)

## 🚀 Getting Started

### Prerequisites

- Node.js 18 or later
- npm or yarn
- OpenAI API key
- Supabase account (optional, for persistent storage)

### Installation

**1. Clone the repository**

```bash
git clone <repository-url>
cd ai-chat-assistant
```

**2. Install dependencies**

```bash
npm install
```

**3. Configure environment variables**

Create a `.env.local` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

Never commit your actual API keys or `.env.local` file.

**4. Start the development server**

```bash
npm run dev
```

**5. Open the application**

Visit  in your browser.

## 📁 Project Structure

```text
.
├── app/
│   ├── api/
│   │   ├── chat/route.ts
│   │   ├── documents/route.ts
│   │   ├── admin/route.ts
│   │   ├── translate/route.ts
│   │   └── voice/route.ts
│   ├── admin/
│   │   └── page.tsx
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── chat/
│   ├── admin/
│   ├── voice/
│   └── ui/
├── context/
│   ├── ChatContext.tsx
│   └── ThemeProvider.tsx
├── hooks/
│   └── use-toast.ts
├── lib/
│   ├── ai/
│   │   ├── openai.ts
│   │   └── langchain.ts
│   ├── db/
│   │   ├── supabase.ts
│   │   └── repository.ts
│   ├── env.ts
│   └── utils.ts
└── types/
    └── index.ts
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/chat` | Send a message to the AI assistant |
| GET | `/api/documents` | Retrieve knowledge-base documents |
| POST | `/api/documents` | Upload a document |
| DELETE | `/api/documents?id=<uuid>` | Delete a document |
| GET | `/api/admin` | Retrieve admin statistics |
| POST | `/api/translate` | Translate text |
| POST | `/api/voice` | Generate speech from text |

### Chat API Example

**Request:**

```json
{
  "message": "Hello, how can I help?",
  "conversationId": "uuid (optional)",
  "language": "en",
  "history": [
    {
      "role": "user",
      "content": "Previous message"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    }
  ]
}
```

**Response:**

```json
{
  "message": {
    "id": "uuid",
    "role": "assistant",
    "content": "AI response...",
    "createdAt": "2024-01-01T00:00:00.000Z"
  },
  "conversationId": "uuid",
  "sources": []
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI API key for GPT and embeddings | Yes* |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | No |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key | No |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service-role key | No |

*The application supports demo mode without an OpenAI API key, if configured in the implementation.*

### Demo Mode

When enabled, demo mode can provide:

- Predefined responses for common queries.
- Feature demonstrations.
- UI/UX preview without live AI integration.

## 🌐 Features in Detail

### Multilingual Support

- Switch between 12 supported languages.
- Select a language directly in the chat interface.
- Use speech recognition in supported languages.
- Generate text-to-speech responses.

### Voice Integration

- **Speech Recognition:** Use the microphone to enter messages through speech.
- **Text-to-Speech:** Listen to AI responses using the speaker option.

### RAG System

1. Upload documents through the Admin Dashboard.
2. Convert document content into vector embeddings.
3. Store embeddings in the vector database.
4. Retrieve relevant document information when a user asks a question.
5. Generate context-aware responses using the retrieved information.

### Admin Dashboard

Access the dashboard at `/admin` to:

- View usage statistics.
- Monitor conversation history.
- Manage knowledge-base documents.
- View daily activity charts.

## 💻 Development

### Available Scripts

```bash
npm run dev
npm run build
npm run start
npm run lint
npm run typecheck
```

| Command | Purpose |
|---|---|
| `npm run dev` | Start development server |
| `npm run build` | Build the application |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm run typecheck` | Run TypeScript checks |

### Adding New Languages

Update the supported language configuration in `lib/env.ts` and add the corresponding language name and translation support in the relevant chat components.

## ☁️ Deployment

The application can be deployed using supported hosting platforms such as:

### Vercel
1. Import your GitHub repository into Vercel.
2. Configure the required environment variables.
3. Deploy the application.

### Netlify
1. Connect your repository to Netlify.
2. Configure environment variables.
3. Deploy the application if the Next.js configuration is supported.

### Docker

If the repository includes a valid Dockerfile:

```bash
docker build -t ai-chat-assistant .
docker run -p 3000:3000 ai-chat-assistant
```

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/amazing-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add amazing feature"
   ```

4. Push your branch:

   ```bash
   git push origin feature/amazing-feature
   ```

5. Open a Pull Request.

## 📄 License

This project is distributed under the MIT License if an MIT `LICENSE` file is included in the repository.

## 🙌 Acknowledgements

- OpenAI for GPT models and text-to-speech APIs.
- Supabase for database and vector storage.
- shadcn/ui for UI components.
- Vercel for the Next.js framework.

---

**Built with Next.js, OpenAI, LangChain, and Supabase.**
