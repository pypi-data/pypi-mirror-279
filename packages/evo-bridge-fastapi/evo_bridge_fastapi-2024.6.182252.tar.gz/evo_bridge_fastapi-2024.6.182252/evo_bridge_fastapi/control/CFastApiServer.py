#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git |
#========================================================================================================================================

from evo_framework import *
import importlib.metadata
try:
    evo_framework_version = importlib.metadata.version('evo_framework')
    IuLog.doDebug(__name__, f"evo_framework version: {evo_framework_version}")
except importlib.metadata.PackageNotFoundError:
    raise Exception("ERROR_evo_framework_NOT_ISTALLED")


from fastapi import BackgroundTasks
from fastapi import FastAPI, HTTPException
from fastapi import Request as RequestFastApi
from fastapi.responses import FileResponse
from fastapi import Response as ResponseFastApi
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, MutableMapping
import uvicorn

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime

from typing import BinaryIO
from fastapi import HTTPException, Request, status
from fastapi.responses import StreamingResponse
import struct

current_path = os.path.dirname(os.path.abspath(__file__))

class CustomStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: MutableMapping[str, Any]):
        response = await super().get_response(path, scope)
        response.headers["ngrok-skip-browser-warning"] = "1234"

        if path.endswith(".mp4") and isinstance(response, FileResponse):
            response.headers["Content-Type"] = "video/mp4"

        if isinstance(response, FileResponse):
            print("response HEADER", path, response.headers)

        return response

#CORS ALLOW
origins = ["*"]



static_files_dir = f"{current_path}/../assets"
templates = Jinja2Templates(directory=f"{current_path}/../assets_template")

# ----------------------------------------------------------------------------------------------------------------------------------------  
class CFastApiServer:
    __instance = None

    def __init__(self):
        CFastApiServer.__instance = self
        self.version = "20240130"
        self.eApiConfig = CApiFlow.getInstance().eApiConfig
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.app.mount(
            "/assets", CustomStaticFiles(directory=static_files_dir), name="assets"
        ) 
        self.mapEClass = {}
        self.mapEAction = {}
        self.currentPathCOnfig = os.path.dirname(os.path.abspath(__file__))
# ----------------------------------------------------------------------------------------------------------------------------------------  
    @staticmethod
    def getInstance():
        if CFastApiServer.__instance is None:
            cObject = CFastApiServer()
            # cObject.doInit()
        return CFastApiServer.__instance

# ----------------------------------------------------------------------------------------------------------------------------------------  
    async def doInit(self):
        try:
            CApiFlow.getInstance().doInit()

            if self.eApiConfig.enumApiTunnel ==  EnumApiTunnel.LOCAL:
                self.eApiConfig.remoteUrl = (
                    f"http://{IuSystem.get_local_ip()}:{str(self.eApiConfig.localPort)}"
                )
            
            elif self.eApiConfig.enumApiTunnel == EnumApiTunnel.NGROK:
                from evo_packages.evo_package_tunnel.utility.IuTunnelNGrok import IuTunnelNgrok
                ngrokToken = CSetting.getInstance().mapSetting["ngrokToken"]
                self.eApiConfig.remoteUrl = await IuTunnelNgrok.do_use_ngrok(
                    ngrokToken, self.eApiConfig.localPort
                )
                
            elif self.eApiConfig.enumApiTunnel == EnumApiTunnel.PINGGY:
                from evo_packages.evo_package_tunnel.utility.IuTunnelPinggy import IuTunnelPinggy
                pinggyToken = ""  # CSetting.getInstance().mapSetting["ngrokToken"]
                
                self.eApiConfig.remoteUrl = await IuTunnelPinggy.do_use_pinggy(
                    pinggyToken, self.eApiConfig.localPort
                )

            await CApiFlow.getInstance().doInitEApiConfig()
            
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise Exception

# ----------------------------------------------------------------------------------------------------------------------------------------  
    async def doGenerateTotp(self) -> str:
        try:
            envTotp = "cyborgai_totp"

            if os.environ.get(envTotp) is None:
                randBase32 = IuTotp.doGenerateRand()
                os.environ[envTotp] = randBase32

            randBase32 = os.environ[envTotp]
            urlTotp = IuTotp.doGenerateUrl(
                randBase32, self.eApiConfig.label, f"CyborgAI_{self.eApiConfig.label}"
            )
            return urlTotp
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception

