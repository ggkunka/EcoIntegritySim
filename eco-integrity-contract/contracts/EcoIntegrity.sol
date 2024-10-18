// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EcoIntegrity {
    struct DataLog {
        uint id;
        string dataHash;
        uint timestamp;
        address logger;
    }

    uint public logCount = 0;
    mapping(uint => DataLog) public logs;

    // Event for debugging purposes
    event DebugLog(string message);
    event NewLog(uint id, string dataHash, uint timestamp, address logger);

    // Updated logData function with debugging logs
    function logData(string memory dataHash) public {
        // Emit a debug event to check function entry
        emit DebugLog("Entering logData function");

        // Increase log count and log the data
        logCount++;
        logs[logCount] = DataLog(logCount, dataHash, block.timestamp, msg.sender);

        // Emit a debug event to check log creation
        emit DebugLog("Log created");

        // Emit event with log details
        emit NewLog(logCount, dataHash, block.timestamp, msg.sender);

        // Emit a debug event to check function exit
        emit DebugLog("Exiting logData function");
    }

    function getLog(uint id) public view returns (string memory dataHash, uint timestamp, address logger) {
        DataLog memory logEntry = logs[id];
        return (logEntry.dataHash, logEntry.timestamp, logEntry.logger);
    }
}
