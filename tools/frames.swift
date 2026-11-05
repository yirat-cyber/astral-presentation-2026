// Extract JPEG frames from a video at given seconds.
// Usage: swift tools/frames.swift <video.mp4> <out_prefix> <sec> [<sec> ...]
import AVFoundation
import AppKit

let args = CommandLine.arguments
let asset = AVURLAsset(url: URL(fileURLWithPath: args[1]))
let gen = AVAssetImageGenerator(asset: asset)
gen.appliesPreferredTrackTransform = true
gen.requestedTimeToleranceBefore = .zero
gen.requestedTimeToleranceAfter = .zero
gen.maximumSize = CGSize(width: 1080, height: 1920)
let dur = CMTimeGetSeconds(asset.duration)
print("duration \(dur)")
for s in args[3...] {
    let t = min(Double(s)!, dur - 0.1)
    do {
        let cg = try gen.copyCGImage(at: CMTime(seconds: t, preferredTimescale: 600), actualTime: nil)
        let rep = NSBitmapImageRep(cgImage: cg)
        let data = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.82])!
        let out = "\(args[2])_\(s).jpg"
        try data.write(to: URL(fileURLWithPath: out))
        print(out, cg.width, cg.height)
    } catch { print("fail \(s): \(error)") }
}
