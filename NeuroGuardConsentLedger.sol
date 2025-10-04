// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title NeuroGuardConsentLedger
 * @dev A simplified smart contract to record immutable user consent status 
 * for biosignal data usage in a decentralized manner.
 *
 * NOTE: This is a simplified mock contract for demonstration purposes. 
 * Actual implementation would require more sophisticated access controls 
 * and data structures.
 */
contract NeuroGuardConsentLedger {
    // Mapping of user ID to their current consent status (e.g., true = given, false = revoked)
    mapping(address => bool) private userConsentStatus;
    
    // Structure to record an immutable history of consent changes
    struct ConsentRecord {
        uint256 timestamp;
        bool hasConsent;
        bytes32 transactionHash;
    }
    
    // Mapping of user ID to an array of their consent history
    mapping(address => ConsentRecord[]) public consentHistory;

    // Event emitted when a user's consent status is updated
    event ConsentUpdated(
        address indexed userAddress, 
        bool newConsentStatus, 
        uint256 timestamp
    );

    /**
     * @dev Allows an external system (e.g., the NeuroGuard API) to set or revoke consent.
     * @param _userAddress The blockchain address representing the user or their data proxy.
     * @param _consentStatus True for consent given, False for consent revoked.
     */
    function setConsent(address _userAddress, bool _consentStatus) public {
        // Only the owner or an authorized contract should call this in a real system.
        // For this mock, we skip complex authorization.
        
        userConsentStatus[_userAddress] = _consentStatus;
        
        // Record the immutable history of this action
        consentHistory[_userAddress].push(ConsentRecord({
            timestamp: block.timestamp,
            hasConsent: _consentStatus,
            transactionHash: tx.hash
        }));
        
        emit ConsentUpdated(_userAddress, _consentStatus, block.timestamp);
    }

    /**
     * @dev Returns the current consent status for a given user address.
     * @param _userAddress The address of the user.
     * @return A boolean indicating the current consent status.
     */
    function getConsentStatus(address _userAddress) public view returns (bool) {
        return userConsentStatus[_userAddress];
    }

    /**
     * @dev Returns the number of times a user's consent has been recorded/changed.
     * @param _userAddress The address of the user.
     * @return The total count of consent records.
     */
    function getConsentRecordCount(address _userAddress) public view returns (uint256) {
        return consentHistory[_userAddress].length;
    }
}

