# Blockchain
NeuroGuard
NeuroGuard Biosignal API and Consent Ledger
This repository provides the backend API for a simulated NeuroGuard system, which reads biosignal data, processes it (via a mocked AI), and handles consent and data logging using a simulated blockchain ledger.
The Python API uses FastAPI for performance and includes a robust fallback mechanism for hardware reading, allowing the server to run perfectly even without a physical device connected.
📁 Repository Structure
.
├── README.md
├── requirements.txt
├── main.py
└── blockchain/
    └── NeuroGuardConsentLedger.sol

🚀 Setup and Installation
1. Prerequisites
 * Python 3.9+
 * Node.js and npm (for deploying the Solidity contract, e.g., using Hardhat or Foundry)
2. Python Backend Setup
 * Clone the repository:
   git clone [your-repo-link]
cd neuroguard-project

 * Create a virtual environment (Recommended):
   python -m venv venv
source venv/bin/activate  # On Linux/macOS
.\venv\Scripts\activate   # On Windows

 * Install dependencies:
   pip install -r requirements.txt

3. Running the FastAPI Server
The server will automatically detect if a serial device is available on the configured port and use mock data if none is found.
 * Identify your Serial Port:
   * If you have a physical device (e.g., Arduino), find its port (e.g., /dev/ttyUSB0 on Linux, COM3 on Windows).
   * Edit main.py and update the SERIAL_PORT variable to your correct port name.
 * Start the Server:
   uvicorn main:app --reload

   The server will start at http://127.0.0.1:8000. You can access the interactive documentation at http://127.0.0.1:8000/docs.
4. API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| /biosignals/live | GET | Fetches a raw biosignal reading. Uses real serial data if available, otherwise returns mock data. |
| /process_data | POST | Simulates AI analysis of received biosignal data and returns a suggested action and ledger update status. |
| /ledger/status | GET | Mocks the current status of the blockchain consent ledger. |
🔗 Solidity Smart Contract
The NeuroGuardConsentLedger.sol contract is a basic smart contract designed to record a user's immutable consent status on a blockchain.
Compilation and Deployment (Conceptual)
 * Install Hardhat/Foundry (if not already installed).
 * Compile the contract:
   # Example using Hardhat
npx hardhat compile

 * Deploy: Deploy the compiled contract to a testnet (e.g., Sepolia) or a local development blockchain (e.g., Ganache).
 * Update main.py (Mock): In a real-world scenario, you would update the main.py file to include the deployed contract's address and ABI for actual interaction. In this current setup, all blockchain interactions are mocked.
License
This project is open-source and available under the MIT License.
