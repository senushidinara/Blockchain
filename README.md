# Blockchain
NeuroGuard
# NeuroGuard Biosignal API and Consent Ledger

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.115.2-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

This repository provides the backend API for a simulated **NeuroGuard** system, which reads biosignal data, processes it (via a mocked AI), and handles consent and data logging using a simulated blockchain ledger.

The Python API uses **FastAPI** for performance and includes a robust fallback mechanism for hardware reading, allowing the server to run perfectly even without a physical device connected.

---

## 📁 Repository Structure

    ├── README.md
    ├── requirements.txt
    ├── main.py
    └── blockchain/
        └── NeuroGuardConsentLedger.sol

---

<details>
<summary>🚀 Setup and Installation</summary>

### 1. Prerequisites
- Python 3.9+
- Node.js and npm (for deploying the Solidity contract, e.g., using Hardhat or Foundry)

### 2. Python Backend Setup

    # Clone the repository
    git clone https://github.com/NeuroGuardOfficial/neuroguard-project.git
    cd neuroguard-project

    # Create a virtual environment (Recommended)
    python -m venv venv
    source venv/bin/activate   # On Linux/macOS
    .\venv\Scripts\activate    # On Windows

    # Install dependencies
    pip install -r requirements.txt

### 3. Running the FastAPI Server
The server will automatically detect if a serial device is available on the configured port and use mock data if none is found.

- Identify your Serial Port:
    - If you have a physical device (e.g., Arduino), find its port (e.g., /dev/ttyUSB0 on Linux, COM3 on Windows)
    - Edit main.py and update the SERIAL_PORT variable to your correct port name

- Start the Server:

    uvicorn main:app --reload

The server will start at: http://127.0.0.1:8000  
Interactive documentation is available at: http://127.0.0.1:8000/docs

</details>

---

<details>
<summary>4. API Endpoints</summary>

    Endpoint: /biosignals/live
    Method: GET
    Description: Fetches a raw biosignal reading. Uses real serial data if available, otherwise returns mock data.

    Endpoint: /process_data
    Method: POST
    Description: Simulates AI analysis of received biosignal data and returns a suggested action and ledger update status.

    Endpoint: /ledger/status
    Method: GET
    Description: Mocks the current status of the blockchain consent ledger.

</details>

---

<details>
<summary>🔗 Solidity Smart Contract</summary>

The `NeuroGuardConsentLedger.sol` contract is a basic smart contract designed to record a user's **immutable consent status** on a blockchain.

### Compilation and Deployment (Conceptual)

- Install Hardhat or Foundry (if not already installed)
- Compile the contract:

        npx hardhat compile

- Deploy: Deploy the compiled contract to a testnet (e.g., Sepolia) or a local blockchain (e.g., Ganache)
- Update main.py (Mock): In a real-world scenario, update the main.py file to include the deployed contract's **address** and **ABI** for actual interaction. In this setup, all blockchain interactions are mocked.

</details>

---

<details>
<summary>📜 Example Consent Record</summary>

    {
      "patient_id": "12345",
      "consent_given": true,
      "data_type": "EEG_signal",
      "timestamp": "2025-10-05T12:00:00Z",
      "signature": "0xA7B9C12345DEADBEEF67890ABCDEF"
    }

</details>

---

<details>
<summary>📚 Requirements</summary>

- Python 3.9+  
- web3.py  
- Flask  
- cryptography  
- mne (for EEG data)  
- yasa (sleep stage analysis)  

</details>

---

<details>
<summary>🔮 Future Work</summary>

- AI-driven anomaly detection in EEG signals  
- Integration with hospital EHR systems  
- Multi-chain interoperability  
- Zero-knowledge proof for private consent verification  

</details>

---

## 📜 License
MIT License © 2025 NeuroGuard Project
