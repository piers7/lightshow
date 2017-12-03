<Query Kind="FSharpExpression">
  <NuGetReference>System.Reactive</NuGetReference>
  <Namespace>System.Drawing</Namespace>
  <Namespace>System.Reactive</Namespace>
  <Namespace>System.Reactive.Linq</Namespace>
</Query>

let targetUri = Uri "tcp://pizero3:7890"
let pixelCount = 200
let decayRate = 20
let refreshRate = TimeSpan.FromSeconds(0.20)
let previewScale = 10

//let toColor (rgb:UInt32) = 
//    let r = rgb >>> 16   |> byte
//    let g = rgb >>> 8    |> byte
//    let b = rgb         |> byte
//    (r,g,b)
//
//let toPixel (r,g,b) = uint32 (r <<< 16) ||| uint32 (g <<< 8) ||| uint32 b

let random = new System.Random()

let reduceBrightness by (r,g,b) = 
    [|r;g;b|]
    |> Array.map (function
        | x when x > (byte by) -> x - (byte by)
        | x -> x
    )
    |> fun x -> x.[0],x.[1],x.[2]
    
let decay = Array.map (reduceBrightness decayRate)

let ping pixels =
    let live = random.Next(0, pixelCount)
    pixels
    |> Array.mapi (fun i p -> 
        match (i,p) with
        | (i,_) when i = live -> (0xFFuy,0xFFuy,0xFFuy)
        | (i,other) -> other
    )

let mutable pixels = Array.create pixelCount (0uy,0uy,0uy)

let transform = 
    ping 
    >> decay

let bitmapFromPixels (width,height) scale pixels =
    let bitmap = new Bitmap((width:int) * scale, height * scale)
    use graphics = Graphics.FromImage(bitmap)
    pixels |> Seq.iteri (fun i c -> 
        let x = i % width
        let y = i / width
        let brush = new System.Drawing.SolidBrush(c)
        graphics.FillRectangle(brush, System.Drawing.Rectangle(x*scale, y*scale, scale, scale))
    )
    bitmap

let view sequence = 
    sequence
    |> Observable.map (
        Array.map (fun (r,g,b) -> Color.FromArgb(int r, int g, int b))
        >> bitmapFromPixels (200/10,10) previewScale    
    )
    |> LINQPad.Extensions.DumpLatest

let send (pixels:(byte*byte*byte)[]) = 
    let message = 
        [|
            0uy // broadcast / all channels
            0uy // set pixels
            (pixels.Length >>> 8 |> byte)     // high byte
            (pixels.Length |> byte)   // low byte
        |]
        |> Array.append (pixels |> Array.collect (fun (r,g,b) -> [| r; g; b |]))
    use socket = new System.Net.Sockets.TcpClient()
    do socket.Connect(targetUri.Host, targetUri.Port)
    use stream = socket.GetStream()
    stream.Write(message, 0, message.Length)
    ()

let doit fn item = fn item; item

let rec sendWorker () = 
    async {
        do
            pixels |> send
        do! Async.Sleep 250
        return! sendWorker ()
    }

Async.Start ( async { do! sendWorker () } )
do
    Observable
        .Interval(refreshRate)
        |> Observable.map (fun i ->
            pixels <- pixels |> transform
            pixels
        )
        |> Observable.map (doit send)
        |> view
        |> ignore