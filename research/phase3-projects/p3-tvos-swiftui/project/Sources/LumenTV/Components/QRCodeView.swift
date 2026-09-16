import SwiftUI
import CoreImage.CIFilterBuiltins

/// Renders a QR code for the activation URL. Light tile on the dark canvas so phone cameras lock quickly;
/// quiet zone is provided by the tile padding. Decorative for VoiceOver: the code text carries the semantics.
struct QRCodeView: View {
    let payload: String
    var size: CGFloat = 320

    var body: some View {
        Group {
            if let image = Self.makeImage(payload) {
                Image(uiImage: image)
                    .interpolation(.none)
                    .resizable()
                    .scaledToFit()
            } else {
                RoundedRectangle(cornerRadius: 8).fill(Color.gray)
            }
        }
        .frame(width: size, height: size)
        .padding(LumenSpace.m)
        .background(Color.white, in: RoundedRectangle(cornerRadius: LumenFocus.cornerRadius, style: .continuous))
        .accessibilityHidden(true)
    }

    private static func makeImage(_ payload: String) -> UIImage? {
        let filter = CIFilter.qrCodeGenerator()
        filter.message = Data(payload.utf8)
        filter.correctionLevel = "M"
        guard let output = filter.outputImage else { return nil }
        let scaled = output.transformed(by: CGAffineTransform(scaleX: 12, y: 12))
        let context = CIContext()
        guard let cg = context.createCGImage(scaled, from: scaled.extent) else { return nil }
        return UIImage(cgImage: cg)
    }
}
