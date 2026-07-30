from workers import Response, WorkerEntrypoint, Request
import urllib.parse

IMAGES = {
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

        imageName = urllib.parse.urlsplit(request.url).path[1:] # remove leading '/'

        userAgent = request.headers.get("User-Agent")
        if (userAgent is None) or ("discord" not in userAgent.lower()):

            if imageName in IMAGES:
                redirect = IMAGES[imageName][1]
            else:
                redirect = "https://github.com/Loupau38/shapez2-enhanced-gifs"

            return Response.redirect(redirect)

        if imageName not in IMAGES:
            return Response(status=404)

        fileName = IMAGES[imageName][0]
        fileType = fileName.split(".")[-1]
        image:Response = await self.env.ASSETS.fetch(f"https://example.com/{fileName}")
        return Response(await image.bytes(),headers={"Content-Type": f"image/{fileType}"})