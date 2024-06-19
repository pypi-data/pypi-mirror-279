#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git |
#========================================================================================================================================
from evo_framework import *
import httpx

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path + "/../../../../")

import lz4.frame
import requests

class CFastApiClient:
    __instance = None

    def __init__(self):
        CFastApiClient.__instance = self
        self.version = "20240130"
        self.mapEClass = {}
        self.mapEAction = {}
        self.currentPathCOnfig = os.path.dirname(os.path.abspath(__file__))
        self.eApiConfig:EApiConfig = EApiConfig()
# ----------------------------------------------------------------------------------------------------------------------------------------  
    @staticmethod
    def getInstance():
        if CFastApiClient.__instance is None:
            cObject = CFastApiClient()
            cObject.doInit()
        return CFastApiClient.__instance

# ----------------------------------------------------------------------------------------------------------------------------------------  
    def doInit(self):
        try:
            self.eApiConfig.doGenerateID()
            sk, pk = IuCryptEC.generate_key_pair()
            IuLog.doVerbose(__name__, f"key generate :{sk} {pk}")
            self.eApiConfig.secretKey = sk
            self.eApiConfig.publicKey = pk.to_string()
            self.eApiConfig.isFirstStart = True 
            
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise Exception

# ----------------------------------------------------------------------------------------------------------------------------------------  
    async def doRequest(self, eAction:EAction):
        url ="http://172.20.10.10:8081/do_action"
        print("doRequest",url)
        
            # Data to send - modify this as per your ItemData model
        
        
        
        eRequest = ERequest()
        eRequest.doGenerateID()
        
        eRequest.data = eAction.toBytes()
        
        eRequest.hash = IuCryptHash.toSha256Bytes(eRequest.data)
        
        IuLog.doVerbose(__name__, f"self{self.eApiConfig}")
        

        eRequest = ERequest()    
        eRequest.id = self.eApiConfig.id
        eRequest.time = IuKey.generateTime()
        eRequest.data = eAction.toBytes()
        eRequest.hash = IuCryptHash.toSha256Bytes(eRequest.data)
        
        sign = IuCryptEC.sign_data( eRequest.hash, self.eApiConfig.secretKey)
        eRequest.pk = self.eApiConfig.publicKey
        eRequest.sign = sign
        eRequestBytes =  lz4.frame.compress(eRequest.toBytes()) 
        
        response = requests.post(url, data=eRequestBytes)

        eResponseBytes = response.content

        eResponseBytesDecompress =  lz4.frame.decompress(eResponseBytes) 
        #print(f"eResponseBytes:{eResponseBytesDecompress}")
       
        eResponse = IuApi.toEObject(EResponse(),eResponseBytesDecompress )
        print(f"eResponse.data :{eResponse }")
        eActionOutput:EAction = IuApi.toEObject(EAction(),eResponse.data )
   
        print(f"eAction:{eAction}")
        
        return eActionOutput
        
       
       
        '''
        print("len eRequestBytes:",len(eRequestBytes))
        timeout = httpx.Timeout(60.0, connect=10.0)
        timeout = httpx.Timeout(60.0, connect=10.0, read=120.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(url, content=eRequestBytes)
                response.raise_for_status()

                async for data in response.aiter_bytes():
                    if data:
                        print("Received chunk:", data)  # Debug output
                        eAction:EAction = IuApi.toEObject(EAction(), data)
                        item = eAction.mapInput.doGet("output_text")
                        print("EActionItem:", item)
                        text = await eAction.fromApiType("output_text")
                        print("Decoded text:", text)

            except httpx.HTTPStatusError as e:
                print(f"HTTP error: {e}")
            except httpx.RequestError as e:
                print(f"Request error: {e}")
            except Exception as ex:
                print(f"An unexpected error occurred: {ex}")
                
        '''

'''
if __name__ == "__main__":
    asyncio.run(test_streaming_response('http://172.20.10.10:8081/do_action'))
'''