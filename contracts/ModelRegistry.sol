// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ModelRegistry {

    struct ModelVersion {
        string modelName;
        string modelHash;
        address registeredBy;
        uint256 timestamp;
        uint256 version;
    }

    mapping(string => ModelVersion[]) private modelVersions;
    mapping(string => bool) private modelExists;

    event ModelRegistered(string modelName, string modelHash, address registeredBy, uint256 timestamp, uint256 version);
    event ModelVerified(string modelName, bool isValid, uint256 timestamp);

    function registerModel(string memory modelName, string memory modelHash) public {
        uint256 newVersion = modelVersions[modelName].length + 1;
        modelVersions[modelName].push(ModelVersion({
            modelName: modelName,
            modelHash: modelHash,
            registeredBy: msg.sender,
            timestamp: block.timestamp,
            version: newVersion
        }));
        modelExists[modelName] = true;
        emit ModelRegistered(modelName, modelHash, msg.sender, block.timestamp, newVersion);
    }

    function verifyModel(string memory modelName, string memory modelHash) public returns (bool) {
        require(modelExists[modelName], "Model not found on blockchain");
        uint256 latestIndex = modelVersions[modelName].length - 1;
        bool isValid = keccak256(abi.encodePacked(modelVersions[modelName][latestIndex].modelHash)) == keccak256(abi.encodePacked(modelHash));
        emit ModelVerified(modelName, isValid, block.timestamp);
        return isValid;
    }

    function getLatestModelInfo(string memory modelName) public view returns (
        string memory name,
        string memory hash,
        address registeredBy,
        uint256 timestamp,
        uint256 version
    ) {
        require(modelExists[modelName], "Model not found");
        uint256 latestIndex = modelVersions[modelName].length - 1;
        ModelVersion memory m = modelVersions[modelName][latestIndex];
        return (m.modelName, m.modelHash, m.registeredBy, m.timestamp, m.version);
    }

    function getModelVersion(string memory modelName, uint256 versionIndex) public view returns (
        string memory name,
        string memory hash,
        address registeredBy,
        uint256 timestamp,
        uint256 version
    ) {
        require(modelExists[modelName], "Model not found");
        require(versionIndex < modelVersions[modelName].length, "Version does not exist");
        ModelVersion memory m = modelVersions[modelName][versionIndex];
        return (m.modelName, m.modelHash, m.registeredBy, m.timestamp, m.version);
    }

    function getVersionCount(string memory modelName) public view returns (uint256) {
        return modelVersions[modelName].length;
    }

    function isModelRegistered(string memory modelName) public view returns (bool) {
        return modelExists[modelName];
    }
}