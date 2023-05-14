pragma solidity >= 0.8.11 <= 0.8.11;

contract DataPrivacy {
    string public signup_details;
    string public private_messages;
    
       
    //call this function to save new user details data to Blockchain
    function setSignup(string memory sd) public {
       signup_details = sd;	
    }
   //get Signup details
    function getSignup() public view returns (string memory) {
        return signup_details;
    }

    //call this function to save private messages to Blockchain
    function setPrivateMessages(string memory pt) public {
       private_messages = pt;	
    }
   //get private messages details
    function getPrivateMessages() public view returns (string memory) {
        return private_messages;
    }

   constructor() public {
        signup_details="";
	private_messages="";
    }
}