// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

//import all required sol.
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract MyToken is ERC721URIStorage, ERC721Enumerable{
    address public ownerOfContract;
    //constructor for ERC721
    constructor() ERC721("FearOfMissingOut", "FOMO") {
        ownerOfContract = msg.sender;
    }

    //ArtWork struct
    struct ArtWork{
        string name;
        string artist;
        uint256 appraisal;

    }

    //map artCollection to tokenId(uint256)
    mapping(uint256 => ArtWork) public artCollection;

    //Appraisal event
    event Appraisal(uint256 token_id, uint256 appraisal, string reportURI);

    //function to Creat the artwork
    function CreatArtwork(
        address ownerOfNFT,
        string memory name,
        string memory artist,
        uint256 appraisal,
        string memory tokenURIAddress
    ) public returns(uint256){
        require(msg.sender == ownerOfContract, "Only the owner who created the contract can create artwork.");
        uint256 tokenId = totalSupply();
        _mint(ownerOfNFT, tokenId);
        _setTokenURI(tokenId,tokenURIAddress);
        artCollection[tokenId] = ArtWork(name,artist,appraisal);

        return tokenId;
    }

    //If you own a specify NFT, you are a verified user,return true. May use for VIP
    function isNFTOwnerVIP(uint256 tokenId) public view returns(bool){
        return ownerOf(tokenId) == msg.sender;
    }
    //If you own any of the NFT,you have general access
    function isNFTOwner(address _address) public view returns(bool){
        uint count = balanceOf(_address);
        if(count > 0){
            return true;
        }
        return false;
    }

//function to add New Info,such as appraisal
    function newAppraisal(
        uint tokenId,
        uint _newAppraisal,
        string memory reportURI
        )public returns(uint256){
            artCollection[tokenId].appraisal = _newAppraisal;
            emit Appraisal(tokenId,_newAppraisal,reportURI);

            return artCollection[tokenId].appraisal; 
        }


//function for selling the NFT
    function buy(uint tokenId) public payable{
        // NFT exists
        require(_exists(tokenId), "NFT does not exist");
        //Who is the onwer of the NFT
        address payable currentOwnerOfNFT = payable(ownerOf(tokenId));
        //make sure the buyer has enough fund.
        require(msg.value > artCollection[tokenId].appraisal,"Insufficient payment.");
        //make sure the buyer not already own the NFT
        require(msg.sender!= ownerOf(tokenId),"You already own this NFT.");
        //Transfer fund
        currentOwnerOfNFT.transfer(msg.value);
        //transfer NFT
        _transfer(currentOwnerOfNFT,msg.sender,tokenId);

        //Update the appraisal after transaction.
        newAppraisal(tokenId,msg.value,"FreeTrade");
    }

// event for Signing message
event Sign(address signer, string message, bytes32 signature);

//function Sign message
    function sign(string memory message) public {
        //acquire request address
        address signer = msg.sender;
        //use encodePacked to sign
        bytes32 signature = keccak256(abi.encodePacked(signer,message));
        //emit the Sign event
        emit Sign(signer,message,signature);
    }

//functions need to be override.
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 firstTokenId,
        uint256 batchSize
    ) internal virtual override (ERC721,ERC721Enumerable) {
    super._beforeTokenTransfer(from, to, firstTokenId, batchSize);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721,ERC721Enumerable) returns (bool) {
        return
            interfaceId == type(IERC721).interfaceId ||
            interfaceId == type(IERC721Metadata).interfaceId ||
            super.supportsInterface(interfaceId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
}   