# ----------------------------------------------------------------------------------------------------------------------------------------  
    async def doRunServer(self):
        try:
            await self.doInit()
          
            # -----------------------------------------------------------------------------------------------------------------------------
            @self.app.get("/admin/{id}", response_class=HTMLResponse)
            async def read_item(request: Request, id: str):
                IuLog.doInfo(__name__, f"id:{id}")
                return templates.TemplateResponse(
                    name="admin.html", context={"request": request, "id": id}
                )

            # -----------------------------------------------------------------------------------------------------------------------------
            @self.app.post("/do_action", tags=["action"])
            async def do_action(
                request: RequestFastApi, background_tasks: BackgroundTasks
            ):
                try:
                    startTime = time.time_ns()
                    dataERequest = await request.body()

                    idERequest, dataInput = await CApiFlow.getInstance().onRequest(dataERequest, checkSign=True)
                   
                    eAction:EAction = IuApi.toEObject(EAction(), dataInput) 
                    eActionTask = EActionTask()
                    eActionTask.id = idERequest
                    eActionTask.doGenerateTime()  
                    eActionTask.action = eAction.action
                    eActionTask.eActionInput = eAction
                    eApi = CApiFlow.getInstance().doGetEApi(eAction.action)
                    
                    async def onAction() -> bytes:
                        eActionOutput:EAction = await CApiFlow.getInstance().onAction(eApi, eActionTask)
                        return await CApiFlow.getInstance().onResponse(idERequest, eActionOutput.toBytes())
                    
                    async def onActionStream():
                        async for eActionOutput in  CApiFlow.getInstance().onActionStream(eApi, eActionTask):
                            dataAction=eActionOutput.toBytes()
                            IuLog.doDebug(__name__, f"eActionOutput:{eActionOutput}")
                            data = await CApiFlow.getInstance().onResponse(idERequest, dataAction)
                      
                            if data is None:
                                raise Exception("ERROR_NOT_VALID_ERESPONSE")
         
                            dataStream = struct.pack('<l', len(data)) + data
      
                            endTime =time.time_ns()
                            elapsedTime = endTime - startTime
                            elapsedTimeSecond = elapsedTime / 1e9
                            
                            IuLog.doInfo(__name__, f"onActionStream id:{eActionOutput.id} dataStream:{len(dataStream)} {elapsedTimeSecond:.9f} s")
                            yield  dataStream
                    
                    
                    if eApi.isStream:
                        return StreamingResponse(onActionStream(), media_type="application/octet-stream",background=background_tasks)
                    else:
                        dataOutput = await onAction()
                        endTime =time.time_ns()
                        elapsedTime = endTime - startTime
                        elapsedTimeSecond = elapsedTime / 1e9
                        IuLog.doInfo(__name__, f"onAction id:{idERequest} dataStream:{len(dataOutput)} {elapsedTimeSecond:.9f} s")
                        return ResponseFastApi(content=dataOutput, media_type="application/octet-stream")

                except Exception as exception:
                    IuLog.doException(__name__, exception)
                    return ResponseFastApi(content=f"Error processing the action: {str(exception)}", status_code=500)

            # -----------------------------------------------------------------------------------------------------------------------------
            @self.app.on_event("shutdown")
            async def shutdown_event():
                try:
                    IuLog.doInfo(__name__, "Shutdown event")
                # await CRtcServer.getInstance().onShutdown()
                except Exception as exception:
                    IuLog.doException(__name__, exception)

            # -----------------------------------------------------------------------------------------------------------------------------
            CSetting.getInstance().eSettings.remoteUrl = self.eApiConfig.remoteUrl
            
            
            
            IuLog.doInfo(__name__, f"versionApi: {CApiFlow.getInstance().version}")
            IuLog.doInfo(__name__, f"versionServer: {self.version}")
            IuLog.doDebug(__name__, f"eApiConfig: {self.eApiConfig}")
            IuLog.doInfo(
                __name__, f"remote_url: {CSetting.getInstance().eSettings.remoteUrl}"
            )
            CApiFlow.getInstance().doPrintMapEApi()

            if self.eApiConfig.isFirstStart:
                urlTotp = await self.doGenerateTotp()
               
                print(
                    f"\x1b[31mDownload Google authenticator use totp for the first access:\x1b[0m"
                )
                
                await IuQrCode.doPrintAscii(urlTotp, isInvert=True)
                print(f"\x1b[31m\n{self.eApiConfig.remoteUrl}/admin\n\x1b[0m")
                print(f"{urlTotp}\n")

            else:
                pathQrCode = static_files_dir + "/qrcode.png"
                pathQrLogo = static_files_dir + "/logo.png"
                await IuQrCode.doGenerate(
                    self.eApiConfig.cyborgaiToken, pathQrCode, pathQrLogo
                )
                print(f"{self.eApiConfig.cyborgaiToken}\n")
                print(f"\n{self.eApiConfig.remoteUrl}/assets/qrcode.png\n")
           
            print(f"Visibility: {self.eApiConfig.enumApiVisibility.name}\n")
            
            config = uvicorn.Config(
                app=self.app,
                host=self.eApiConfig.localAddress,
                port=self.eApiConfig.localPort,
                loop="asyncio",
            )

            server = uvicorn.Server(config)
            await server.serve()

        except Exception as exception:
            IuLog.doException(__name__, exception)
# ---------------------------------------------------------------------------------------------------------------------------------------- 
