from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import datetime
import ipfsapi
import os
import json
from web3 import Web3, HTTPProvider
from django.core.files.storage import FileSystemStorage
import pickle
from pycocks.cocks import CocksPKG
from pycocks.cocks import Cocks

api = ipfsapi.Client(host='http://127.0.0.1', port=5001)
global details, username

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'DataPrivacy.json' #Blockchain DataPrivacy contract code
    deployed_contract_address = '0x546626da110F8C7714a274c0CF81FABE7491f69d' #hash address to access DataPrivacy contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'signup':
        details = contract.functions.getSignup().call() #call this function to get signup data
    if contract_type == 'messages':
        details = contract.functions.getPrivateMessages().call()#call this function to get private messages    
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'DataPrivacy.json' #Blockchain contract file
    deployed_contract_address = '0x546626da110F8C7714a274c0CF81FABE7491f69d' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'signup':
        details+=currentData
        msg = contract.functions.setSignup(details).transact()#call this function to save signup data in Blockchain
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'messages':
        details+=currentData
        msg = contract.functions.setPrivateMessages(details).transact()#call this function to save private messages
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def LoginAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        readDetails('signup')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == username and password == array[2]:
                status = "Welcome "+username
                break
        if status != 'none':
            file = open('session.txt','w')
            file.write(username)
            file.close()   
            context= {'data':status}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'Login.html', context)


def PostMessage(request):
    if request.method == 'GET':
        global username
        readDetails('signup')
        arr = details.split("\n")
        output =  '<tr><td><font size="" color="black">Private&nbsp;Data&nbsp;Shares</b></td><td><select name="t3" multiple>'
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'signup' and array[1] != username:
                output += '<option value="'+array[1]+'">'+array[1]+'</option>'
        output+="</select>"
        context= {'data':output}
        return render(request, 'PostMessage.html', context)

def ViewMessage(request):
    if request.method == 'GET':
        global username
        strdata = '<table border=1 color="white" align=center width=100% ><tr><th style="background-color:white;"><font size="" color="black">Owner</th><th style="background-color:white;"><font size="" color="black">Post Message</th>'
        strdata+='<th style="background-color:white;"><font size="" color="black">Share Users </th>'
        strdata+='<th style="background-color:white;"><font size="" color="black">Hashcode</th><th style="background-color:white;"><font size="" color="black">Image</th>'
        strdata+='<th style="background-color:white;"><font size="" color="black">Date Time</th></tr>'
        for root, dirs, directory in os.walk('static/tweetimages'):
            for j in range(len(directory)):
                os.remove('static/tweetimages/'+directory[j])
        readDetails('messages')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            user_list = array[3].split(",")
            if array[0] == 'post' and username in user_list:
                content = api.get_pyobj(array[4])
                content = pickle.loads(content)
                with open("DataPrivacyApp/static/tweetimages/"+array[6], "wb") as file:
                    file.write(content)
                file.close()
                strdata+='<tr><td style="background-color:white;"><font size="" color="black">'+str(array[1])+'</td>'
                strdata+='<td style="background-color:white;"><font size="" color="black">'+str(array[2])+'</td>'
                strdata+='<td style="background-color:white;"><font size="" color="black">'+str(array[3])+'</td>'
                strdata+='<td style="background-color:white;"><font size="" color="black">'+str(array[4])+'</td>'
                strdata+='<td style="background-color:white;"><img src=static/tweetimages/'+array[6]+'  width=200 height=200></img></td>'
                strdata+='<td style="background-color:white;" ><font size="" color="black">'+str(array[5])+'</td>'
        context= {'data':strdata}
        return render(request, 'ViewMessage.html', context)        
         



        
def PostMessageAction(request):
    if request.method == 'POST':
        share_users = request.POST.getlist('t3')
        share_users = ','.join(share_users)
        post_message = request.POST.get('t1', False)
        filename = request.FILES['t2'].name
        myfile = request.FILES['t2'].read()
        myfile = pickle.dumps(myfile)
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        file.close()
        share_users += ','+user
        hashcode = api.add_pyobj(myfile)
        cocks_pkg = CocksPKG()
        public_key, private_key = cocks_pkg.extract(user)#generate public and private key using 'user' identity
        cocks = Cocks(cocks_pkg.n)
        enc = cocks.encrypt(post_message.encode(), private_key) #encrypt data by using private key data will be encrypted and store in Blockchain
        enc = str(enc[0])
        data = "post#"+user+"#"+post_message+"#"+share_users+"#"+str(hashcode)+"#"+str(current_time)+"#"+filename+"\n"
        saveDataBlockChain(data,"messages")#save encrrypted data in Blockchain
        output = 'Post message saved in Blockchain with below hashcodes & Media file saved in IPFS.<br/>'+str(hashcode)+"<br/>Encrypted Message: "+str(enc)
        context= {'data':output}
        return render(request, 'UserScreen.html', context)
        

def SignupAction(request):
    if request.method == 'POST':
        global details
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        output = "Username already exists"
        readDetails('signup')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == username:
                status = username+" already exists"
                break
        if status == "none":
            details = ""
            data = "signup#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"signup")
            context = {"data":"Signup process completed and record saved in Blockchain"}
            return render(request, 'Signup.html', context)
        else:
            context = {"data":status}
            return render(request, 'Signup.html', context)




