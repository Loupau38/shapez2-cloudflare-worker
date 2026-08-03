from workers import Response, WorkerEntrypoint, Request
import urllib.parse

ENHANCED_GIFS = {
    "notch.gif" : (
        "notch.gif",
        "https://shapez2.wiki.gg/wiki/Notch"
    ),
    "space-belt-pipe-throughput.gif" : (
        "space-belt-pipe-throughput.gif",
        "https://shapez2.wiki.gg/wiki/Space_Transport"
    )
}

class Default(WorkerEntrypoint):

    async def fetch(self, request:Request):

        path = urllib.parse.urlsplit(request.url).path[1:] # remove leading '/'

        if path.startswith("gif/"):
            return await enhancedGIFs(self,request,path.removeprefix("gif/"))

        return Response.redirect("https://github.com/Loupau38/shapez2-cloudflare-worker")

async def enhancedGIFs(self:Default,request:Request,path:str) -> None:

    if path not in ENHANCED_GIFS:
        return Response(status=404)

    userAgent = request.headers.get("User-Agent")
    if (userAgent is None) or ("discord" not in userAgent.lower()):
        return Response.redirect(ENHANCED_GIFS[path][1])

    fileName = ENHANCED_GIFS[path][0]
    fileType = fileName.split(".")[-1]
    image:Response = await self.env.ASSETS.fetch(f"https://example.com/{fileName}")
    return Response(await image.bytes(),headers={"Content-Type": f"image/{fileType}"})