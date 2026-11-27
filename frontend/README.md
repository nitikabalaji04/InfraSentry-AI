# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

## Phase 1 – Day 11: Frontend and Backend Integration

### Objective
Integrate the React frontend with the FastAPI backend and SQLite database to deliver a complete infrastructure security scanning workflow.

### Technologies Used
- React.js – Frontend development
- Vite – Frontend development and build tool
- CSS – Responsive dashboard styling
- FastAPI – Backend API services
- SQLite – Database management
- Fetch API – Frontend and backend communication
- CORS Middleware – Cross-origin communication

### Features Implemented
- Responsive cybersecurity dashboard
- Backend connectivity indicator
- Database-driven security statistics
- Dockerfile and Terraform file uploads
- Frontend file type and size validation
- Security findings with severity levels and recommendations
- Database-driven scan history
- View, rename and delete scan functionality
- Loading states and error messages
- Empty state handling
- Duplicate submission prevention during active requests

### Integrated API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Backend connectivity |
| POST | /api/upload | Upload and scan configuration files |
| GET | /api/scans | Retrieve scan history |
| GET | /api/scans/{scan_id} | Retrieve individual reports |
| PUT | /api/scans/{scan_id} | Update scan records |
| DELETE | /api/scans/{scan_id} | Delete scan records |
| GET | /api/analytics/summary | Retrieve security statistics |

### Complete Application Workflow

User selects configuration file → Frontend validates input → API receives file → Backend performs security analysis → SQLite stores scan results → Frontend displays security report → Dashboard statistics and scan history are refreshed.

### Testing Results

| Test | Result |
|---|---|
| Backend connectivity | Passed |
| Database statistics retrieval | Passed |
| Dockerfile security scanning | Passed – 3 findings |
| Terraform security scanning | Passed – 3 findings |
| Unsupported file validation | Passed |
| Scan history retrieval | Passed |
| Rename scan record | Passed |
| Delete scan record | Passed |
| Frontend production build | Passed |

### Challenges and Solutions

- Cross-origin communication: Configured CORS middleware to allow communication between the local React frontend and FastAPI backend.
- API integration: Created a centralized API service module to manage requests and responses.
- Invalid file submissions: Implemented frontend validation and meaningful error messages.
- Dashboard synchronization: Implemented automatic data refresh after successful database operations.
- Duplicate submissions: Disabled submission controls while processing requests.

### Running the Application

Start the backend from the project root:

```bash
uvicorn app.main:app --reload --app-dir backend
```

Start the frontend in a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

Backend: http://127.0.0.1:8000

API Documentation: http://127.0.0.1:8000/docs

### Outcome

Successfully integrated the frontend, backend and database into a functional infrastructure security scanning application. The application supports configuration file analysis, security report visualization and scan record management through a unified dashboard.

The current security scanner uses preliminary rule-based detection and does not guarantee that a configuration is completely secure.